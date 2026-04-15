# Logic-Canvas

Logic-Canvas는 개발자용 지식 베이스 CLI이자, FastAPI 기반 웹 뷰어다.  
알고리즘, 디자인 패턴, 핵심 CS 지식을 SQLite에 저장하고, 터미널에서는 Rich 출력으로, 웹에서는 인터랙티브 카드 UI로 볼 수 있다.

현재 프로젝트는 특히 정보처리기사 학습 흐름에 맞게 확장되어 있으며, `SW 설계`, `데이터베이스`, `운영체제`, `네트워크`, `보안` 기준 필터와 25개 기본 시드를 제공한다.

## 주요 기능

- Typer 기반 CLI 명령어
- Rich 기반 터미널 표/마크다운 출력
- SQLite 기반 경량 로컬 저장소
- FastAPI 기반 웹 UI
- pyngrok 기반 외부 공개 URL 생성
- 정처기 과목별 필터
- 정처기 핵심 개념 25개 기본 시드

## 기술 스택

- Python 3.9+
- Typer
- Rich
- SQLite
- FastAPI
- Uvicorn
- pyngrok

## 설치

프로젝트 루트에서:

```bash
pip install -e .
```

가상환경을 쓰는 경우:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## 데이터 모델

각 지식 항목은 아래 필드를 가진다.

- `id`
- `category`: `algorithm | pattern | cs`
- `subject`: `sw_design | database | operating_system | network | security`
- `title`
- `summary`
- `code_snippet`
- `code_language`: `python | dart | NULL`
- `needs_review`

`category`는 지식의 성격을 나타낸다.

- `algorithm`: 알고리즘/절차 중심
- `pattern`: 설계 패턴 중심
- `cs`: 개념/이론 중심

`subject`는 학습 과목 축이다.

- `sw_design`: SW 설계
- `database`: 데이터베이스
- `operating_system`: 운영체제
- `network`: 네트워크
- `security`: 보안

## 빠른 시작

```bash
logic init-db
logic seed-exam
logic list --subject sw_design
logic view 1
```

직접 항목을 추가하려면:

```bash
logic add \
  --subject network \
  --category cs \
  --title "OSI 7계층" \
  --summary "네트워크 통신 기능을 7개 계층으로 나눈 참조 모델"
```

코드 스니펫 파일과 함께 추가하려면:

```bash
logic add \
  --subject operating_system \
  --category algorithm \
  --title "LRU" \
  --summary "최근에 가장 적게 사용한 페이지를 교체" \
  --code-file ./examples/lru.py \
  --code-language python
```

## CLI 명령어

### `logic init-db`

SQLite DB와 테이블을 생성한다.

```bash
logic init-db
```

### `logic add`

지식 항목을 추가한다.

```bash
logic add \
  --subject sw_design \
  --category pattern \
  --title "Singleton" \
  --summary "객체를 하나만 생성해 전역에서 공유" \
  --needs-review
```

옵션:

- `--subject`
- `--category`, `-c`
- `--title`, `-t`
- `--summary`, `-s`
- `--code-file`
- `--code-language`
- `--needs-review`

### `logic list`

목록을 조회한다.

```bash
logic list
logic list --subject database
logic list --category pattern
logic list --subject security --category cs
```

### `logic view`

ID 기준으로 상세 항목을 본다.

```bash
logic view 3
```

### `logic seed-exam`

정보처리기사 핵심 개념 25개를 초기 데이터로 넣는다.  
같은 제목과 과목 조합은 중복 삽입되지 않도록 `INSERT OR IGNORE`로 처리된다.

```bash
logic seed-exam
```

### `logic serve`

FastAPI 서버를 띄우고, pyngrok로 외부 공개 URL을 연다.

```bash
logic serve
```

옵션:

- `--host` 기본값 `0.0.0.0`
- `--port` 기본값 `8000`

## 웹 UI

`logic serve`를 실행하면 다음이 순서대로 수행된다.

1. SQLite 초기화
2. ngrok 터널 생성
3. Public URL 출력
4. FastAPI 서버 실행

웹 UI 특징:

- 다크 모드 기반 인터랙티브 카드 그리드
- 과목별 필터 칩
- 카드 아코디언 애니메이션
- 코드 스니펫 표시
- 각 카드의 `명령어 복사` 버튼

복사되는 명령 예시:

```bash
logic add --subject sw_design -c pattern -t 'Singleton' -s '객체 인스턴스를 하나만 생성...'
```

## 정처기 기본 시드 구성

총 25개 항목이 과목별 5개씩 포함된다.

### SW 설계

- Singleton
- Observer
- Factory Method
- 결합도(Coupling)
- 응집도(Cohesion)

### 데이터베이스

- 정규화(1NF~3NF)
- 이상 현상(Anomaly)
- 트랜잭션
- ACID
- 인덱스(Index)

### 운영체제

- 프로세스와 스레드
- 스케줄링
- 교착상태 4조건
- 가상 메모리
- 페이지 교체 알고리즘

### 네트워크

- OSI 7계층
- TCP/IP 4계층
- IP 주소와 서브넷 마스크
- TCP 3-Way Handshake
- 라우팅(Routing)

### 보안

- 대칭키 / 비대칭키 암호화
- 해시(Hash)
- 접근 제어
- SQL Injection
- 서비스 거부 공격 (DoS/DDoS)

## 디렉토리 구조

```text
logic-canvas/
├─ data/
│  └─ logic_canvas.db
├─ scripts/
│  └─ seed_topics.py
├─ sql/
│  └─ schema.sql
├─ src/
│  └─ logic_canvas/
│     ├─ __init__.py
│     ├─ db.py
│     ├─ exam_seed.py
│     ├─ main.py
│     ├─ models.py
│     ├─ renderer.py
│     ├─ repository.py
│     └─ web.py
├─ .gitignore
├─ pyproject.toml
└─ README.md
```

## 개발 메모

- DB 파일은 `data/logic_canvas.db`
- `logic init-db`는 기존 DB에 `subject` 컬럼이 없으면 자동 보강한다
- 웹 UI는 별도 프론트엔드 프레임워크 없이 단일 HTML/CSS/JavaScript 문자열로 렌더링된다
- Python 3.9 호환 문법 기준으로 작성되어 있다

## 실행 예시 요약

```bash
pip install -e .
logic init-db
logic seed-exam
logic list --subject network
logic view 1
logic serve
```
