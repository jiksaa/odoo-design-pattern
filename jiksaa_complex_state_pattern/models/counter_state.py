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

    def action_done(self):
        raise ValidationError('Draft Counter could not be set to Done')

    def action_run(self):
        self.counter.state = COUNTER_STATE_RUNNING

    def action_count(self):
        raise ValidationError('Counter should be running to perform this action')


class CounterStateRunning(models.Model):
    _name = 'counter.state.running'
    _inherit = 'jk.counter.state'
    _sequence = 'jk_counter_state_id_seq'

    type = fields.Char(default=_name)

    def action_done(self):
        self.counter.state = COUNTER_STATE_DONE

    def action_run(self):
        raise ValidationError('The counter is already running')

    def action_count(self):
        self.counter.value += 1


class CounterStateDone(models.Model):
    _name = 'counter.state.done'
    _inherit = 'jk.counter.state'
    _sequence = 'jk_counter_state_id_seq'

    type = fields.Char(default=_name)

    locked_error = 'Counter is locked'

    def action_done(self):
        raise ValidationError(self.locked_error)

    def action_run(self):
        raise ValidationError(self.locked_error)

    def action_count(self):
        raise ValidationError(self.locked_error)
