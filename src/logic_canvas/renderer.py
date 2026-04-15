from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from logic_canvas.models import KnowledgeItem


console = Console()


def render_item_list(items: list[KnowledgeItem]) -> None:
    table = Table(title="Logic Canvas")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Subject", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Title", style="bold")
    table.add_column("Review", style="yellow")

    for item in items:
        table.add_row(
            str(item.id),
            item.subject.value if item.subject else "-",
            item.category.value,
            item.title,
            "Yes" if item.needs_review else "No",
        )

    console.print(table)


def render_item_detail(item: KnowledgeItem) -> None:
    lines = [
        f"# {item.title}",
        "",
        f"- ID: `{item.id}`",
        f"- Subject: `{item.subject.value if item.subject else '-'}`",
        f"- Category: `{item.category.value}`",
        f"- Needs Review: `{'Yes' if item.needs_review else 'No'}`",
        "",
        "## Summary",
        item.summary,
    ]

    if item.code_snippet:
        language = item.code_language.value if item.code_language else "text"
        lines.extend(
            [
                "",
                "## Code Snippet",
                f"```{language}",
                item.code_snippet,
                "```",
            ]
        )

    console.print(Markdown("\n".join(lines)))
