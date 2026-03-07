# MedgeClaw 同步机制

## 快速开始

```bash
cd <MedgeClaw项目目录>
python3 sync.py
openclaw gateway restart
```

## 环境配置

首次使用前，复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
# 编辑 .env，设置 MEDGECLAW_ROOT（默认自动检测）
```

## 工作原理

- **配置文件**: `.medgeclaw-sync.yml` 定义同步内容
- **同步脚本**: `sync.py` 读取配置执行同步
- **环境变量**: `.env` 定义路径（可选，默认自动检测）

## 修改同步内容

编辑 `.medgeclaw-sync.yml`，支持：
- `docs`: 文档覆盖写入
- `skills`: 整目录复制
- `append`: 幂等追加（按 marker 判重）
- `config`: OpenClaw JSON 配置修改

无需修改 `sync.py` 或 `medgeclaw-init.sh`。

## 输出路径约束

所有任务输出必须写入：
- 数据分析 → `data/<task_name>/output/`
- Dashboard → `data/<task_name>/dashboard/`
- 科学写作 → `writing_outputs/<date>_<topic>/`

禁止写入项目根目录或 `outputs/`（已废弃）。

详见 `CLAUDE.md` 和 `.gitignore`。
