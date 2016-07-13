"""
Library for retrieving basektball player-tracking and play-by-play data.
"""

# brew install p7zip

import os
import json
import pandas as pd

os.chdir('/Users/christopherjenness/Desktop/Personal/SportVU/NBA-player-movement')
os.system('mkdir temp')

class Game(object):
    """
    Class for basketball game.  Retrieves play by play and player tracking data.
    """
    
    def __init__(self, date, home_team, away_team):
        """
        Args:
            date (str): 'MM.DD.YYYY', date of game
            home_team (str): 'XXX', abbreviation of home team
            away_team (str): 'XXX', abbreviation of away team
        
        Attributes:
            date (str): 'MM.DD.YYYY', date of game
            home_team (str): 'XXX', abbreviation of home team
            away_team (str): 'XXX', abbreviation of away team
            tracking_id (str): id to access player tracking data
                Due to the way the SportVU data is stored, game_id is 
                complicated: 'MM.DD.YYYY.AWAYTEAM.at.HOMETEAM'
                For Example: 01.13.2016.GSW.at.DEN
            pbp (pd.DataFrame): Play by play data.  33 columns per pbp instance.
            game_id (str): ID for game.  Lukcily, SportVU and play by play use the same game ID
        """
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.tracking_id = '{self.date}.{self.away_team}.at.{self.home_team}'.format(self=self)
        self.tracking_data = None
        self.game_id = None
        self.pbp = None
        self._get_tracking_data()
        self._get_playbyplay_data()
        print('done loading data')
    
    def _get_tracking_data(self):
        """
        Helper function for retrieving tracking data
        """
        # Extract Data into /temp folder
        datalink = "https://raw.githubusercontent.com/neilmj/BasketballData/master/2016.NBA.Raw.SportVU.Game.Logs/{self.tracking_id}.7z".format(self=self)
        os.system("curl " + datalink + " -o " + os.getcwd() + '/temp/zipdata') 
        os.system("7za -o./temp x " + os.getcwd() + '/temp/zipdata') 
        os.remove("./temp/zipdata")
        
        # Extract game ID from extracted file name.
        for file in os.listdir('./temp'):
            if file.endswith('.json'):
                self.game_id = file[:-5]
        
        # Load tracking data
        with open('temp/{self.game_id}.json'.format(self=self)) as data_file:
            self.tracking_data = json.load(data_file) # Load this json
        os.remove('./temp/{self.game_id}.json'.format(self=self))
        return self

    def _get_playbyplay_data(self):
        """
        Helper function for retrieving tracking data
        """
        # stats.nba.com API call
        os.system('curl "http://stats.nba.com/stats/playbyplayv2?'
            'EndPeriod=0&'
            'EndRange=0&'
            'GameID={self.game_id}&'
            'RangeType=0&'
            'Season=2015-16&'
            'SeasonType=Season&'
            'StartPeriod=0&'
            'StartRange=0" > {cwd}/temp/pbp_{self.game_id}.json'.format(cwd=os.getcwd(), self=self))
        
        # load play by play into pandas DataFrame
        with open("{cwd}/temp/pbp_{self.game_id}.json".format(cwd=os.getcwd(), self=self)) as json_file:
            parsed = json.load(json_file)['resultSets'][0]
        os.remove("{cwd}/temp/pbp_{self.game_id}.json".format(cwd=os.getcwd(), self=self))
        self.pbp = pd.DataFrame(parsed['rowSet'])
        self.pbp.columns= parsed['headers']
        return self

a = Game('01.13.2016', 'DEN', 'GSW')  

df = pd.DataFrame(a.tracking_data['events'])
df2 = pd.DataFrame()

counter = 0
for row in df.moments:
    for inner_row in row['moments']:
        df = df.append(inner_row[5])
    counter += 1
        

        
# http://opiateforthemass.es/articles/animate-nba-shot-events/
        
# http://opiateforthemass.es/articles/animate-nba-shot-events/
        
        
        
        
        
        



