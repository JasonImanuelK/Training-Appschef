# -*- coding: utf-8 -*-

from odoo import models, fields


class Employee(models.Model):
    _name = 'appschef.employee'
    _description = 'Employees Data'

    name = fields.Char(string='Name', required=True)
    position = fields.Selection([
        ('manager', 'Manager'),
        ('intern', 'Intern'),
        ('employee', 'Employee')
    ], string='Position', 
    required=True)
    manager = fields.Many2one(
        'appschef.employee',
        string='Manager',
        ondelete='cascade',
        domain="[('position', '=', 'manager'), ('id', '!=', id)]")
    gender = fields.Selection(
        [
            ("man","Man"),
            ("woman", "Women")
        ],
        string='Gender', 
        required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)

    project_ids = fields.Many2many(
        'appschef.project',
        'employee_project_rel',
        'project_id',
        'employee_id',
        string='Related Projects'
    )

    com_rule_ids = fields.Many2many(
        'appschef.commission.rule',
        'employee_com_rule_rel',
        'com_rule_id',
        'employee_id',
        string="Related Rules",
        required= False
    )
    history_com_ids = fields.One2many(
        'appschef.history.commission',
        'employee_id',
        string='List History Commission'
    )

    sale_order_ids = fields.One2many(
        'sale.order',
        'employee_id',
        string='List sale order'
    )



    

