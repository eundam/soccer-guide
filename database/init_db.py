import os
import duckdb

# 이 파일(database/init_db.py) 기준으로 프로젝트 루트 경로 계산
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "soccer_guide.db")


def get_conn():
    return duckdb.connect(DB_PATH)


conn = get_conn()

# 기존 테이블 삭제 후 재생성 (구조 변경 반영)
conn.execute("DROP TABLE IF EXISTS Match")
conn.execute("DROP TABLE IF EXISTS Soccer_Pub")
conn.execute("DROP TABLE IF EXISTS Football_Club")

conn.execute("""
CREATE TABLE Football_Club(
club_id INTEGER PRIMARY KEY,
team_name VARCHAR,
league VARCHAR,
manager VARCHAR,
logo_path VARCHAR
)
""")

conn.execute("""
CREATE TABLE Match(
match_id INTEGER PRIMARY KEY,
home_team_id INTEGER,
away_team_id INTEGER,
match_time TIMESTAMP,
broadcast_platform VARCHAR,
platform_logo_path VARCHAR
)
""")

# Soccer_Pub: support_team_id 컬럼 추가 (펍이 응원하는 구단)
conn.execute("""
CREATE TABLE Soccer_Pub(
pub_id INTEGER PRIMARY KEY,
pub_name VARCHAR,
address VARCHAR,
main_league VARCHAR,
support_team_id INTEGER,
pub_image_path VARCHAR
)
""")

conn.execute("""
INSERT INTO Football_Club
VALUES
(1,'Arsenal','EPL','Mikel Arteta','assets/clubs/arsenal.png'),
(2,'Aston Villa','EPL','Unai Emery','assets/clubs/aston_villa.png'),
(3,'Bournemouth','EPL','Andoni Iraola','assets/clubs/bournemouth.png'),
(4,'Brentford','EPL','Keith Andrews','assets/clubs/brentford.png'),
(5,'Brighton & Hove Albion','EPL','Fabian Hurzeler','assets/clubs/brighton.png'),
(6,'Burnley','EPL','Scott Parker','assets/clubs/burnley.png'),
(7,'Chelsea','EPL','Enzo Maresca','assets/clubs/chelsea.png'),
(8,'Crystal Palace','EPL','Oliver Glasner','assets/clubs/crystal_palace.png'),
(9,'Everton','EPL','David Moyes','assets/clubs/everton.png'),
(10,'Fulham','EPL','Marco Silva','assets/clubs/fulham.png'),
(11,'Leeds United','EPL','Daniel Farke','assets/clubs/leeds.png'),
(12,'Liverpool','EPL','Arne Slot','assets/clubs/liverpool.png'),
(13,'Manchester City','EPL','Pep Guardiola','assets/clubs/manchester_city.png'),
(14,'Manchester United','EPL','Ruben Amorim','assets/clubs/manchester_united.png'),
(15,'Newcastle United','EPL','Eddie Howe','assets/clubs/newcastle.png'),
(16,'Nottingham Forest','EPL','Nuno Espirito Santo','assets/clubs/nottingham_forest.png'),
(17,'Sunderland','EPL','Regis Le Bris','assets/clubs/sunderland.png'),
(18,'Tottenham Hotspur','EPL','Thomas Frank','assets/clubs/tottenham.png'),
(19,'West Ham United','EPL','Graham Potter','assets/clubs/west_ham.png'),
(20,'Wolverhampton Wanderers','EPL','Vitor Pereira','assets/clubs/wolves.png')
""")

conn.execute("""
INSERT INTO Match
VALUES
(1,12,3,'2025-08-15 04:00:00','쿠팡플레이',''),
(2,1,11,'2025-08-23 23:00:00','쿠팡플레이',''),
(3,13,18,'2025-08-23 20:30:00','쿠팡플레이',''),
(4,7,8,'2025-08-17 22:00:00','쿠팡플레이',''),
(5,14,6,'2025-08-30 23:30:00','쿠팡플레이',''),
(6,15,12,'2025-08-25 04:00:00','쿠팡플레이',''),
(7,2,9,'2025-09-13 21:00:00','쿠팡플레이',''),
(8,17,19,'2025-09-20 23:00:00','쿠팡플레이',''),
(9,5,4,'2025-09-27 19:30:00','쿠팡플레이',''),
(10,20,10,'2025-10-04 23:00:00','쿠팡플레이',''),
(11,16,13,'2025-10-18 23:00:00','쿠팡플레이',''),
(12,18,1,'2025-11-08 22:30:00','쿠팡플레이','')
""")

# 펍마다 응원 구단(support_team_id) 지정
# 컬럼 순서: pub_id, pub_name, address, main_league, support_team_id, pub_image_path
conn.execute("""
INSERT INTO Soccer_Pub
VALUES
-- 실제 존재하는 축구 펍 (이름/주소는 실제 정보, 응원팀 매핑은 데모용 설정)
(1,'리버풀펍 흑석',
'서울 동작구 흑석로 101-10 1층',
'EPL',
12,
'assets/pubs/liverpool_pub.jpg'),

(2,'코키펍 홍대',
'서울 마포구 와우산로21길 19-8 태경빌딩 1층',
'EPL',
1,
'assets/pubs/cocky_pub.jpg'),

(3,'매치볼 하우스',
'서울 도봉구 도봉로 497 덕성빌딩 1층',
'EPL',
14,
'assets/pubs/matchball_house.jpg'),

(4,'오퍼스 신촌',
'서울 서대문구 연세로7길 18 2층',
'EPL',
7,
'assets/pubs/opus.jpg'),

(5,'샘라이언스 이태원',
'서울 용산구 이태원로27가길 50 2층',
'EPL',
13,
'assets/pubs/sam_ryans.jpg'),

(6,'셰익스비어 종각',
'서울 종로구 종로14길 13',
'EPL',
18,
'assets/pubs/shakesbeer.jpg'),

(7,'하이드아웃 삼각지',
'서울 용산구 한강대로 185-1',
'EPL',
15,
'assets/pubs/hideout.jpg'),

(8,'트라이포트 부평',
'인천 부평구 시장로12번길 7',
'EPL',
2,
'assets/pubs/triport.jpg')
""")

conn.close()

print(f"DB 초기화 완료 → {DB_PATH}")