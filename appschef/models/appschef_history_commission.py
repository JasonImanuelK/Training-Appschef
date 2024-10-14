from odoo import models, fields,api


class HistoryCommission(models.Model):
    _name = 'appschef.history.commission'
    _description = "It's a model to store employee's commission"

    com_date = fields.Date(string="Commission Date")
    employee_id = fields.Many2one(
        'appschef.employee',
        string='Employee',
        ondelete='cascade',
        required=True)
    order_id = fields.Many2one(
        'sale.order',
        string="Order Reference",
        required=True, ondelete='cascade', index=True, copy=False)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True,
        precompute=True,
        ondelete='restrict'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    com_amount = fields.Monetary(string="Commission Amount")

    @api.depends('company_id')
    def _compute_currency_id(self):
        for order in self:
            order.currency_id = order.company_id.currency_id