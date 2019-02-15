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
    def get_form_fields(self):
        form_fields = ['played_by','time_to_decide','time_to_submit','times_changed_mind','interactions']
        if Constants.collect_beliefs:
            form_fields.append('belief')
        if Constants.collect_actions:
            form_fields.append('action')
        return form_fields

    def before_next_page(self):
        if self.round_number == Constants.num_rounds:
            self.player.store_data()

page_sequence = [SectionContinue, SectionContinueWait, MainInterface]
