from odoo import models, fields, api

class DailyReport (models.Model):
    _name = 'appschef.daily.report'
    _description = 'This class contains daily reports data.'
    
    report_number = fields.Char(string="Report Number", readonly=True, copy=False, default='New')
    date = fields.Date(string='Report Date', required=True)
    name = fields.Many2one(
        'appschef.employee',
        string= "Employee's Name",
        ondelete='cascade', 
        required=True)
    state = fields.Selection(
        [
            ('draft','Draft'),
            ('submitted','Submitted'),
            ('validated','Validated')
        ], 
        default = "draft"
    )
    list_report_ids = fields.One2many(
        'appschef.list.reports',
        'daily_report_id',
        string='List Reports'
    )
    def action_validate(self):
        self.write({'state': 'validated'})
    def action_invalidate(self):
        self.write({'state': 'draft'})
    def action_submit(self):
        self.write({'state': 'submitted'})
        return self.env.ref('appschef.action_tree_daily_report').read()[0]
    def create(self, vals):
        if vals.get('report_number', 'New') == 'New':
            vals['report_number'] = self.env['ir.sequence'].next_by_code('appschef.daily.report') or 'New'
        return super(DailyReport, self).create(vals)       

class ListReports (models.Model):
    _name = 'appschef.list.reports'
    _description = 'List of Reports about the project.'

    daily_report_id = fields.Many2one(
        'appschef.daily.report',
        string='Daily Report',
        ondelete='cascade',
        required=True
    )
    project_id = fields.Many2one(
        'appschef.project',
        string='Project',
        ondelete='cascade',
        required=True
    )
    summary = fields.Text(string='Summary', required=True)

class ReportDailyReport(models.AbstractModel):
    _name = 'report.appschef.report_daily_report'
    _description = 'Daily Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['appschef.daily.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'appschef.daily.report',
            'docs': docs,
        }
    


    
    
