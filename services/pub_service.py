from repositories.pub_repository import PubRepository
from repositories.join_repository import JoinRepository

class PubService:

    def __init__(self):

        self.pub_repo = PubRepository()
        self.join_repo = JoinRepository()

    def get_all_pubs(self):

        return self.pub_repo.select_all_pubs()

    def add_pub(
        self,
        pub_name,
        address,
        league,
        image_path
    ):

        self.pub_repo.insert_pub(
            pub_name,
            address,
            league,
            image_path
        )

    def update_pub(
        self,
        pub_id,
        address,
        league
    ):

        self.pub_repo.update_pub(
            pub_id,
            address,
            league
        )

    def delete_pub(
        self,
        pub_id
    ):

        self.pub_repo.delete_pub(pub_id)

    def recommend_pubs(
        self,
        match_id
    ):

        return self.join_repo.get_recommended_pubs(
            match_id
        )