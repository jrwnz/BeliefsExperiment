from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class UndercuttingPracticeInstructions(Page):
    template_name = 'global/UndercuttingPracticeInstructions.html'

    def is_displayed(self):
        return self.round_number == 1

class MainInterface(Page):
    template_name = 'global/MainInterface.html'

    form_model = 'player'
    form_fields = ['action','played_by','time_to_decide','time_to_submit','times_changed_mind']

    def before_next_page(self):
        self.player.set_opponent_action()

page_sequence = [UndercuttingPracticeInstructions, MainInterface]
