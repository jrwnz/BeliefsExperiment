from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json

author = 'Jeremy'

doc = """
Calculates and presents payments based on specifications in payoff_info.json.
"""

class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1

    with open('Settings/payoff_info.json','r') as f:
        payoff_info = json.load(f)
    with open('Settings/payoff_info.json','r') as f:
        payoff_info = json.load(f)
    with open('Settings/games.json','r') as f:
        all_game_info = json.load(f)

class Subsession(BaseSubsession):
    def set_all_section_a_actions(self):
        all_section_a_actions = {'red': {}, 'blue': {}}
        for player in self.get_players():
            role = 'blue' if player.participant.id_in_session % 2 == 1 else 'red'
            section_a_outcomes = player.participant.vars['section_a_outcomes']
            for outcome in section_a_outcomes:
                game_code = outcome['game_code']
                action = outcome['action']
                if action:
                    if game_code in all_section_a_actions[role]:
                        all_section_a_actions[role][game_code].append(action)
                    else:
                        all_section_a_actions[role][game_code] = [action]

        self.session.vars['all_section_a_actions'] = all_section_a_actions

    def load_test_data(self):
        print('---------------------loading test data---------------------')
        with open('Settings/TestData/all_section_a_actions.json','r') as f:
            all_section_a_actions = json.load(f)
        self.session.vars['all_section_a_actions'] = all_section_a_actions

        with open('Settings/TestData/section_a_outcomes.json','r') as f:
            section_a_outcomes = json.load(f)
        with open('Settings/TestData/section_b_outcomes.json','r') as f:
            section_b_outcomes = json.load(f)            
        for player in self.get_players():
            player.participant.vars['section_a_outcomes'] = section_a_outcomes
            player.participant.vars['section_b_outcomes'] = section_b_outcomes

    def write_test_data(self):
        print('---------------------writing test data---------------------')
        with open('Settings/TestData/all_section_a_actions.json','w') as f:
            json.dump(self.session.vars['all_section_a_actions'],f)

        player = self.get_players()[0]
        if 'section_a_outcomes' in player.participant.vars:
            with open('Settings/TestData/section_a_outcomes.json','w') as f:
                json.dump(player.participant.vars['section_a_outcomes'],f)
        if 'section_b_outcomes' in player.participant.vars:
            with open('Settings/TestData/section_b_outcomes.json','w') as f:
                json.dump(player.participant.vars['section_b_outcomes'],f) 

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    action_earnings = models.CurrencyField(min=0)
    belief_earnings = models.CurrencyField(min=0)
    earnings_info = models.LongStringField()

    def role(self):
        if self.participant.id_in_session % 2 == 1:
            return 'blue'
        else:
            return 'red'

    def get_payoffs(self):
        if self.participant.id_in_session % 2 == 1:
            role = 'blue'  
            opponent_role = 'red'
        else:
            role = 'red'
            opponent_role = 'blue'

        paid_round_outcomes = []
        paid_game_codes = []

        #Draw rounds for payment based on parameters fron Constants.payoff_info
        #Restrictions is that no two rounds with the same game_code can be selected
        for section in Constants.payoff_info:
            for payment_type in Constants.payoff_info[section]:
                section_outcomes = self.participant.vars['section_{}_outcomes'.format(section)]
                number_of_payoffs = Constants.payoff_info[section][payment_type]['number']
                for _ in range(number_of_payoffs):
                    possible_payoff_outcomes = [outcome for outcome in section_outcomes if outcome['game_code'] not in paid_game_codes and outcome['round_complete']]
                    if len(possible_payoff_outcomes) == 0:
                        break
                    outcome = random.choice(possible_payoff_outcomes)
                    outcome['payment_type'] = payment_type
                    outcome['section'] = section
                    outcome['section_number'] = ['a','b'].index(section)+1
                    paid_round_outcomes.append(outcome)
                    paid_game_codes.append(outcome['game_code'])

        #For section b paid rounds, draw random opponent action from section A
        all_section_a_actions = self.session.vars['all_section_a_actions']
        for outcome in paid_round_outcomes:
            if outcome['section'] == 'b':
                outcome['opponent_action'] = random.choice(all_section_a_actions[opponent_role][outcome['game_code']])
                
        #For all paid rounds, do randomizations to determine payoffs
        for outcome in paid_round_outcomes:
            outcome['payoffs'] = Constants.all_game_info[outcome['game_code']]['Payoffs']

            if outcome['payment_type'] == 'action':
                if role == 'blue':
                    payoff_prob = outcome['payoffs'][outcome['action']][outcome['opponent_action']][0]
                else:
                    payoff_prob = outcome['payoffs'][outcome['opponent_action']][outcome['action']][1]
                outcome['payoff_prob'] = payoff_prob
                outcome['payoff_draw'] = random.random()
                outcome['payoff_bool'] = outcome['payoff_draw']*100 < outcome['payoff_prob']

            elif outcome['payment_type'] == 'belief':
                outcome['paid_question'] = random.randint(0,100)
                outcome['paid_question_option'] = 'lottery' if outcome['paid_question'] >= int(outcome['belief']) else 'action'       
                outcome['lottery_draw'] = random.random()
                outcome['payoff_bool'] = ((outcome['paid_question_option'] == 'lottery' and outcome['lottery_draw']*100 < outcome['paid_question']) 
                            or (outcome['paid_question_option'] == 'action' and outcome['opponent_action'] in ['U','L']))

            outcome['possible_payoff_amount'] = Constants.payoff_info[outcome['section']][outcome['payment_type']]['amount']
            outcome['payoff_amount'] = outcome['possible_payoff_amount'] if outcome['payoff_bool'] else 0

            self.participant.vars['paid_round_outcomes'] = paid_round_outcomes

        self.action_earnings = sum([outcome['payoff_amount'] for outcome in paid_round_outcomes if outcome['payment_type'] == 'action'])
        self.belief_earnings = sum([outcome['payoff_amount'] for outcome in paid_round_outcomes if outcome['payment_type'] == 'belief'])
        self.earnings_info = json.dumps(paid_round_outcomes)

        self.payoff += self.action_earnings + self.belief_earnings
