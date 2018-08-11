import soup_kitchen
import player_object


class TeamPlayerScraper:
    def __init__(self, team_page):
        self.team_soup = soup_kitchen.get_soup(team_page)
        self.team_name = self.get_team_name()

    def get_team_player_data(self):
        players = []
        rows = self._get_team_rows()
        for row in rows:
            player = self._extract_player_row(row)
            players.append(player)

        return players

    def _get_team_rows(self):
        return self.team_soup.select('tr.even, tr.odd')

    def get_team_name(self):
        # name = self.team_soup.find()
        return 'get team name not implemented'
        pass

    @staticmethod
    def _extract_player_row(row):
        return player_object.Player(row)
