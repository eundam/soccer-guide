from database.db import get_connection

class ClubRepository:

    def select_all_clubs(self):

        conn = get_connection()

        result = conn.execute("""
            SELECT *
            FROM Football_Club
        """).fetchdf()

        conn.close()

        return result.to_dict("records")
    
    def search_club(self, keyword):

        conn = get_connection()

        result = conn.execute(
            """
            SELECT *
            FROM Football_Club
            WHERE team_name ILIKE ?
            """,
            (f"%{keyword}%",)
        ).fetchdf()

        conn.close()

        return result.to_dict("records")