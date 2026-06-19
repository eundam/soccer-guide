from database.db import get_connection

class JoinRepository:

    def get_recommended_pubs(
        self,
        match_id
    ):

        conn = get_connection()

        # 펍이 응원하는 구단(support_team_id)이
        # 해당 경기의 홈팀 또는 원정팀이면 추천한다.
        result = conn.execute("""
        SELECT

            P.pub_name,
            P.address,
            P.main_league,
            P.pub_image_path,

            H.team_name AS home_team,
            A.team_name AS away_team,
            S.team_name AS support_team

        FROM Match M

        INNER JOIN Football_Club H
        ON M.home_team_id = H.club_id

        INNER JOIN Football_Club A
        ON M.away_team_id = A.club_id

        INNER JOIN Soccer_Pub P
        ON P.support_team_id = M.home_team_id
        OR P.support_team_id = M.away_team_id

        INNER JOIN Football_Club S
        ON P.support_team_id = S.club_id

        WHERE M.match_id = ?
        """,
        (match_id,)
        ).fetchdf()

        conn.close()

        return result.to_dict("records")