from odoo import models, fields, api


STATE_SELECTION = [
    ('counter.state.draft', 'Draft'),
    ('counter.state.running', 'Running'),
    ('counter.state.done', 'Locked'),
]

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
    _name = 'jk.complex.counter'
    _inherit = ['mail.thread']
    _description = 'Complex Counter'

    @api.model
    def _default_state_id(self):
        return self.env.ref('jiksaa_complex_state_pattern.counter_state_draft')

    name = fields.Char(string='Name', required=True)
    value = fields.Integer(string='Value', default=0, required=True)
    state = fields.Selection(
        selection=STATE_SELECTION,
        string='State',
        compute='_compute_state',
        store=True,
    )
    state_id = fields.Reference(
        selection=STATE_SELECTION,
        string='State Record',
        required=True,
        default=lambda self: self._default_state_id()
    )
    user_id = fields.Many2one(
        'res.users',
        string='Assign To',
        default=lambda self: self.env.user,
    )

    @api.depends('state_id')
    def _compute_state(self):
        for counter in self:
            counter.state = counter.state_id._name if counter.state_id else False

    @api.multi
    def action_run(self):
        for counter in self:
            counter.state_id.action_run(counter)

    @api.multi
    def action_done(self):
        for counter in self:
            counter.state_id.action_done(counter)

    def action_count(self):
        for counter in self:
            counter.state_id.action_count(counter)

    def action_notify(self):
        """
        Common action whatever the state
        :return: None
        """
        for counter in self:
            counter.message_post(body='Actual counter value is: {}'.format(counter.value))

