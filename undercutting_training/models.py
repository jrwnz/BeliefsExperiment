from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Jeremy Ward'

doc = """
Teaches/tests understanding of reading undercutting matrices w/ added probability.
"""

class Constants(BaseConstants):
    name_in_url = 'undercutting_training'
    collect_actions = True
    collect_beliefs = False
    practice = True

    players_per_group = None

    with open('Settings/payoff_info.json','r') as f:
        payoff_info = json.load(f)
    with open('Settings/games.json','r') as f:
        all_game_info = json.load(f)
    with open('Settings/orders.json','r') as f:
        game_order = json.load(f)[name_in_url]

    num_rounds = len(game_order)

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.get_game_info()

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    game_code = models.StringField()
    game_payoffs = models.StringField()
    game_type = models.StringField()
    game_index = models.StringField()
    game_question_player = models.StringField()
    game_question_actions = models.StringField()
    game_correct_response = models.IntegerField(min=0)

    played_by = models.StringField()
    time_to_decide = models.FloatField(min=0,blank=True)
    time_to_submit = models.FloatField(min=0,blank=True)

    response = models.StringField()

    def get_game_info(self):
        game = Constants.game_order[self.round_number-1]['blue']
        game_info = Constants.all_game_info[game['Code']]
        self.game_code = game['Code']
        self.game_type = game['Type']
        self.game_index = game['Index']
        self.game_payoffs = json.dumps(game_info['Payoffs'])
        self.game_question_player = game_info['Question_Player']
        self.game_question_actions = game_info['Question_Actions']

        game_correct_payoffs = game_info['Payoffs'][game_info['Question_Actions'].split(',')[0]][game_info['Question_Actions'].split(',')[1]]
        self.game_correct_response = (game_correct_payoffs[0] if game_info['Question_Player'] == 'blue' else game_correct_payoffs[1])


