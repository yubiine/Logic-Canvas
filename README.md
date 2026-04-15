# Logic-Canvas

개발자용 지식 베이스 CLI 도구 초안이다.

## 디렉토리 구조

```text
logic-canvas/
├─ data/
│  └─ logic_canvas.db
├─ sql/
│  └─ schema.sql
├─ src/
│  └─ logic_canvas/
│     ├─ __init__.py
│     ├─ db.py
│     ├─ main.py
│     ├─ models.py
│     ├─ renderer.py
│     └─ repository.py
└─ pyproject.toml
```

## 실행 예시

```bash
pip install -e .
logic init-db
logic seed-exam
logic add --subject sw_design --category pattern --title "Singleton" --summary "객체를 하나만 생성"
logic list --subject network
logic view 1
```
