from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Jeremy Ward'

doc = """
Collects beliefs and/or actions in unsynchronized, unmatched games.
"""


class Constants(BaseConstants):
    name_in_url = 'beliefs'
    collect_actions = True
    collect_beliefs = True
    practice = False

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
    game_iteration = models.IntegerField(min=0)

    played_by = models.StringField()
    time_to_decide = models.FloatField(min=0,blank=True)
    time_to_submit = models.FloatField(min=0,blank=True)
    times_changed_mind = models.IntegerField(min=0,blank=True)

    interactions = models.StringField()
    
    belief = models.StringField(blank=True)
    action = models.StringField(blank=True)

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

    def store_data(self):
        all_outcomes = []
        for round_data in self.in_all_rounds():
            if round_data.action and round_data.belief:
                outcome = {
                    'action': round_data.action,
                    'belief': round_data.belief,
                    'game_code': round_data.game_code,
                    'round_number': round_data.round_number,
                    'role': self.role()
                }
                all_outcomes.append(outcome)
        self.participant.vars['section_b_outcomes'] = all_outcomes
