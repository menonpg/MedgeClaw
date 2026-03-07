# OpenClaw Integration

MedgeClaw runs on top of [OpenClaw](https://github.com/openclaw/openclaw). This guide explains how to inject MedgeClaw's identity, skills, and project context into an OpenClaw instance.

## Quick Start

```bash
cd /path/to/MedgeClaw
python3 sync.py
openclaw gateway restart
```

## What `sync.py` Does

1. **Skills path** — Adds `MedgeClaw/skills/` to `openclaw.json` → `skills.load.extraDirs`

2. **Model limits** — Sets `contextWindow` and `maxTokens` for all configured models

3. **MEDGECLAW.md** — Syncs project context to OpenClaw workspace (`~/.openclaw/workspace/MEDGECLAW.md`)

4. **IDENTITY.md** — Updates agent identity to "MedgeClaw 🧬🦀"

5. **SOUL.md** — Appends MedgeClaw personality section (consult K-Dense skills, Chinese labels, rigorous stats)

6. **AGENTS.md** — Adds instruction to read `MEDGECLAW.md` on session startup

All sync behavior is controlled by `.medgeclaw-sync.yml`. Edit that file to customize what gets synced.

## Quick Remind

If OpenClaw loses context or you want to send a reminder message:

```bash
python3 sync.py --remind
```

This syncs configuration and sends a system event to remind the agent of its MedgeClaw identity.

## Manual Configuration

If you prefer not to use the sync script, add this to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/MedgeClaw/skills"]
    }
  },
  "models": {
    "providers": {
      "your-provider": {
        "models": [{
          "contextWindow": 200000,
          "maxTokens": 320000
        }]
      }
    }
  }
}
```

Then manually copy project docs to `~/.openclaw/workspace/`.
