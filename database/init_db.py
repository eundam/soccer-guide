from db import get_conn

conn = get_conn()

conn.execute("""
CREATE TABLE IF NOT EXISTS Football_Club(
club_id INTEGER PRIMARY KEY,
team_name VARCHAR,
league VARCHAR,
manager VARCHAR,
logo_path VARCHAR
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS Match(
match_id INTEGER PRIMARY KEY,
home_team_id INTEGER,
away_team_id INTEGER,
match_time TIMESTAMP,
broadcast_platform VARCHAR,
platform_logo_path VARCHAR
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS Soccer_Pub(
pub_id INTEGER PRIMARY KEY,
pub_name VARCHAR,
address VARCHAR,
main_league VARCHAR,
pub_image_path VARCHAR
)
""")

conn.execute("""
INSERT OR REPLACE INTO Football_Club
VALUES
(1,'Arsenal','EPL','Arteta','assets/clubs/arsenal.png'),
(2,'Liverpool','EPL','Slot','assets/clubs/liverpool.png'),
(3,'Barcelona','LaLiga','Flick','assets/clubs/barcelona.png')
""")

conn.execute("""
INSERT OR REPLACE INTO Match
VALUES
(1,1,2,'2026-06-15 22:00:00','쿠팡플레이',''),
(2,3,1,'2026-06-18 20:00:00','SPOTV','')
""")

conn.execute("""
INSERT OR REPLACE INTO Soccer_Pub
VALUES
(1,'Kings Pub',
'서울 강남구',
'EPL',
'assets/pubs/왕스펍.jpg'),

(2,'Joy Pub',
'서울 마포구',
'LaLiga',
'assets/pubs/조이펍.jpg')
""")

conn.close()

print("DB 초기화 완료")