from odoo import fields, models
from odoo.tools.misc import get_lang
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta

RESIGNATION_TYPE = [('normalResLess10', 'Normal resignation for less than 10 years'),
                    ('normalResMore10', 'Normal resignation for more than 10 years'),
                    ('endContractNo80', 'End of contract based on Termination of the contract based on Article No 80'),
                    ('endContractNo81', 'End of contract based on Termination of the contract based on Article No 81'),
                    ('terminationContract', 'Termination of contract')
                    ]

class HrGratuitySettlementReport(models.TransientModel):
    _name = 'report.hr.gratuity.settlement'
    _description = 'Report Gratuity Settlement PDF'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved'), ('cancel', 'Rejected')], string='Status', default='approved')
    employee_contract_type = fields.Selection([
        ('limited', 'Limited'),
        ('unlimited', 'Unlimited')], string='Contract Type')
    resignation_type = fields.Selection(selection=RESIGNATION_TYPE,  string='Resignation Type')
    resignation_id = fields.Many2one('hr.resignation', string='Employee')
    emp_Financial_Manager = fields.Char(string="Emp Financial Manager")
    emp_HR_GRO_Manager = fields.Char(string="Emp HR GRO Manager")
    emp_Chief_Accountant = fields.Char(string="Emp Chief Accountant")

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['company_id'] = data['form']['company_id'][0] or False
        result['state'] = data['form']['state'] or False
        result['employee_contract_type'] = data['form']['employee_contract_type'] or False
        result['resignation_type'] = data['form']['resignation_type'] or False
        if data['form']['resignation_id'] and data['form']['resignation_id'][0]:
            result['resignation_id'] = data['form']['resignation_id'][0]
        result['emp_Chief_Accountant'] = data['form']['emp_Chief_Accountant'] or False
        result['emp_HR_GRO_Manager'] = data['form']['emp_HR_GRO_Manager'] or False
        result['emp_Financial_Manager'] = data['form']['emp_Financial_Manager'] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        self._set_employee_managers_name()
        data['form'] = self.read(['date_from', 'date_to', 'company_id', 'state', 'resignation_id', 'employee_contract_type', 'resignation_type', 'emp_Financial_Manager', 'emp_HR_GRO_Manager', 'emp_Chief_Accountant'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)

    def _set_employee_managers_name(self):
        job_managers = self.env['hr.job'].search(
            ["|", "|", ("name", "=", "Chief Accountant"), ("name", "=", "HR & GRO Manager"),
             ("name", "=", "Financial Manager")])
        for job in job_managers:
            employee_managers = self.env['hr.employee'].search([("job_id", "=", job.id)])
            if job.name == "Chief Accountant":
                self.emp_Chief_Accountant = employee_managers[0].local_name
            if job.name == "HR & GRO Manager":
                self.emp_HR_GRO_Manager = employee_managers[0].local_name
            if job.name == "Financial Manager":
                self.emp_Financial_Manager = employee_managers[0].local_name

    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref(
            'erpezi_hr.report_hr_gratuity_settlement').report_action(
            records, data=data)
