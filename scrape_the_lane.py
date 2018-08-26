import requests

from data_exporter import DataExporter
import team_player_scraper
import pprint
from argparse import ArgumentParser

from player_object import Player

LOGIN_URL = 'http://drivethelane.com/'
TEAM_URL = 'http://drivethelane.com/team-stats?atype=t&gtype=reg&mode=g&tid=t{0}'
# The following URL scrapes the "averages" page rather than the "totals" page.
# TEAM_URL = 'http://drivethelane.com/team-stats?tid=t{0}'

pp = pprint.PrettyPrinter()


def main(args):
    print('-----------------------\nBeginning scrape\n-----------------------')
    session = get_session(args.username, args.password)

    players = []
    team_index = 0
    while team_index < 256:
        team_index += 1

        # Get team content
        team_content = get_page_content(session, build_team_url(team_index))

        scraper = team_player_scraper.TeamPlayerScraper(team_content, team_index)
        team_players = scraper.get_team_player_data()
        players.extend(team_players)

        print('Team Id: {0}'.format(team_index))
        print('Team {0} Players: {1} '.format(team_index, len(team_players)))
        print('Total Players: {0}'.format(len(players)))

    exporter = DataExporter()
    exporter.write_to_csv(Player.RowHeader, players)


def build_team_url(team_id):
    return TEAM_URL.format(team_id)


def get_page_content(session, url):
    page = session.get(url)
    print('Scrape Request: {0} from url: {1}'.format(page.status_code, url))
    return page.content


def login(session, url, username, password):
    payload = {'user': username, 'pass': password, 'login': '1'}
    login_response = session.post(url, data=payload)
    print('Login Request: {0} username: {1}'.format(
        login_response.status_code, username))
    return login_response.content


def get_session(username, password):
    # create a session
    session = requests.session()
    # Login
    login(session, LOGIN_URL, username, password)
    return session


parser = ArgumentParser()
parser.add_argument('-u', '--user', dest='username',
                    help='You need to provide a username')
parser.add_argument('-p', '--pass', dest='password',
                    help='You need to provide a password')
# parser.add_argument('-d', '--debug', dest='debug', default=False)

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
