import re

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

    def _extract_player_row(self, row):
        player = player_object.Player(row)
        # Assume row is tr.even or tr.odd from player table with the following cells
        # Name	Yr	Ht	Pos	[spacer] Gms Min FG	FG%	3P	3P%	FT	FT%	OR	DR	TR	Ast	Stl	Blk	TO	PF	+/-	Pts
        cells = row.find_all('td')

        # Extract data from cells (TDs) and populate the player object.
        player.id = self._get_player_id(cells[0])
        player.name = self._get_player_name(cells[0])
        player.year = cells[1].contents[0]
        player.height = cells[2].contents[0]
        player.position = cells[3].contents[0]
        # Column 4 is a spacer column.
        player.games = cells[5]
        player.min = cells[6].contents[0]
        player.fg = cells[7].contents[0]
        player.fg_pct = cells[8].contents[0]
        player.three_p = self.get_content(cells, 9)
        player.offense_rating = self.get_content(cells, 10)
        player.defense_rating = self.get_content(cells, 11)
        player.tr = self.get_content(cells, 12)
        player.ast = self.get_content(cells, 13)
        player.stl = self.get_content(cells, 14)
        player.blk = self.get_content(cells, 15)
        player.to = self.get_content(cells, 16)
        player.pf = self.get_content(cells, 17)
        player.plus_minus = self.get_content(cells, 18)
        player.pts = self.get_content(cells, 19)

        return player

    def get_content(self, cells, index):
        cell = cells[index]
        value = cell.content[0] if cell is None else ''
        return value

    def _get_player_name(self, name_td):
        # <a href="player?pid=p9DE5067489" class="player">Joseph Piccione</a>
        return name_td.find('a').text

    def _get_player_id(self, name_td):
        # <a href="player?pid=p9DE5067489" class="player">Joseph Piccione</a>
        href = name_td.find('a')['href']
        # href should be 'player?pid=p9DE5067489'
        # use regular expression to match part after equals sign.
        matches = re.search(r'pid=(p\w+)', href)
        # if a match is found return value otherwise return -1
        return matches.group(1) if matches else -1
