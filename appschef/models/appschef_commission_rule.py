from odoo import models, fields, _


class CommissionRule(models.Model):
    _name = 'appschef.commission.rule'
    _description = 'Rule for product to give commission to employee'

    name = fields.Char(string="Commission Name")
    list_rule_ids = fields.One2many(
        'appschef.list.rule',
        'com_rule_id',
        string='List Rule'
    )
    def action_add_rule(self):
        return {
            'name': _('Insert Rule'),
            'type': 'ir.actions.act_window',
            'res_model': 'commission.rule.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'com_rule_id': self.id
            },
        }
    
class ListRule(models.Model):
    _name = 'appschef.list.rule'
    _description = 'List of Rule inside a Commission Rule.'

    com_rule_id = fields.Many2one(
        'appschef.commission.rule',
        string='Commission Rule',
        ondelete='cascade',
        required=True
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        ondelete='cascade',
        required=True
    )
    percentage = fields.Float(string="Percentage", digits=(16, 2))
    
    