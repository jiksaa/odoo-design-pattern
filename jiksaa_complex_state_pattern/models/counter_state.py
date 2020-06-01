from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


COUNTER_STATE_DRAFT = 'draft'
COUNTER_STATE_RUNNING = 'running'
COUNTER_STATE_DONE = 'done'


class CounterState(models.Model):
    _name = 'jk.counter.state'
    _description = 'Counter State'
    _table = 'jk_counter_state'

    name = fields.Char(string='Name')
    type = fields.Char(string='Type')


class CounterStateDraft(models.Model):
    _name = 'counter.state.draft'
    _inherit = 'jk.counter.state'
    _sequence = 'jk_counter_state_id_seq'

    type = fields.Char(default=_name)

    def action_done(self, counter):
        raise ValidationError('Draft Counter could not be set to Done')

    def action_run(self, counter):
        counter.state_id = self.env.ref('jiksaa_complex_state_pattern.counter_state_running')

    def action_count(self, counter):
        raise ValidationError('Counter should be running to perform this action')


class CounterStateRunning(models.Model):
    _name = 'counter.state.running'
    _inherit = 'jk.counter.state'
    _sequence = 'jk_counter_state_id_seq'

    type = fields.Char(default=_name)

    def action_done(self, counter):
        counter.state_id = self.env.ref('jiksaa_complex_state_pattern.counter_state_done')

    def action_run(self, counter):
        raise ValidationError('The counter is already running')

    def action_count(self, counter):
        counter.value += 1


class CounterStateDone(models.Model):
    _name = 'counter.state.done'
    _inherit = 'jk.counter.state'
    _sequence = 'jk_counter_state_id_seq'

    type = fields.Char(default=_name)

    locked_error = 'Counter is locked'

    def action_done(self, counter):
        raise ValidationError(self.locked_error)

    def action_run(self, counter):
        raise ValidationError(self.locked_error)

    def action_count(self, counter):
        raise ValidationError(self.locked_error)
