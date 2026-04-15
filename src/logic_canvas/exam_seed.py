from __future__ import annotations

from typing import List, Tuple

from logic_canvas.db import get_connection, init_db


EXAM_TOPICS: List[Tuple[str, str, str, str, None, None, int]] = [
    ("pattern", "sw_design", "Singleton", "객체 인스턴스를 하나만 생성해 전역에서 동일한 접근점을 제공하는 생성 패턴.", None, None, 0),
    ("pattern", "sw_design", "Observer", "한 객체의 상태 변화가 여러 구독 객체에 자동 전파되도록 만드는 행위 패턴.", None, None, 0),
    ("pattern", "sw_design", "Factory Method", "객체 생성 책임을 서브클래스로 분리해 생성 로직의 결합도를 낮추는 패턴.", None, None, 0),
    ("cs", "sw_design", "결합도(Coupling)", "모듈 간 상호 의존 정도를 뜻하며 낮을수록 유지보수성과 재사용성이 높다.", None, None, 0),
    ("cs", "sw_design", "응집도(Cohesion)", "모듈 내부 요소들이 하나의 책임에 얼마나 밀접하게 관련되는지를 뜻하며 높을수록 좋다.", None, None, 0),
    ("cs", "database", "정규화(1NF~3NF)", "데이터 중복을 줄이고 이상 현상을 방지하기 위해 테이블을 구조적으로 분해하는 과정.", None, None, 0),
    ("cs", "database", "이상 현상(Anomaly)", "삽입, 삭제, 갱신 과정에서 데이터 중복 때문에 발생하는 비정상 동작을 말한다.", None, None, 0),
    ("cs", "database", "트랜잭션", "하나의 논리적 작업 단위로 모두 성공하거나 모두 실패해야 하는 데이터 처리 묶음이다.", None, None, 0),
    ("cs", "database", "ACID", "트랜잭션의 핵심 특성으로 원자성, 일관성, 격리성, 영속성을 의미한다.", None, None, 0),
    ("cs", "database", "인덱스(Index)", "검색 속도를 높이기 위해 사용하는 자료구조로 조회 성능 향상 대신 쓰기 비용이 늘 수 있다.", None, None, 0),
    ("cs", "operating_system", "프로세스와 스레드", "프로세스는 실행 중인 프로그램 단위이고 스레드는 프로세스 내부 실행 흐름 단위다.", None, None, 0),
    ("cs", "operating_system", "스케줄링", "CPU를 어떤 프로세스에 어떤 순서로 배분할지 결정하는 운영체제 정책이다.", None, None, 0),
    ("cs", "operating_system", "교착상태 4조건", "상호 배제, 점유와 대기, 비선점, 환형 대기 네 조건이 모두 만족될 때 교착상태가 발생한다.", None, None, 0),
    ("cs", "operating_system", "가상 메모리", "보조기억장치를 활용해 실제 메모리보다 큰 주소 공간을 제공하는 메모리 관리 기법이다.", None, None, 0),
    ("algorithm", "operating_system", "페이지 교체 알고리즘", "메모리 부족 시 어떤 페이지를 제거할지 결정하며 FIFO, LRU 등이 대표적이다.", None, None, 0),
    ("cs", "network", "OSI 7계층", "네트워크 통신 기능을 7개 계층으로 나눈 참조 모델로 계층별 역할 분리가 핵심이다.", None, None, 0),
    ("cs", "network", "TCP/IP 4계층", "인터넷에서 실제로 널리 사용하는 계층 모델로 네트워크 접근, 인터넷, 전송, 응용 계층으로 구성된다.", None, None, 0),
    ("cs", "network", "IP 주소와 서브넷 마스크", "네트워크 주소와 호스트 주소를 구분해 같은 네트워크 범위를 판별하는 기준이다.", None, None, 0),
    ("cs", "network", "TCP 3-Way Handshake", "클라이언트와 서버가 연결 수립 전에 SYN, SYN+ACK, ACK를 주고받는 절차다.", None, None, 0),
    ("cs", "network", "라우팅(Routing)", "패킷이 목적지까지 가는 최적 경로를 선택하고 전달하는 과정이다.", None, None, 0),
    ("cs", "security", "대칭키 / 비대칭키 암호화", "대칭키는 같은 키로 암복호화하고 비대칭키는 공개키와 개인키를 분리해 사용한다.", None, None, 0),
    ("cs", "security", "해시(Hash)", "임의 길이 데이터를 고정 길이 값으로 변환하며 무결성 검증과 비밀번호 저장에 활용된다.", None, None, 0),
    ("cs", "security", "접근 제어", "사용자나 프로세스가 자원에 접근할 수 있는 권한을 식별, 인증, 인가로 관리하는 개념이다.", None, None, 0),
    ("cs", "security", "SQL Injection", "입력값 검증 미흡을 악용해 악성 SQL을 주입하고 데이터베이스를 조작하는 공격 기법이다.", None, None, 0),
    ("cs", "security", "서비스 거부 공격 (DoS/DDoS)", "과도한 요청으로 시스템 자원을 고갈시켜 정상 서비스 제공을 방해하는 공격이다.", None, None, 0),
]


def seed_exam_topics() -> int:
    init_db()
    with get_connection() as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO knowledge_items (
                category,
                subject,
                title,
                summary,
                code_snippet,
                code_language,
                needs_review
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            EXAM_TOPICS,
        )
        return connection.total_changes
