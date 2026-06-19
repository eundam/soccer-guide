# ⚽ 해외 축구(EPL) 시청 가이드 및 축구 펍 지도 안내 시스템

> 데이터베이스 Term Project — 컴퓨터공학과 정은담 (2025115347)

프리미어리그(EPL) 경기 일정과 중계 플랫폼 정보를 확인하고, 내가 응원하는 팀의 경기를 함께 볼 수 있는 **축구 펍을 추천**해 주는 데스크톱 GUI 애플리케이션입니다. `Python` + `Flet` + `DuckDB`로 구현했습니다.

---

## 📌 주요 기능

| 기능 | 설명 |
|------|------|
| 구단 목록 조회 | 2025-26 시즌 EPL 20개 구단의 로고·리그·감독 정보를 카드로 표시 |
| 구단 검색 | 구단 이름(영문 일부)으로 검색 (대소문자 무시) |
| 경기 일정 | 홈/원정팀, 경기 시각, 중계 플랫폼 확인 |
| 펍 추천 | 선택한 경기에 출전하는 구단을 응원하는 펍을 JOIN으로 매칭 추천 |
| 펍 관리 | 펍 등록·수정·삭제 (별도 다이얼로그) |

---

## 🗂️ 데이터베이스 구조

3개의 테이블(Entity 2 + Relationship 1)로 구성되며 BCNF 수준으로 정규화했습니다.

- **Football_Club** — 구단 마스터 (구단명, 리그, 감독, 로고 경로)
- **Match** — 경기 일정 (홈/원정 팀을 `Football_Club`의 외래키로 참조)
- **Soccer_Pub** — 펍 정보 (응원 구단 `support_team_id`로 경기와 매칭)


---

## 🏗️ 프로젝트 구조

```
soccer-guide/
├── main.py                      # Flet GUI 진입점
├── database/
│   ├── db.py                    # DuckDB 연결
│   └── init_db.py               # 테이블 생성 + 초기 데이터 삽입
├── services/                    # 비즈니스 로직 계층
│   ├── club_service.py
│   ├── match_service.py
│   └── pub_service.py
├── repositories/                # DB 접근 계층
│   ├── club_repository.py
│   ├── match_repository.py
│   ├── pub_repository.py
│   └── join_repository.py       # 펍 추천 JOIN
├── assets/
│   ├── clubs/                   # 구단 로고 이미지
│   └── pubs/                    # 펍 매장 사진
├── soccer_guide.erd             # ERD 
└── pyproject.toml
└──soccer_guide.db
```

계층 구조: User → Flet(UI) → Service → Repository → DuckDB

---

## 🚀 실행 방법

### 1. 의존성 설치
```bash
uv sync
# 또는
pip install duckdb flet pandas
```

### 2. 데이터베이스 초기화
```bash
python database/init_db.py
```
> 실행 위치와 무관하게 프로젝트 루트에 `soccer_guide.db`가 생성됩니다.

### 3. 애플리케이션 실행
```bash
uv run python main.py
```

---

## 🛠️ 기술 스택

- **Python** 3.13
- **Flet** 0.85 — 파이썬 기반 GUI 프레임워크
- **DuckDB** 1.5 — 파일 기반 내장형 관계형 데이터베이스
- **pandas** — 조회 결과 처리

---

## 📖 데이터 출처 안내

- 구단 정보(팀명·감독)는 2025-26 시즌 EPL 기준 실제 데이터입니다.
- 펍의 상호·주소는 실제 존재하는 국내 축구 펍 정보를 사용했으며, 응원 구단(`support_team_id`) 매핑은 추천 기능 시연을 위한 설정값입니다.