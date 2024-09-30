from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, time, timedelta

class ReportAttendance(models.AbstractModel):
    _name = 'report.erpezi_hr.report_bonds_template'
    _description = 'Attendance PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        list_values=[]



        payment = self.env['partner.loan.installment.details'].search([
            ("company_id", "=", data['form'].get('company_id')[0]),
            ("date_from", ">=", data['form'].get('date_from')),
            ("date_to", "<", data['form'].get('date_to')),
            ("loan_id", "=", data['form'].get('loan_id'))
        ])


        payment_paid = payment.total




        input_data = {
                'payment_paid':  payment_paid
            }
        list_values.append(input_data)

        return {
            'data': data['form'],
            'lines': list_values,
        }
