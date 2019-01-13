from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Jeremy Ward'

doc = """
Collects actions in unsynchronized, matched games.
"""

class Constants(BaseConstants):
    name_in_url = 'undercutting'
    collect_actions = True
    collect_beliefs = False
    practice = False

    players_per_group = 2

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

        blue_players = [player for player in self.get_players() if player.role() == 'blue']
        red_players = [player for player in self.get_players() if player.role() == 'red']
        random.shuffle(red_players)
        self.set_group_matrix(
            [list(x) for x in zip(blue_players,red_players)]
        )

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    game_code = models.StringField()
    game_payoffs = models.StringField()
    game_type = models.StringField()
    game_index = models.StringField()
    game_iteration = models.IntegerField(min=0)

    played_by = models.StringField()
    time_to_decide = models.FloatField(min=0,blank=True)
    time_to_submit = models.FloatField(min=0,blank=True)
    times_changed_mind = models.IntegerField(min=0,blank=True)

    action = models.StringField(blank=True)
    opponent_action = models.StringField(blank=True)

    def role(self):
        if self.participant.id_in_session % 2 == 1:
            return 'blue'
        else:
            return 'red'

    def get_game_info(self):
        game = Constants.game_order[self.round_number-1][self.role()]
        game_info = Constants.all_game_info[game['Code']]
        self.game_code = game['Code']
        self.game_type = game['Type']
        self.game_index = game['Index']
        self.game_payoffs = json.dumps(game_info['Payoffs'])
        self.game_iteration = game['Iteration']

    def set_opponent_action(self):
        self.get_others_in_group()[0].opponent_action = self.action 

    def store_data(self):
        all_outcomes = []
        for round_data in self.in_all_rounds():
            outcome = {
                'action': round_data.action,
                'opponent_action': round_data.opponent_action,
                'game_code': round_data.game_code,
                'round_number': round_data.round_number,
                'role': self.role()
            }
            all_outcomes.append(outcome)
        self.participant.vars['section_uc_outcomes'] = all_outcomes
