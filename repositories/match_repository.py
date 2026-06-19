from database.db import get_connection

class MatchRepository:

    def select_all_matches(self):

        conn = get_connection()

        result = conn.execute("""
        SELECT
            m.match_id,
            h.team_name as home_team,
            a.team_name as away_team,
            m.match_time,
            m.broadcast_platform

        FROM Match m

        JOIN Football_Club h
        ON m.home_team_id = h.club_id

        JOIN Football_Club a
        ON m.away_team_id = a.club_id
        """).fetchdf()

        conn.close()

        return result.to_dict("records")
    
    def search_match_by_date(self, date):

        conn = get_connection()

        result = conn.execute(
            """
            SELECT *

            FROM Match

            WHERE CAST(match_time AS DATE)=?
            """,
            (date,)
        ).fetchdf()

        conn.close()

        return result.to_dict("records")