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
        pub_image_path
    ):

        conn = get_connection()

        next_id = conn.execute("""
            SELECT COALESCE(MAX(pub_id),0)+1
            FROM Soccer_Pub
        """).fetchone()[0]

        conn.execute("""
            INSERT INTO Soccer_Pub
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            next_id,
            pub_name,
            address,
            main_league,
            pub_image_path
        ))

        conn.close()

    # 수정(Update)
    def update_pub(
        self,
        pub_id,
        address,
        main_league
    ):

        conn = get_connection()

        conn.execute("""
            UPDATE Soccer_Pub
            SET address = ?,
                main_league = ?
            WHERE pub_id = ?
        """,
        (
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