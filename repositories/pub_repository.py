from database.db import get_connection

class PubRepository:

    # 전체 조회
    def select_all_pubs(self):

        conn = get_connection()

        result = conn.execute("""
            SELECT *
            FROM Soccer_Pub
        """).fetchdf()

        conn.close()

        return result.to_dict("records")

    # 등록(Create)
    def insert_pub(
        self,
        pub_name,
        address,
        main_league,
        support_team_id,
        pub_image_path
    ):

        conn = get_connection()

        next_id = conn.execute("""
            SELECT COALESCE(MAX(pub_id),0)+1
            FROM Soccer_Pub
        """).fetchone()[0]

        conn.execute("""
            INSERT INTO Soccer_Pub
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            next_id,
            pub_name,
            address,
            main_league,
            support_team_id,
            pub_image_path
        ))

        conn.close()

    # 수정(Update)
    def update_pub(
        self,
        pub_id,
        pub_name,
        address,
        main_league
    ):
        # 입력값이 비어 있으면(빈 문자열) 해당 칸은 수정하지 않고
        # 기존 값을 그대로 유지한다.
        # NULLIF(?, '') : 입력이 ''이면 NULL로 바꾸고,
        # COALESCE(NULL, 기존컬럼) : NULL이면 기존 값을 사용한다.

        conn = get_connection()

        conn.execute("""
            UPDATE Soccer_Pub
            SET pub_name    = COALESCE(NULLIF(?, ''), pub_name),
                address     = COALESCE(NULLIF(?, ''), address),
                main_league = COALESCE(NULLIF(?, ''), main_league)
            WHERE pub_id = ?
        """,
        (
            pub_name,
            address,
            main_league,
            pub_id
        ))

        conn.close()

    # 삭제(Delete)
    def delete_pub(self, pub_id):

        conn = get_connection()

        conn.execute("""
            DELETE FROM Soccer_Pub
            WHERE pub_id = ?
        """,
        (pub_id,))

        conn.close()