from odoo import models
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import dateutil
import odoo.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class loanAgesReceivables(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.loan_payments_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Appointment")
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        cell_format2 = workbook.add_format({'align': 'center', 'border': True})
       # sheet.set_column(0, 86, 25)
        sheet.set_column(0, 0, None, cell_format)

      #  sheet.set_column(0, 86, 25)
        sheet.merge_range('Y1:AH1', 'تقرير اعمار الاقساط المستحقة', cell_format)



        bold = workbook.add_format({'bold': True})
        row = 1
        col = 0

        sheet.write(row, col + 23, 'تصنيف القرض', cell_format)
        sheet.write(row, col + 24, 'مجموع الرصيد', cell_format)
        sheet.write(row, col + 25, 'مجموع المستحق', cell_format)
        sheet.write(row, col + 26, 'خلال سنة', cell_format)
        sheet.write(row, col + 27, 'خلال 10 شهور', cell_format)
        sheet.write(row, col + 28, 'خلال 6 شهور', cell_format)
        sheet.write(row, col + 29, 'خلال 3 شهور', cell_format)
        sheet.write(row, col + 30, 'خلال شهر', cell_format)
        sheet.write(row, col + 31, 'خلال اسبوع', cell_format)
        sheet.write(row, col + 32, 'خلال يوم', cell_format)
        sheet.write(row, col + 33, 'العملة', cell_format)
        sheet.write(row, col + 34, 'اسم المستفيد', cell_format)
        # loaners = self.env['res.partner'].search([("active", "=", True), ("category.id", "=", 5)])
        loaners = self.env['partner.loan.details'].search(['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse')])

        loan_doc_type = 'S'
        nationality_symbol = 'PS'
        facility_id = ''
        facility_category = 'SI'
        account_type = 'S'
        company_id = ''
        branch_id = '1'
        facility_type = 'F024'
        economic_sector = 'S2'
        cus_eval_stat = '0'
        line_type = 'M'
        legal = 'B'
        doc_type = 'DC'
        tot_amt = 0

        for loaner in loaners:
            loan_num = loaner.name
            fin_t_typee = loaner.loan_class

            if loaner.loan_prog == 'trial':
                prgoram_typee = 'تجريبي'
                tot_amt = loaner.principal_amount
            elif loaner.loan_prog == 'cluster':
                prgoram_typee = 'عناقيد'
                tot_amt = loaner.final_total
            else:
                prgoram_typee = ""

            balance_amt = loaner.total_amount_due
            alocation_amt = tot_amt - balance_amt
            line_count = loaner.duration
            date_disb = loaner.date_disb.strftime("%d/%m/%Y")
            com = self.env['res.partner'].search([("id", "=", loaner.partner_id.id)])

            if com.card_id:
                id = com.card_id
            else:
                id = ""
            guarantor_id = self.env['res.partner'].search([("id", "=", loaner.guarantor_id.id)])
            if guarantor_id.card_id:

                guar_card_id = guarantor_id.card_id
                guar_name = guarantor_id.name

            else:
                guar_card_id = ""
                guar_name = ""

            #  print(guarantor_id.id)
            # print(loaner.id)
            last_pay = self.env['partner.loan.installment.details'].search([('loan_id.id', '=', loaner.id)], limit=1,
                                                                           order="id desc")
            last_pay_date = self.env['partner.loan.installment.details'].search(
                [('loan_id.id', '=', loaner.id), ('state', '=', 'paid')], limit=1, order="id desc")
            first_line = self.env['partner.loan.installment.details'].search([('loan_id.id', '=', loaner.id)], limit=1)
            line_amt = first_line.total
            last_date = last_pay.date_from.strftime("%d/%m/%Y")
            if last_pay_date:
                last_paid_date = last_pay_date.date_from.strftime("%d/%m/%Y")
            else:
                last_paid_date = ''
            if loaner.grace_period:
                grace = loaner.grace_period
            else:
                grace = ''
            d2 = date.today()
            # print (d2)
            sum_unpaid = self.env['partner.loan.installment.details'].search(
                [('loan_id.id', '=', loaner.id), ('state', '=', 'unpaid'), ('date_from', '<', d2)])
            sum_u = sum_unpaid.filtered(lambda line: line.loan_id.id == loaner.id)
            pai = 0

            if sum_u:
                for sum in sum_u:
                    pai += sum.total
       #     print(pai)
            if loaner.company_id.id == 1:
                curr = 'ILS'
            elif loaner.company_id.id == 2:
                curr = 'USD'
            if loaner.loan_prog == 'trial':
                intrest_amt = 0.03
            elif loaner.loan_prog == 'cluster':
                intrest_amt = 4000

            intrest_type = '9'
            # month = loaner.date_disb
            month = loaner.date_disb.strftime("%m")
            year = loaner.date_disb.strftime("%Y")
            G1 = loaner.principal_amount
            # month = datetime.datetime.strptime(str(loaner.date_disb), '%Y-%m-%d').date()
            row += 1



            if fin_t_typee == 'islamic':
                fin_typee = 'اسلامي'

            elif fin_t_typee == 'commercial':
                fin_typee = 'تجاري'
            else:
                fin_t_typee = ""
            sheet.write(row, col + 29, fin_typee, cell_format2)
            sheet.write(row, col + 33, loaner.currency_id.name, cell_format2)
            sheet.write(row, col + 34, loaner.partner_id.name, cell_format2)
            ids = self.env['partner.loan.installment.details'].search([('loan_id', '=', loaner.id)])
            paid_0 = 0
            paid_7 = 0
            paid_30 = 0
            paid_60 = 0
            paid_90 = 0
            paid_120 = 0
            paid_180 = 0
            paid_300 = 0
            paid_360 = 0
            remains_0 = 0
            remains_30 = 0
            remains_60 = 0
            remains_90 = 0
            remains_120 = 0
            remains_180 = 0
            remains_360 = 0
            cus_loan_class = ''
            




            total_ages = remains_30 + remains_60 + remains_90 + remains_120 + remains_180 + remains_360
            sheet.write(row, col + 32, paid_0, cell_format2)
            sheet.write(row, col + 31, paid_7, cell_format2)
            sheet.write(row, col + 30, paid_30, cell_format2)
            sheet.write(row, col + 29, paid_90, cell_format2)
            sheet.write(row, col + 28, paid_180, cell_format2)
            sheet.write(row, col + 27, paid_300, cell_format2)
            sheet.write(row, col + 26, paid_360, cell_format2)
            sheet.write(row, col + 25, total_ages, cell_format2)
            sheet.write(row, col + 24, loaner.total_amount_due, cell_format2)
            sheet.write(row, col + 23, cus_loan_class, cell_format2)

        #   print (id)
       ###     if id.loan_id:
        ###        if id.date_from + dateutil.relativedelta.relativedelta(days=0) < datetime.now().date() and id.date_from + dateutil.relativedelta.relativedelta(days=30) > datetime.now().date():
                    ##     total += id.tot_sum
                    ##     delay_amt1 = total
                    # #       self.update({'aging1': delay_amt1})
               #     lonns.update({'class_comp': '1'})
        ###        if id.date_from + dateutil.relativedelta.relativedelta(days=31) < datetime.now().date() and id.date_from + dateutil.relativedelta.relativedelta(days=60) > datetime.now().date():
                ##    total2 += id.tot_sum
                ##    delay_amt2 = total2
                ##     self.update({'aging2': delay_amt2})
                   #  lonns.update({'class_comp': '2'})
        ###        if id.date_from + dateutil.relativedelta.relativedelta(days=61) < datetime.now().date() and id.date_from + dateutil.relativedelta.relativedelta(days=90) > datetime.now().date():
                ##   total3 += id.tot_sum
                ##   delay_amt3 = total3
                ##   self.update({'aging3': delay_amt3})
                  #   lonns.update({'class_comp': '3'})
        ###        if id.date_from + dateutil.relativedelta.relativedelta(days=91) < datetime.now().date() and id.date_from + dateutil.relativedelta.relativedelta(days=120) > datetime.now().date():
                ##   total4 += id.tot_sum
                ##   delay_amt4 = total4
                ##      self.update({'aging4': delay_amt4})
                    # lonns.update({'class_comp': '4'})
