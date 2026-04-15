from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
import uvicorn
from pyngrok import ngrok
from pyngrok.exception import PyngrokError
from rich.panel import Panel
from rich.table import Table

from logic_canvas.db import DB_PATH, init_db
from logic_canvas.exam_seed import EXAM_TOPICS, seed_exam_topics
from logic_canvas.models import Category, CodeLanguage, Subject
from logic_canvas.renderer import console, render_item_detail, render_item_list
from logic_canvas.repository import add_item, get_item, list_items


app = typer.Typer(
    name="logic",
    help="Logic-Canvas: 알고리즘, 패턴, CS 지식을 관리하는 CLI 도구",
    no_args_is_help=True,
)


@app.command("init-db")
def init_db_command() -> None:
    """SQLite DB와 기본 테이블을 생성한다."""
    init_db()
    console.print(f"[green]Database initialized:[/green] {DB_PATH}")


@app.command()
def add(
    subject: Subject = typer.Option(
        ...,
        "--subject",
        help="sw_design | database | operating_system | network | security",
    ),
    category: Category = typer.Option(..., "--category", "-c", help="algorithm | pattern | cs"),
    title: str = typer.Option(..., "--title", "-t", help="지식 항목 제목"),
    summary: str = typer.Option(..., "--summary", "-s", help="핵심 설명"),
    code_file: Optional[Path] = typer.Option(None, "--code-file", help="코드 스니펫 파일 경로"),
    code_language: Optional[CodeLanguage] = typer.Option(
        None, "--code-language", help="python | dart"
    ),
    needs_review: bool = typer.Option(False, "--needs-review", help="복습 필요 여부"),
) -> None:
    """새 지식 항목을 추가한다."""
    init_db()

    code_snippet = None
    if code_file:
        code_snippet = code_file.read_text(encoding="utf-8")
    elif code_language:
        raise typer.BadParameter("--code-language는 --code-file과 함께 사용해야 합니다.")

    item_id = add_item(
        category=category,
        subject=subject,
        title=title,
        summary=summary,
        code_snippet=code_snippet,
        code_language=code_language,
        needs_review=needs_review,
    )
    console.print(f"[green]Created item[/green] with ID [bold]{item_id}[/bold]")


@app.command("list")
def list_command(
    subject: Optional[Subject] = typer.Option(None, "--subject", help="과목 필터"),
    category: Optional[Category] = typer.Option(None, "--category", "-c", help="카테고리 필터"),
) -> None:
    """지식 항목 목록을 조회한다."""
    init_db()
    items = list_items(category=category, subject=subject)
    if not items:
        console.print("[yellow]No knowledge items found.[/yellow]")
        return
    render_item_list(list(items))


@app.command()
def view(item_id: int) -> None:
    """ID로 지식 항목 상세를 조회한다."""
    init_db()
    item = get_item(item_id)
    if item is None:
        console.print(f"[red]Item not found:[/red] {item_id}")
        raise typer.Exit(code=1)
    render_item_detail(item)


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", help="FastAPI 바인딩 호스트"),
    port: int = typer.Option(8000, "--port", help="서버 포트"),
) -> None:
    """ngrok 터널을 열고 FastAPI 웹 서버를 실행한다."""
    init_db()

    try:
        tunnel = ngrok.connect(addr=port, proto="http")
    except PyngrokError as exc:
        console.print(
            Panel.fit(
                f"[bold red]Failed to open ngrok tunnel[/bold red]\n{exc}",
                title="Logic Canvas",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    public_url = tunnel.public_url

    info_table = Table.grid(padding=(0, 2))
    info_table.add_row("Local", f"http://127.0.0.1:{port}")
    info_table.add_row("Public URL", f"[bold cyan]{public_url}[/bold cyan]")
    info_table.add_row("DB", str(DB_PATH))

    console.print(
        Panel.fit(
            info_table,
            title="Logic Canvas Web",
            subtitle="ngrok tunnel active",
            border_style="green",
        )
    )

    try:
        uvicorn.run("logic_canvas.web:app", host=host, port=port, reload=False)
    finally:
        ngrok.disconnect(public_url)
        ngrok.kill()


@app.command("seed-exam")
def seed_exam_command() -> None:
    """정처기 핵심 개념 25개를 초기 데이터로 반영한다."""
    inserted = seed_exam_topics()
    console.print(
        Panel.fit(
            "정처기 핵심 개념 {total}개 세트를 확인했습니다.\n이번 실행에서 반영된 행 수: [bold]{inserted}[/bold]".format(
                total=len(EXAM_TOPICS),
                inserted=inserted,
            ),
            title="Logic Canvas Seed",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    app()
