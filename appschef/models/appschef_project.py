from odoo import models, fields

class Project(models.Model):
    _name = 'appschef.project'
    _description = 'Projects Data'

    name = fields.Char(string='Name', required=True)
    technologies = fields.Selection(
        [
            ("android","Android"),
            ("desktop","Desktop"),
            ("macos","MacOS")
        ], 
        string = "Techonologies", 
        required=True
    )
    project_type = fields.Selection(
        [
            ("contract","Contract"),
            ("collaboration","Collaboration")
        ], string = "Project Type", 
        required=True
    )
    karyawan_ids = fields.Many2many(
        'appschef.employee',
        'employee_project_rel',
        'employee_id',
        'project_id',
        string='Related Employees'
    )

    list_reports_ids = fields.One2many(
        'appschef.list.reports',
        'project_id',
        string="List of Reports."
    ) 