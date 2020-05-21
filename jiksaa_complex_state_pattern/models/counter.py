from odoo import models, fields, api


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
        draft_record = self.env.ref('jiksaa_complex_state_pattern.counter_state_draft')
        return draft_record.id

    name = fields.Char(string='Name', required=True)
    value = fields.Integer(string='Value', default=0, required=True)
    state_id = fields.Many2one(
        'jk.counter.state',
        string='State',
        required=True,
        default=lambda self: self._default_state_id()
    )
    user_id = fields.Many2one(
        'res.users',
        string='Assign To',
        default=lambda self: self.env.user,
    )

