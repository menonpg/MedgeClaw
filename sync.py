#!/usr/bin/env python3
"""MedgeClaw 同步脚本 — 读取 .medgeclaw-sync.yml 执行同步

用法: 
  python3 sync.py           # 完整同步
  python3 sync.py --remind  # 检查配置，如需要则同步，最后发送提醒消息

配置: .medgeclaw-sync.yml
环境: .env (MEDGECLAW_ROOT, OPENCLAW_DIR)
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ 需要 PyYAML: pip install pyyaml")
    sys.exit(1)


def load_env(medgeclaw_dir: Path) -> dict:
    """从 .env 文件加载环境变量（不覆盖已有的系统环境变量）"""
    env_file = medgeclaw_dir / ".env"
    if not env_file.exists():
        return {}
    env = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            # 展开 $HOME 和 ~ 等变量
            val = os.path.expandvars(val)
            val = os.path.expanduser(val)
            if key not in os.environ:
                os.environ[key] = val
            env[key] = val
    return env


def resolve_paths(medgeclaw_dir: Path):
    """从环境变量或默认值解析路径"""
    openclaw_dir = Path(os.environ.get("OPENCLAW_DIR", Path.home() / ".openclaw"))
    workspace = openclaw_dir / "workspace"
    config_path = openclaw_dir / "openclaw.json"

    if not config_path.exists():
        print(f"❌ 未找到 OpenClaw 配置: {config_path}")
        print("   请先安装并初始化 OpenClaw: https://docs.openclaw.ai")
        sys.exit(1)

    return openclaw_dir, workspace, config_path


def load_sync_config(medgeclaw_dir: Path) -> dict:
    config_path = medgeclaw_dir / ".medgeclaw-sync.yml"
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def sync_docs(docs, medgeclaw_dir: Path, workspace: Path):
    """同步文档（覆盖写入）"""
    print("📝 同步文档...")
    for item in docs:
        src_rel, dst_rel = [s.strip() for s in item.split("->")]
        src = medgeclaw_dir / src_rel
        dst = workspace / dst_rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"   ✅ {dst_rel}")
        else:
            print(f"   ⏭️  {src_rel} 不存在，跳过")


def sync_skills(skills, medgeclaw_dir: Path, workspace: Path):
    """同步 skills（整个目录复制）"""
    print("🎨 同步 skills...")
    for item in skills:
        src_rel, dst_rel = [s.strip() for s in item.split("->")]
        src = medgeclaw_dir / src_rel
        dst = workspace / dst_rel
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)
            print(f"   ✅ {dst_rel}")
        else:
            print(f"   ⏭️  {src_rel} 不存在，跳过")


def sync_append(append_items, medgeclaw_dir: Path, workspace: Path):
    """追加内容到现有文件（幂等，按 marker 判重）"""
    print("📋 追加内容...")
    for item in append_items:
        src = medgeclaw_dir / item["source"]
        dst = workspace / item["target"]
        marker = item["marker"]

        if not src.exists():
            print(f"   ⏭️  {item['source']} 不存在，跳过")
            continue

        with open(src) as f:
            content = f.read()

        if dst.exists():
            with open(dst) as f:
                existing = f.read()
            if marker in existing:
                print(f"   ⏭️  {item['target']} 已包含 '{marker}'，跳过")
                continue

        with open(dst, "a") as f:
            f.write("\n" + content)
        print(f"   ✅ {item['target']} 已追加")


def sync_config(config_items, medgeclaw_dir: Path, openclaw_dir: Path):
    """修改 OpenClaw 配置"""
    print("📦 更新配置...")
    config_path = openclaw_dir / "openclaw.json"

    with open(config_path) as f:
        config = json.load(f)

    skill_dirs = []
    
    for item in config_items:
        if item["action"] == "add_skill_dir":
            skill_dir = str(medgeclaw_dir / item["value"])
            skill_dirs.append(skill_dir)

        elif item["action"] == "set_model_limits":
            context_window = item.get("contextWindow")
            max_tokens = item.get("maxTokens")

            providers = config.get("models", {}).get("providers", {})
            updated = 0
            for provider_data in providers.values():
                for model in provider_data.get("models", []):
                    if context_window:
                        model["contextWindow"] = context_window
                    if max_tokens:
                        model["maxTokens"] = max_tokens
                    updated += 1

            if updated:
                print(f"   ✅ 已更新 {updated} 个模型: contextWindow={context_window}, maxTokens={max_tokens}")
            else:
                print("   ⚠️  未找到模型配置，跳过 set_model_limits")

    # 统一处理 skill_dirs
    if skill_dirs:
        extra_dirs = (
            config.setdefault("skills", {})
            .setdefault("load", {})
            .setdefault("extraDirs", [])
        )
        # 清理旧的 MedgeClaw 相关路径
        extra_dirs = [
            d for d in extra_dirs
            if "MedgeClaw" not in d and "medgeclaw" not in d.lower()
        ]
        extra_dirs.extend(skill_dirs)
        config["skills"]["load"]["extraDirs"] = extra_dirs
        print(f"   ✅ skills.load.extraDirs 已更新 ({len(skill_dirs)} 个路径)")

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def generate_workspace_docs(medgeclaw_dir: Path, workspace: Path):
    """生成注入了实际路径的 workspace 文档（MEDGECLAW.md, IDENTITY.md）
    
    模板文件使用 {{MEDGECLAW_ROOT}} 占位符，此函数替换为实际路径。
    """
    placeholders = {
        "{{MEDGECLAW_ROOT}}": str(medgeclaw_dir),
    }

    for doc in ["MEDGECLAW.md", "IDENTITY.md"]:
        src = workspace / doc
        if not src.exists():
            continue
        with open(src) as f:
            content = f.read()
        for placeholder, value in placeholders.items():
            content = content.replace(placeholder, value)
        with open(src, "w") as f:
            f.write(content)


def main():
    medgeclaw_dir = Path(__file__).parent.resolve()
    remind_mode = "--remind" in sys.argv

    # 加载 .env
    load_env(medgeclaw_dir)

    # 解析路径
    openclaw_dir, workspace, config_path = resolve_paths(medgeclaw_dir)

    if remind_mode:
        print("🧬 MedgeClaw Quick Remind")
    else:
        print("🧬 MedgeClaw Sync")
        print(f"   MedgeClaw: {medgeclaw_dir}")
        print(f"   OpenClaw:  {openclaw_dir}\n")

    # 加载同步配置
    config = load_sync_config(medgeclaw_dir)

    # 执行同步
    if "docs" in config:
        sync_docs(config["docs"], medgeclaw_dir, workspace)
    if "skills" in config:
        sync_skills(config["skills"], medgeclaw_dir, workspace)
    if "append" in config:
        sync_append(config["append"], medgeclaw_dir, workspace)
    if "config" in config:
        sync_config(config["config"], medgeclaw_dir, openclaw_dir)

    # 替换模板占位符
    generate_workspace_docs(medgeclaw_dir, workspace)

    # 清理 BOOTSTRAP.md
    bootstrap = workspace / "BOOTSTRAP.md"
    if bootstrap.exists():
        bootstrap.unlink()
        print("🗑️  已删除 BOOTSTRAP.md")

    if remind_mode:
        print("\n💬 发送提醒消息...")
        try:
            subprocess.run(
                ["openclaw", "system", "event", "--text",
                 "🧬 MedgeClaw 提醒: 你是 MedgeClaw，生物医药 AI 研究助手。详细配置见 MEDGECLAW.md 和 CLAUDE.md。遇到科研任务请参考 K-Dense Scientific Skills。",
                 "--mode", "now"],
                check=False, capture_output=True
            )
            print("✅ Done.")
        except Exception:
            print("⚠️  openclaw 命令未找到，跳过提醒")
    else:
        print("\n✅ 同步完成！重启 gateway: openclaw gateway restart")


if __name__ == "__main__":
    main()
