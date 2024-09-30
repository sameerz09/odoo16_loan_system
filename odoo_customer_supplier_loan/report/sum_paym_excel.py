from odoo import models
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import dateutil
import odoo.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class loanAgesReceivables(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.sum_paym_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Appointment")
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        cell_format2 = workbook.add_format({'align': 'center', 'border': True})
       # sheet.set_column(0, 86, 25)
        sheet.set_column(0, 0, None, cell_format)

      #  sheet.set_column(0, 86, 25)
        sheet.merge_range('AD1:AI1', 'تقرير تواريخ الدفعات', cell_format)



        bold = workbook.add_format({'bold': True})
        row = 1
        col = 0

        # sheet.write(row, col + 23, 'تصنيف القرض', cell_format)
        sheet.write(row, col + 32, 'تاريخ الدفعة', cell_format)
        sheet.write(row, col + 31, 'قيمة الدفعة', cell_format)
        sheet.write(row, col + 33, 'العملة', cell_format)
        sheet.write(row, col + 34, 'اسم المستفيد', cell_format)
        loaners = self.env['partner.loan.payments'].search([("state", "=", 'paid'), ("payment_date", ">=", data['form'].get('date_from')), ("payment_date", "<=", data['form'].get('date_to'))])

        for loaner in loaners:
            row +=1

            sheet.write(row, col + 31, loaner.pay_amt, cell_format2)
            sheet.write(row, col + 32, loaner.payment_date.strftime("%d/%m/%Y"), cell_format2)
            sheet.write(row, col + 33, loaner.currency_id, cell_format2)
            sheet.write(row, col + 34, loaner.name, cell_format2)
