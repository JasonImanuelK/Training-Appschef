import io
import json
import xlsxwriter
from datetime import date
from odoo import models, fields
from odoo.http import request, Response

class ReportHistory(models.TransientModel):
    _name = 'appschef.report.history'
    _description = 'Making a report commission history and wizard.'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    project_ids = fields.Many2many(
        'appschef.project',
        'report_project_rel',
        'project_id',
        'report_id',
        string='Related Projects'
    )

    def action_report_xlsx(self):
        if self.project_ids:
            project_id_from_input = self.project_ids.mapped('id')
            project_name_from_input = self.project_ids.mapped('name')

            employees = self.env['appschef.employee'].search([('project_ids', 'in', project_id_from_input)])

            commission_history = self.env['appschef.history.commission'].search([
                ('employee_id', 'in', employees.ids),    
                ('com_date', '>=', self.start_date),    
                ('com_date', '<=', self.end_date),     
            ])
        else:
            project_name_from_input = ""
            commission_history = self.env['appschef.history.commission'].search([  
                ('com_date', '>=', self.start_date),    
                ('com_date', '<=', self.end_date),    
            ])

        employee_totals = {}
        for history in commission_history:
            if history.employee_id.id not in employee_totals:
                employee_totals[history.employee_id.id] = {
                    'employee_name': history.employee_id.name,
                    'total_com_amount': history.com_amount
                }
            else:
                employee_totals[history.employee_id.id]['total_com_amount'] += history.com_amount

        employee_total_list = list(employee_totals.values())

        data = {
            'commission_history': employee_total_list,
            'start_date': self.start_date.isoformat(),
            'end_date' : self.end_date.isoformat(),
            'project_names' : project_name_from_input
        }

        return {
            'type':'ir.actions.report',
            'data':{
                'model':'appschef.report.history',
                'options':json.dumps(data),
                'output_format':'xlsx',
                'report_name':'Report Commission History'
            },
            'report_type':'xlsx'
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        table_header = workbook.add_format()
        table_header.set_border(2)
        table_header.set_bold() 

        table = workbook.add_format()
        table.set_border(2)

        table_money = workbook.add_format({'num_format': '$#,##0.00'})
        table_money.set_border(2)

        com_history = data['commission_history']

        worksheet.write(0,0,'Tanggal',bold)
        worksheet.write(0,1,data['start_date'])
        worksheet.write(0,2,data['end_date'])

        if data['project_names'] != "":
            worksheet.write(1,0,'Project',bold)

            col_projects = 1
            for rec in data['project_names']:
                worksheet.write(1,col_projects,rec)
                col_projects += 1

        worksheet.write(3,0,"Nama",table_header)
        worksheet.write(3,1,'Total Komisi', table_header)

        row = 4
        col = 0

        for record in com_history:
            worksheet.write(row, col, record['employee_name'],table)
            worksheet.write(row, col + 1, record['total_com_amount'],table_money)
            row += 1

        workbook.close()

        output.seek(0)

        response.stream.write(output.read())

        output.close()

