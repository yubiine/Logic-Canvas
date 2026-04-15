from __future__ import annotations

import json
import shlex
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from logic_canvas.db import init_db
from logic_canvas.repository import get_item, list_items


app = FastAPI(title="Logic Canvas Web")


def _category_label(category: str) -> str:
    labels = {
        "algorithm": "Algorithm",
        "pattern": "Pattern",
        "cs": "CS",
    }
    return labels.get(category, category.title())


def _subject_label(subject: str) -> str:
    labels = {
        "sw_design": "SW 설계",
        "database": "데이터베이스",
        "operating_system": "운영체제",
        "network": "네트워크",
        "security": "보안",
    }
    return labels.get(subject, "미분류")


def _build_copy_command(item) -> str:
    return "logic add --subject {subject} -c {category} -t {title} -s {summary}".format(
        subject=shlex.quote(item.subject.value) if item.subject else "sw_design",
        category=shlex.quote(item.category.value),
        title=shlex.quote(item.title),
        summary=shlex.quote(item.summary),
    )


def _serialize_item(item) -> Dict[str, object]:
    subject = item.subject.value if item.subject else "uncategorized"
    return {
        "id": item.id,
        "category": item.category.value,
        "category_label": _category_label(item.category.value),
        "subject": subject,
        "subject_label": _subject_label(subject),
        "title": item.title,
        "summary": item.summary,
        "code_snippet": item.code_snippet or "",
        "code_language": item.code_language.value if item.code_language else "text",
        "needs_review": item.needs_review,
        "copy_command": _build_copy_command(item),
    }


def _build_page(items: List[Dict[str, object]]) -> str:
    serialized_items = json.dumps(items, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Logic Canvas</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #07111f;
      --panel: rgba(9, 17, 29, 0.82);
      --panel-strong: rgba(13, 24, 40, 0.95);
      --line: rgba(137, 168, 208, 0.16);
      --line-strong: rgba(129, 170, 255, 0.3);
      --text: #edf3ff;
      --muted: #93a6c3;
      --code-bg: #020814;
      --code-line: rgba(255, 255, 255, 0.06);
      --shadow: 0 24px 80px rgba(0, 0, 0, 0.42);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(79, 209, 197, 0.14), transparent 24rem),
        radial-gradient(circle at top right, rgba(139, 92, 246, 0.18), transparent 26rem),
        linear-gradient(180deg, #0a1628 0%, #08111e 58%, #050b14 100%);
    }

    .shell {
      width: min(1260px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 38px 0 64px;
    }

    .hero {
      padding: 32px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: linear-gradient(135deg, rgba(22, 33, 52, 0.92), rgba(7, 15, 27, 0.92));
      box-shadow: var(--shadow);
    }

    .eyebrow {
      margin: 0 0 12px;
      color: #8fb3ff;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.2em;
      text-transform: uppercase;
    }

    h1 {
      margin: 0;
      font-size: clamp(2.3rem, 5vw, 4.8rem);
      line-height: 0.92;
      letter-spacing: -0.04em;
    }

    .subcopy {
      max-width: 56rem;
      margin: 16px 0 0;
      color: var(--muted);
      line-height: 1.75;
    }

    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 22px;
    }

    .meta-pill,
    .filter-chip {
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.04);
      color: #c7d6ef;
      font-size: 0.9rem;
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 16px;
      align-items: end;
      margin: 28px 0 18px;
    }

    .toolbar h2 {
      margin: 0;
      font-size: 1.06rem;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .toolbar p {
      margin: 8px 0 0;
      color: var(--muted);
    }

    .filters {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .filter-chip {
      cursor: pointer;
      transition: transform 160ms ease, border-color 160ms ease, background-color 160ms ease;
    }

    .filter-chip:hover {
      transform: translateY(-1px);
      border-color: var(--line-strong);
    }

    .filter-chip.active {
      background: rgba(129, 170, 255, 0.16);
      border-color: rgba(129, 170, 255, 0.45);
      color: #eef4ff;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      align-items: start;
    }

    .card {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(180deg, rgba(13, 24, 40, 0.96), rgba(7, 15, 27, 0.96));
      box-shadow: var(--shadow);
      transition: transform 180ms ease, border-color 180ms ease;
    }

    .card:hover {
      transform: translateY(-3px);
      border-color: var(--line-strong);
    }

    .card::before {
      content: "";
      position: absolute;
      inset: 0 0 auto;
      height: 3px;
      background: linear-gradient(90deg, transparent, var(--badge), transparent);
      opacity: 0.9;
    }

    .card-header {
      display: grid;
      gap: 14px;
      width: 100%;
      padding: 22px 22px 18px;
      border: 0;
      background: transparent;
      color: inherit;
      text-align: left;
      cursor: pointer;
    }

    .card-topline,
    .card-subject {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
    }

    .badge,
    .subject-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(255, 255, 255, 0.05);
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .badge {
      color: var(--badge);
    }

    .badge::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: currentColor;
      box-shadow: 0 0 14px currentColor;
    }

    .subject-pill {
      color: #c8d6ef;
      text-transform: none;
      letter-spacing: 0.02em;
    }

    .state {
      color: var(--muted);
      font-size: 0.82rem;
      white-space: nowrap;
    }

    .card-title {
      margin: 0;
      font-size: 1.32rem;
      font-weight: 800;
      line-height: 1.16;
      letter-spacing: -0.03em;
    }

    .card-preview {
      margin: 0;
      color: var(--muted);
      font-size: 0.96rem;
      line-height: 1.65;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .chevron {
      justify-self: end;
      width: 2.2rem;
      height: 2.2rem;
      border-radius: 999px;
      display: grid;
      place-items: center;
      color: #bbcae5;
      background: rgba(255, 255, 255, 0.05);
      transition: transform 240ms ease, background-color 240ms ease;
    }

    .card.is-open .chevron {
      transform: rotate(180deg);
      background: rgba(255, 255, 255, 0.1);
    }

    .card-body {
      max-height: 0;
      overflow: hidden;
      opacity: 0;
      transition: max-height 320ms ease, opacity 220ms ease, padding 220ms ease;
      padding: 0 22px;
    }

    .card.is-open .card-body {
      max-height: 960px;
      opacity: 1;
      padding: 0 22px 22px;
    }

    .body-divider {
      height: 1px;
      margin-bottom: 18px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.14), transparent);
    }

    .body-copy {
      margin: 0 0 18px;
      color: #d7e4fb;
      font-size: 0.97rem;
      line-height: 1.8;
      white-space: pre-wrap;
    }

    .code-panel {
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 18px;
      background: var(--code-bg);
    }

    .code-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 14px;
      border-bottom: 1px solid var(--code-line);
      color: #9fb4d2;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    pre {
      margin: 0;
      padding: 16px;
      overflow-x: auto;
      color: #e9f1ff;
      font-family: "SFMono-Regular", "Menlo", monospace;
      font-size: 0.9rem;
      line-height: 1.65;
    }

    .empty-code {
      padding: 18px 16px;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.7;
    }

    .card-actions {
      display: flex;
      justify-content: flex-end;
      margin-top: 16px;
    }

    .copy-button {
      padding: 10px 14px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.05);
      color: #f3f7ff;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      transition: transform 160ms ease, border-color 160ms ease, background-color 160ms ease;
    }

    .copy-button:hover {
      transform: translateY(-1px);
      border-color: rgba(129, 170, 255, 0.35);
      background: rgba(129, 170, 255, 0.12);
    }

    .copy-button.copied {
      color: #07111f;
      background: #4fd1c5;
      border-color: #4fd1c5;
    }

    .empty-state {
      padding: 56px 24px;
      border: 1px dashed var(--line);
      border-radius: 24px;
      background: rgba(255, 255, 255, 0.03);
      color: var(--muted);
      text-align: center;
      line-height: 1.8;
      grid-column: 1 / -1;
    }

    @media (max-width: 700px) {
      .shell {
        width: min(1260px, calc(100vw - 20px));
        padding-top: 20px;
      }

      .hero,
      .card-header,
      .card.is-open .card-body {
        padding-left: 18px;
        padding-right: 18px;
      }

      .card-topline,
      .card-subject,
      .toolbar {
        align-items: start;
        flex-direction: column;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Logic Canvas</p>
      <h1>정보처리기사 인터랙티브 학습 가이드</h1>
      <p class="subcopy">
        SW 설계, 데이터베이스, 운영체제, 네트워크, 보안 핵심 개념을 과목별로 필터링하고,
        카드를 펼쳐 핵심 설명과 코드 메모를 함께 복습하는 정처기 전용 학습 보드다.
      </p>
      <div class="meta-bar">
        <span class="meta-pill" id="item-count"></span>
        <span class="meta-pill" id="visible-count"></span>
        <span class="meta-pill">Accordion Cards</span>
      </div>
    </section>

    <section class="toolbar">
      <div>
        <h2>Exam Subjects</h2>
        <p>과목 버튼을 눌러 필요한 핵심 개념만 빠르게 추려 보세요.</p>
      </div>
      <div class="filters" id="filters"></div>
    </section>

    <section class="grid" id="card-grid"></section>
  </main>

  <script>
    const items = __ITEMS_JSON__;
    const grid = document.getElementById("card-grid");
    const filtersRoot = document.getElementById("filters");
    const itemCount = document.getElementById("item-count");
    const visibleCount = document.getElementById("visible-count");

    const subjectTheme = {
      sw_design: "#ff8a5b",
      database: "#4fd1c5",
      operating_system: "#ffd166",
      network: "#7aa2ff",
      security: "#c084fc"
    };

    const subjectOrder = [
      { key: "all", label: "전체" },
      { key: "sw_design", label: "SW 설계" },
      { key: "database", label: "데이터베이스" },
      { key: "operating_system", label: "운영체제" },
      { key: "network", label: "네트워크" },
      { key: "security", label: "보안" }
    ];

    let selectedSubject = "all";

    itemCount.textContent = items.length + " Items";

    function escapeHtml(value) {
      return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function previewText(value) {
      const text = String(value).trim();
      return text.length <= 118 ? text : text.slice(0, 115) + "...";
    }

    function getFilteredItems() {
      if (selectedSubject === "all") {
        return items;
      }
      return items.filter((item) => item.subject === selectedSubject);
    }

    function renderFilters() {
      filtersRoot.innerHTML = subjectOrder.map((subject) => `
        <button
          type="button"
          class="filter-chip ${subject.key === selectedSubject ? "active" : ""}"
          data-subject="${subject.key}"
        >
          ${subject.label}
        </button>
      `).join("");

      filtersRoot.querySelectorAll(".filter-chip").forEach((button) => {
        button.addEventListener("click", () => {
          selectedSubject = button.dataset.subject || "all";
          renderFilters();
          renderCards();
        });
      });
    }

    function renderCards() {
      const filteredItems = getFilteredItems();
      visibleCount.textContent = filteredItems.length + " Visible";

      if (!filteredItems.length) {
        grid.innerHTML = `
          <div class="empty-state">
            <strong>선택한 과목에 등록된 항목이 없습니다.</strong><br />
            다른 필터를 선택하거나 <code>logic add --subject ...</code>로 항목을 추가해 보세요.
          </div>
        `;
        return;
      }

      grid.innerHTML = filteredItems.map((item) => {
        const badgeColor = subjectTheme[item.subject] || "#8fb3ff";
        const reviewText = item.needs_review ? "Review Pending" : "Reviewed";
        const codeBlock = item.code_snippet
          ? `
            <div class="code-panel">
              <div class="code-head">
                <span>Code Snippet</span>
                <span>${escapeHtml(item.code_language)}</span>
              </div>
              <pre><code>${escapeHtml(item.code_snippet)}</code></pre>
            </div>
          `
          : `
            <div class="code-panel">
              <div class="code-head">
                <span>Code Snippet</span>
                <span>none</span>
              </div>
              <div class="empty-code">저장된 코드 스니펫이 없습니다. 개념 복습용 카드입니다.</div>
            </div>
          `;

        return `
          <article class="card" style="--badge: ${badgeColor};">
            <button class="card-header" type="button" aria-expanded="false">
              <div class="card-topline">
                <span class="badge">${escapeHtml(item.category_label)}</span>
                <span class="state">${reviewText}</span>
              </div>
              <div class="card-subject">
                <span class="subject-pill">${escapeHtml(item.subject_label)}</span>
              </div>
              <h3 class="card-title">${escapeHtml(item.title)}</h3>
              <p class="card-preview">${escapeHtml(previewText(item.summary))}</p>
              <span class="chevron" aria-hidden="true">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
              </span>
            </button>
            <div class="card-body">
              <div class="body-divider"></div>
              <p class="body-copy">${escapeHtml(item.summary)}</p>
              ${codeBlock}
              <div class="card-actions">
                <button class="copy-button" type="button" data-command="${escapeHtml(item.copy_command)}">
                  명령어 복사
                </button>
              </div>
            </div>
          </article>
        `;
      }).join("");

      bindInteractions();
    }

    function bindInteractions() {
      const cards = Array.from(document.querySelectorAll(".card"));

      cards.forEach((card) => {
        const header = card.querySelector(".card-header");
        const copyButton = card.querySelector(".copy-button");

        header.addEventListener("click", () => {
          const isOpen = card.classList.contains("is-open");
          cards.forEach((otherCard) => {
            otherCard.classList.remove("is-open");
            otherCard.querySelector(".card-header").setAttribute("aria-expanded", "false");
          });

          if (!isOpen) {
            card.classList.add("is-open");
            header.setAttribute("aria-expanded", "true");
          }
        });

        copyButton.addEventListener("click", async (event) => {
          event.stopPropagation();
          const command = copyButton.dataset.command || "";

          try {
            await navigator.clipboard.writeText(command);
            copyButton.classList.add("copied");
            copyButton.textContent = "복사 완료";
            window.setTimeout(() => {
              copyButton.classList.remove("copied");
              copyButton.textContent = "명령어 복사";
            }, 1400);
          } catch (error) {
            copyButton.textContent = "복사 실패";
            window.setTimeout(() => {
              copyButton.textContent = "명령어 복사";
            }, 1400);
          }
        });
      });
    }

    renderFilters();
    renderCards();
  </script>
</body>
</html>
""".replace("__ITEMS_JSON__", serialized_items)


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    init_db()
    items = [_serialize_item(item) for item in list_items()]
    return HTMLResponse(_build_page(items))


@app.get("/api/items/{item_id}", response_class=JSONResponse)
def item_detail(item_id: int) -> JSONResponse:
    init_db()
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(_serialize_item(item))
