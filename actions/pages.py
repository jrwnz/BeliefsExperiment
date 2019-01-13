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

class MainInterface(Page):
    template_name = 'global/MainInterface.html'

    form_model = 'player'
    form_fields = ['action','played_by','time_to_decide','time_to_submit','times_changed_mind']

    def before_next_page(self):
        self.player.set_opponent_action()

class RoundWait(WaitPage):
    wait_for_all_groups = True
    template_name = 'global/WaitPage.html'

    def after_all_players_arrive(self):
        if self.round_number == Constants.num_rounds:
            for player in self.subsession.get_players():
                player.store_data()

page_sequence = [SectionContinue, SectionContinueWait, MainInterface, RoundWait]
