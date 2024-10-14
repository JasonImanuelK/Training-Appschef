from odoo import models, fields

class CommissionRuleWizard(models.TransientModel):
    _name = 'commission.rule.wizard'
    _description = 'Wizard to create Commission Rules'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    percentage = fields.Float(string='Commission Percentage', required=True)

    def create_commission_rule(self):
        self.env['appschef.list.rule'].create({
            'product_id': self.product_id.id,
            'percentage': self.percentage,
            'com_rule_id': self._context.get('com_rule_id')
        })
