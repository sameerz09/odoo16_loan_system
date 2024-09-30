from odoo import fields, models
from odoo.tools.misc import get_lang
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta

class AttendanceReport(models.TransientModel):
    _name = 'bonds.report'
    _description = 'Report Attendance PDF'

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date',required=True, default=(datetime.now()+relativedelta(months=-1)).strftime('%Y-%m-25'))
    date_to = fields.Date(string='End Date',required=True, default=(datetime.now()).strftime('%Y-%m-24'))
    loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")



    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['company_id'] = data['form']['company_id'][0] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)



    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('erpezi_hr.report_attendance').report_action(records, data=data)

class PortfolioReport(models.TransientModel):
        _name = 'portfolio.report'
        _description = 'Report portfolio PDF'

        company_id = fields.Many2one('res.company', string='Company', required=True,
                                     default=lambda self: self.env.company)
        date_from = fields.Date(string='Start Date', required=True,
                                default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
        date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
        loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

        def _build_contexts(self, data):
            result = {}
            result['date_from'] = data['form']['date_from'] or False
            result['date_to'] = data['form']['date_to'] or False
            result['company_id'] = data['form']['company_id'][0] or False

            return result

        def check_report(self):
            self.ensure_one()
            data = {}
            data['ids'] = self.env.context.get('active_ids', [])
            data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
            data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
            used_context = self._build_contexts(data)
            data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

            return self.with_context(discard_logo_check=True)._print_report(data)

        def _print_report(self, data):
            records = self.env[data['model']].browse(data.get('ids', []))
            return self.env.ref('odoo_customer_supplier_loan.sampo_report').report_action(records, data=data)

class agriculturalReport(models.TransientModel):
            _name = 'agricultural.report'
            _description = 'Agricultural Activities Report'

            company_id = fields.Many2one('res.company', string='Company', required=True,
                                         default=lambda self: self.env.company)
            date_from = fields.Date(string='Start Date', required=True,
                                    default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
            date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
            loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

            def _build_contexts(self, data):
                result = {}
                result['date_from'] = data['form']['date_from'] or False
                result['date_to'] = data['form']['date_to'] or False
                result['company_id'] = data['form']['company_id'][0] or False

                return result

            def check_report(self):
                self.ensure_one()
                data = {}
                data['ids'] = self.env.context.get('active_ids', [])
                data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
                data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
                used_context = self._build_contexts(data)
                data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

                return self.with_context(discard_logo_check=True)._print_report(data)

            def _print_report(self, data):
                records = self.env[data['model']].browse(data.get('ids', []))
                return self.env.ref('odoo_customer_supplier_loan.borrower_report').report_action(records, data=data)

class barroersReport(models.TransientModel):
                _name = 'borrower.report'
                _description = 'Borrowers Report'

                company_id = fields.Many2one('res.company', string='Company', required=True,
                                             default=lambda self: self.env.company)
                date_from = fields.Date(string='Start Date', required=True,
                                        default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
                date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
                loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

                def _build_contexts(self, data):
                    result = {}
                    result['date_from'] = data['form']['date_from'] or False
                    result['date_to'] = data['form']['date_to'] or False
                    result['company_id'] = data['form']['company_id'][0] or False

                    return result

                def check_report(self):
                    self.ensure_one()
                    data = {}
                    data['ids'] = self.env.context.get('active_ids', [])
                    data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
                    data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
                    used_context = self._build_contexts(data)
                    data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

                    return self.with_context(discard_logo_check=True)._print_report(data)

                def _print_report(self, data):
                    records = self.env[data['model']].browse(data.get('ids', []))
                    return self.env.ref('odoo_customer_supplier_loan.borrower_report').report_action(records, data=data)


class totalLoansFinancing(models.TransientModel):
    _name = 'totalloans.financing'
    _description = 'Total Loans and Financing'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date', required=True,
                            default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
    date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
    loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['company_id'] = data['form']['company_id'][0] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)

    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('odoo_customer_supplier_loan.totalloans_report').report_action(records, data=data)


class totalLoansFinancing(models.TransientModel):
    _name = 'loan.ages.receivables'
    _description = 'Loans Ages of receivables'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date', required=True,
                            default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
    date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
    loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['company_id'] = data['form']['company_id'][0] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)

    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('odoo_customer_supplier_loan.loan_ages_report').report_action(records, data=data)
class loanagespayments(models.TransientModel):
    _name = 'loan.payments'
    _description = 'Loans Payments'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date', required=True,
                            default=(datetime.now() + relativedelta(months=-1)).strftime('%Y-%m-25'))
    date_to = fields.Date(string='End Date', required=True, default=(datetime.now()).strftime('%Y-%m-24'))
    loan_id = fields.Char(string="Loan Number", readonly=True, help="Loan Number")

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['company_id'] = data['form']['company_id'][0] or False

        return result

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)

        return self.with_context(discard_logo_check=True)._print_report(data)

    def _print_report(self, data):
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('odoo_customer_supplier_loan.payments_reports_xlsx').report_action(records, data=data)







