from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class UndercuttingTrainingInstructions(Page):
    template_name = 'global/UndercuttingTrainingInstructions.html'

    def is_displayed(self):
        return self.round_number == 1

class UndercuttingTraining(Page):
    template_name = 'global/MatrixTraining.html'                
    form_model = 'player'
    form_fields = ['response','played_by','time_to_decide','time_to_submit']

page_sequence = [UndercuttingTrainingInstructions, UndercuttingTraining]
