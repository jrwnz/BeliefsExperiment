from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import json


class ExperimentFinished(WaitPage):
    wait_for_all_groups = True
    template_name = 'global/ExperimentFinished.html'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        if self.session.config['load_test_data_if_yes'] == 'yes':
            self.subsession.load_test_data()
        else:
            self.subsession.set_all_section_a_actions()
            if self.session.config['write_test_data_if_yes'] == 'yes':
                self.subsession.write_test_data()

        for player in self.subsession.get_players():
            player.get_payoffs()
                
            if player.participant.label == None:
                player.participant.label = '0'   

class SectionContinue(Page):
    template_name = 'global/SectionContinue.html'

# class PaymentsSetupWait(WaitPage):
#     wait_for_all_groups = True
#     template_name = 'global/WaitPage.html'

#     def after_all_players_arrive(self):
#         if self.session.config['load_test_data_if_yes'] == 'yes':
#             self.subsession.load_test_data()
#         else:
#             self.subsession.set_all_section_a_actions()
#             if self.session.config['write_test_data_if_yes'] == 'yes':
#                 self.subsession.write_test_data()

#         for player in self.subsession.get_players():
#             player.get_payoffs()
                
#             if player.participant.label == None:
#                 player.participant.label = '0'              

class PaymentInstructions(Page):
    template_name = 'global/PaymentsInstructions.html' 
        
class Payments(Page):
    template_name = 'global/Payments.html'

page_sequence = [
    ExperimentFinished,
    SectionContinue, 
    # PaymentsSetupWait, 
    PaymentInstructions, 
    Payments
    ]
