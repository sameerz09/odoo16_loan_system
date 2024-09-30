# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.tools.misc import get_lang
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta


from odoo import models, fields, api, _

class EmpLoanReport(models.TransientModel):
    _name = 'partner.emp.loan.report'
    _description = 'Employees bonds Loan Report'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date', required=True,
                            default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
    date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
    loan_id = fields.Char(string="Loan Number", readonly=False, help="Loan Number")

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['loan_id'] = data['form']['loan_id'] or False
        result['company_id'] = data['form']['company_id'][0] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'loan_id', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)

    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('erpezi_hr.report_bonds').report_action(records, data=data)
