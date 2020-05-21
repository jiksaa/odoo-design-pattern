from odoo import models, fields, api
from .counter_state import COUNTER_STATE_DRAFT, COUNTER_STATE_SELECTION
from .counter_state import AbstractCounterState


class Counter(models.Model):
    """
    Counter workflow
    +-------------------------------------------------+
    |                                                 |
    | +----+----+      +-----------+      +----+---+  |
    | |         | run  |           | lock |        |  |
    | |  draft  +----->+  running  +----->+  done  |  |
    | |         |      |           |      |        |  |
    | +---------+      +-+-------+-+      +--------+  |
    |                    |       ^                    |
    |                    +-------+                    |
    |                      count                      |
    |                                                 |
    +---------------+----------------+----------------+
                    |                ^
                    +----------------+
                          notify
    """
    _name = 'jk.simple.counter'
    _inherit = ['mail.thread']
    _description = 'Counter'

    name = fields.Char(string='Name', required=True)
    value = fields.Integer(string='Value', default=0, required=True)
    state = fields.Selection(
        selection=COUNTER_STATE_SELECTION,
        string='State',
        default=COUNTER_STATE_DRAFT,
        required=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='Assign To',
        default=lambda self: self.env.user,
    )

    def _get_state(self):
        self.ensure_one()
        return AbstractCounterState.get_state(self)

    @api.multi
    def action_run(self):
        for counter in self:
            counter._get_state().action_run()

    @api.multi
    def action_done(self):
        for counter in self:
            counter._get_state().action_done()

    def action_count(self):
        for counter in self:
            counter._get_state().action_count()

    def action_notify(self):
        """
        Common action whatever the state
        :return: None
        """
        for counter in self:
            counter.message_post(body='Actual counter value is: {}'.format(counter.value))
