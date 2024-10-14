from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    list_rule_ids = fields.One2many(
        'appschef.list.rule',
        'product_id',
        string='List Rule'
    )


