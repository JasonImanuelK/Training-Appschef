from odoo import fields, api, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    com_amount = fields.Monetary(compute="_compute_com_amount", readonly=True, default=0.0)

    @api.depends('product_id', 'order_id.employee_id')
    def _compute_com_amount(self):
        for rec in self:
            if rec.product_id and rec.order_id and rec.order_id.employee_id:
                records = rec.env['appschef.list.rule'].search([
                    ('product_id', '=', rec.product_id.id),
                    ('employee_id','=', rec.order_id.employee_id.id)])
                if records :
                    rec.com_amount = records.percentage*rec.price_total/100 
                else:
                    rec.com_amount = 0.0
            else:
                rec.com_amount = 0.0

class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_com = fields.Monetary(string="Total Commission",compute="_compute_total_commission", default=0.0)
    employee_id = fields.Many2one(
        'appschef.employee',
        string='Employee',
        ondelete='cascade',
        required=True
    )
    have_com = fields.Boolean(compute="_check_commission", default=False)

    @api.depends('total_com')
    def _check_commission(self):
        if self.total_com <= 0.0:
            self.have_com = False
        else:
            self.have_com = True

    @api.depends('order_line.com_amount')
    def _compute_total_commission(self):
        for rec in self:
            rec.total_com = 0.0
            for record in rec.order_line :
                if record.com_amount :
                    rec.total_com += record.com_amount
                else :
                    rec.total_com += 0.0

    def _action_confirm(self):
        if self.state == "sale" and self.have_com:
            self.env['appschef.history.commission'].create({
                    'com_date': self.date_order,
                    'employee_id': self.employee_id.id,
                    'order_id': self.id,
                    'com_amount': self.total_com
            })
        super(SaleOrder, self)._action_confirm()

    def _action_cancel(self):
        if self.have_com:
            commission_rules = self.env['appschef.history.commission'].search([
                ('order_id', '=', self.id)
            ])
            
            if commission_rules:
                commission_rules.unlink() 
                print("Delete commission rules for product ID ")
            else:
                print("No commission rules found to delete.")

        super(SaleOrder, self)._action_cancel()

        
