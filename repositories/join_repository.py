from database.db import get_connection

class JoinRepository:

    def get_recommended_pubs(
        self,
        match_id
    ):

        conn = get_connection()

        result = conn.execute("""
        SELECT

            P.pub_name,
            P.address,
            P.main_league,
            P.pub_image_path,

            H.team_name AS home_team,
            A.team_name AS away_team

        FROM Match M

        INNER JOIN Football_Club H
        ON M.home_team_id = H.club_id

        INNER JOIN Football_Club A
        ON M.away_team_id = A.club_id

        INNER JOIN Soccer_Pub P
        ON P.main_league = H.league

        WHERE M.match_id = ?
        """,
        (match_id,)
        ).fetchdf()

        conn.close()

        return result.to_dict("records")