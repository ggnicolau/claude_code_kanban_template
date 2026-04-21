from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MCP_CONFIG_PATH = ROOT / ".mcp.json"


def run_command(command: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def load_env() -> dict[str, str]:
    env = os.environ.copy()
    if env.get("GH_TOKEN"):
        return env

    if MCP_CONFIG_PATH.exists():
        data = json.loads(MCP_CONFIG_PATH.read_text(encoding="utf-8"))
        auth_header = (
            data.get("mcpServers", {})
            .get("github", {})
            .get("headers", {})
            .get("Authorization", "")
        )
        if auth_header.startswith("Bearer "):
            env["GH_TOKEN"] = auth_header.removeprefix("Bearer ").strip()
    return env


def parse_origin_repo(env: dict[str, str]) -> str:
    origin_url = run_command(["git", "config", "--get", "remote.origin.url"], env)
    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", origin_url)
    if not match:
        raise RuntimeError("Nao foi possivel identificar o repositorio de origem do template.")
    return f"{match.group('owner')}/{match.group('repo')}"


def prompt_text(label: str, default: str | None = None, required: bool = True) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return ""
        print("Valor obrigatorio. Tente novamente.")


def prompt_choice(label: str, options: list[tuple[str, str]], default_key: str) -> str:
    print(label)
    for index, (_, description) in enumerate(options, start=1):
        print(f"{index}. {description}")

    keys = [key for key, _ in options]
    default_index = keys.index(default_key) + 1

    while True:
        raw_value = input(f"Escolha uma opcao [{default_index}]: ").strip()
        if not raw_value:
            return default_key
        if raw_value.isdigit():
            index = int(raw_value) - 1
            if 0 <= index < len(options):
                return options[index][0]
        lowered = raw_value.lower()
        if lowered in keys:
            return lowered
        print("Opcao invalida. Tente novamente.")


def build_repo_name(raw_name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw_name.strip())
    sanitized = re.sub(r"-{2,}", "-", sanitized).strip("-")
    if not sanitized:
        raise ValueError("Nome de repositorio invalido.")
    return sanitized


def maybe_set_secret(
    env: dict[str, str],
    full_name: str,
    secret_name: str,
    secret_value: str,
) -> None:
    process = subprocess.run(
        ["gh", "secret", "set", secret_name, "--repo", full_name],
        cwd=ROOT,
        env=env,
        text=True,
        input=secret_value,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or process.stdout.strip())


def maybe_run_workflow(env: dict[str, str], full_name: str, workflow_name: str) -> str:
    return run_command(
        ["gh", "workflow", "run", workflow_name, "--repo", full_name],
        env,
    )


def find_project(env: dict[str, str], project_title: str) -> str:
    query = (
        "query { viewer { projectsV2(first: 100, orderBy: {field: TITLE, direction: ASC}) "
        "{ nodes { title url closed } } } }"
    )
    output = run_command(["gh", "api", "graphql", "-f", f"query={query}"], env)
    data = json.loads(output)
    for node in data["data"]["viewer"]["projectsV2"]["nodes"]:
        if node["title"] == project_title and not node["closed"]:
            return node["url"]
    return ""


def list_repo_issues(env: dict[str, str], full_name: str) -> list[dict[str, object]]:
    output = run_command(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            full_name,
            "--json",
            "number,title,state",
        ],
        env,
    )
    return json.loads(output)


def summarize_validation(
    env: dict[str, str],
    full_name: str,
    project_title: str,
) -> None:
    project_url = find_project(env, project_title)
    issues = list_repo_issues(env, full_name)

    print("\nValidacao")
    print(f"- Repositorio: https://github.com/{full_name}")
    print(f"- Project: {project_url or 'nao encontrado'}")
    print(f"- Issues abertas: {len(issues)}")
    for issue in issues:
        print(f"  - #{issue['number']} {issue['title']} ({issue['state']})")


def ensure_repo_absent(env: dict[str, str], full_name: str) -> None:
    result = subprocess.run(
        ["gh", "repo", "view", full_name, "--json", "nameWithOwner"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        raise RuntimeError(f"O repositorio {full_name} ja existe.")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wizard para criar um novo repositorio a partir deste template."
    )
    parser.add_argument("--name", help="Nome do novo repositorio.")
    parser.add_argument(
        "--visibility",
        choices=["private", "public"],
        help="Visibilidade do novo repositorio.",
    )
    parser.add_argument("--description", default=None, help="Descricao do repositorio.")
    parser.add_argument(
        "--skip-secret",
        action="store_true",
        help="Nao configura o secret GH_PAT no repositorio novo.",
    )
    parser.add_argument(
        "--skip-workflow",
        action="store_true",
        help="Nao roda a workflow Setup Kanban apos criar o repositorio.",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Nao roda a validacao final.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    env = load_env()
    template_repo = parse_origin_repo(env)
    owner = template_repo.split("/", maxsplit=1)[0]

    print("Wizard de criacao de repositorio")
    print(f"- Template atual: {template_repo}")

    repo_name = build_repo_name(
        args.name or prompt_text("Nome do novo repositorio", required=True)
    )
    visibility = args.visibility or prompt_choice(
        "Visibilidade do repositorio",
        [("private", "Privado"), ("public", "Publico")],
        default_key="private",
    )
    description = (
        args.description
        if args.description is not None
        else prompt_text("Descricao", default="", required=False)
    )

    configure_secret = not args.skip_secret
    run_workflow_now = not args.skip_workflow
    validate_result = not args.skip_validate

    if args.skip_secret is False and args.name is None:
        configure_secret = (
            prompt_choice(
                "Configurar o secret GH_PAT no repo novo?",
                [("yes", "Sim"), ("no", "Nao")],
                default_key="yes",
            )
            == "yes"
        )
    if args.skip_workflow is False and args.name is None:
        run_workflow_now = (
            prompt_choice(
                "Rodar a workflow Setup Kanban agora?",
                [("yes", "Sim"), ("no", "Nao")],
                default_key="yes",
            )
            == "yes"
        )
    if args.skip_validate is False and args.name is None:
        validate_result = (
            prompt_choice(
                "Validar resultado no final?",
                [("yes", "Sim"), ("no", "Nao")],
                default_key="yes",
            )
            == "yes"
        )

    full_name = f"{owner}/{repo_name}"
    project_title = f"{repo_name} Kanban"

    print("\nResumo")
    print(f"- Novo repo: {full_name}")
    print(f"- Visibilidade: {visibility}")
    print(f"- Configurar GH_PAT: {'sim' if configure_secret else 'nao'}")
    print(f"- Rodar Setup Kanban: {'sim' if run_workflow_now else 'nao'}")
    print(f"- Validar ao final: {'sim' if validate_result else 'nao'}")

    if prompt_choice(
        "Deseja continuar?",
        [("yes", "Sim"), ("no", "Nao")],
        default_key="yes",
    ) != "yes":
        print("Operacao cancelada.")
        return 0

    try:
        ensure_repo_absent(env, full_name)

        create_command = [
            "gh",
            "repo",
            "create",
            full_name,
            "--template",
            template_repo,
            f"--{visibility}",
            "--clone=false",
        ]
        if description:
            create_command.extend(["--description", description])

        repo_url = run_command(create_command, env)
        print(f"\nRepositorio criado: {repo_url}")

        if configure_secret:
            gh_token = env.get("GH_TOKEN")
            if not gh_token:
                raise RuntimeError("GH_TOKEN nao encontrado para configurar o secret GH_PAT.")
            maybe_set_secret(env, full_name, "GH_PAT", gh_token)
            print("- Secret GH_PAT configurado.")

        if run_workflow_now:
            workflow_output = maybe_run_workflow(env, full_name, "Setup Kanban")
            print(f"- Workflow disparada: {workflow_output}")
        else:
            print("- Workflow Setup Kanban nao foi executada.")

        if validate_result:
            summarize_validation(env, full_name, project_title)
        else:
            print("- Validacao final pulada.")
    except Exception as exc:  # noqa: BLE001
        print(f"\nErro: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
