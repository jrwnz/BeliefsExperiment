from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class SectionContinue(Page):
    template_name = 'global/SectionContinue.html'

    def is_displayed(self):
        return self.round_number == 1

class SectionContinueWait(WaitPage):
    wait_for_all_groups = True
    template_name = 'global/WaitPage.html'

    def is_displayed(self):
        return self.round_number == 1

class MatrixTraining(Page):
    template_name = 'global/MatrixTraining.html'                
    form_model = 'player'
    form_fields = ['response','played_by','time_to_decide','time_to_submit']

page_sequence = [SectionContinue, SectionContinueWait, MatrixTraining]
