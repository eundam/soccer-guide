from repositories.match_repository import MatchRepository

class MatchService:

    def __init__(self):
        self.repo = MatchRepository()

    def get_matches(self):
        return self.repo.select_all_matches()
    def search_match_by_date(self, date):

        return self.repo.search_match_by_date(date)