from repositories.club_repository import ClubRepository

class ClubService:

    def __init__(self):
        self.repo = ClubRepository()

    def get_all_clubs(self):
        return self.repo.select_all_clubs()
    
    def search_club(self, keyword):
        return self.repo.search_club(keyword)