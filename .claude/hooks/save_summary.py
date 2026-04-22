#!/usr/bin/env python3
"""
Stop hook: salva resumo da sessão em .claude/memory/sessions/
Requer: ANTHROPIC_API_KEY no ambiente para resumo automático.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def read_transcript(transcript_path: str) -> list[dict]:
    events = []
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except (FileNotFoundError, OSError):
        pass
    return events


def extract_text(events: list[dict]) -> str:
    parts = []
    for event in events:
        role = event.get("role", "")
        content = event.get("content", "")
        if isinstance(content, str) and content.strip():
            parts.append(f"{role.capitalize()}: {content[:600]}")
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "").strip()
                    if text:
                        parts.append(f"{role.capitalize()}: {text[:600]}")
    return "\n".join(parts[-60:])


def summarize(transcript_text: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": (
                    "Resumo conciso desta sessão Claude Code em português. "
                    "Foque em: decisões tomadas, tarefas concluídas, agentes envolvidos, próximos passos. "
                    "Máximo 200 palavras.\n\n"
                    f"TRANSCRIPT:\n{transcript_text}"
                ),
            }],
        )
        return response.content[0].text
    except ImportError:
        return (
            "Resumo automático indisponível — instale `anthropic` (`uv add anthropic`).\n\n"
            "Últimas interações:\n" + "\n".join(transcript_text.split("\n")[-10:])
        )
    except Exception as e:
        return f"Erro ao gerar resumo: {e}"


def main() -> int:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return 0

    transcript_path = data.get("transcript_path", "")
    session_id = data.get("session_id", "unknown")

    if not transcript_path:
        return 0

    events = read_transcript(transcript_path)
    if not events:
        return 0

    text = extract_text(events)
    if not text.strip():
        return 0

    summary = summarize(text)

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    sessions_dir = project_dir / ".claude" / "memory" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    out = sessions_dir / f"{timestamp}_{session_id[:8]}.md"
    out.write_text(
        f"# Sessão {timestamp}\n\n"
        f"**Session ID:** `{session_id}`\n\n"
        f"## Resumo\n\n{summary}\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
