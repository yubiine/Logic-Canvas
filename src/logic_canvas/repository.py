from __future__ import annotations

from typing import Optional, Sequence

from logic_canvas.db import get_connection
from logic_canvas.models import Category, CodeLanguage, KnowledgeItem, Subject


def add_item(
    *,
    category: Category,
    subject: Optional[Subject],
    title: str,
    summary: str,
    code_snippet: Optional[str],
    code_language: Optional[CodeLanguage],
    needs_review: bool,
) -> int:
    query = """
        INSERT INTO knowledge_items (
            category,
            subject,
            title,
            summary,
            code_snippet,
            code_language,
            needs_review
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        category.value,
        subject.value if subject else None,
        title,
        summary,
        code_snippet,
        code_language.value if code_language else None,
        int(needs_review),
    )
    with get_connection() as connection:
        cursor = connection.execute(query, values)
        return int(cursor.lastrowid)


def list_items(
    category: Optional[Category] = None,
    subject: Optional[Subject] = None,
) -> Sequence[KnowledgeItem]:
    base_query = """
        SELECT id, category, subject, title, summary, code_snippet, code_language, needs_review
        FROM knowledge_items
    """
    conditions = []
    params = []
    if category:
        conditions.append("category = ?")
        params.append(category.value)
    if subject:
        conditions.append("subject = ?")
        params.append(subject.value)
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    base_query += " ORDER BY id DESC"

    with get_connection() as connection:
        rows = connection.execute(base_query, tuple(params)).fetchall()
    return [_row_to_item(row) for row in rows]


def get_item(item_id: int) -> Optional[KnowledgeItem]:
    query = """
        SELECT id, category, subject, title, summary, code_snippet, code_language, needs_review
        FROM knowledge_items
        WHERE id = ?
    """
    with get_connection() as connection:
        row = connection.execute(query, (item_id,)).fetchone()
    if row is None:
        return None
    return _row_to_item(row)


def _row_to_item(row) -> KnowledgeItem:
    return KnowledgeItem(
        id=row["id"],
        category=Category(row["category"]),
        subject=Subject(row["subject"]) if row["subject"] else None,
        title=row["title"],
        summary=row["summary"],
        code_snippet=row["code_snippet"],
        code_language=CodeLanguage(row["code_language"]) if row["code_language"] else None,
        needs_review=bool(row["needs_review"]),
    )
