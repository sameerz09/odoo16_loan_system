from odoo import models
from datetime import datetime, timedelta
import datetime
from datetime import date
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class BorrowerXlsx(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.borrowers_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Appointment")
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        cell_format2 = workbook.add_format({'align': 'center', 'border': True})
       # sheet.set_column(0, 86, 25)
        sheet.set_column(0, 0, None, cell_format)

      #  sheet.set_column(0, 86, 25)
        sheet.merge_range('R1:AG1', 'ﺖﻗﺮﻳﺭ ﺎﻠﻤﻘﺗﺮﻀﻴﻧ', cell_format)



        bold = workbook.add_format({'bold': True})
        row = 1
        col = 0

        sheet.write(row, col + 13, 'رقم هاتف المقترض', cell_format)
        sheet.write(row, col + 14, 'رقم هاتف الكفيل', cell_format)
        sheet.write(row, col + 15, 'رقم هوية الكفيل', cell_format)
        sheet.write(row, col + 16, 'اسم الكفيل', cell_format)
        sheet.write(row, col + 17, 'المبلغ الاجمالي بعد احتساب الفائدة', cell_format)
        sheet.write(row, col + 18, 'الرصيد المتبقي', cell_format)
        sheet.write(row, col + 19, 'المبالغ المحصلة', cell_format)
        sheet.write(row, col + 20, 'عملة القرض', cell_format)
        sheet.write(row, col + 21, 'أصل  القرض', cell_format)
        sheet.write(row, col + 22, 'عدد الأقساط', cell_format)
        sheet.write(row, col + 23, 'فترة السماح', cell_format)
        sheet.write(row, col + 24, 'مدة القرض', cell_format)
        sheet.write(row, col + 25, 'التخصص', cell_format)
        sheet.write(row, col + 26, 'التصنيف', cell_format)
        sheet.write(row, col + 27, 'القطاع الزراعي', cell_format)
        sheet.write(row, col + 28, 'اسم البرنامج', cell_format)
        sheet.write(row, col + 29, 'نوع التمويل', cell_format)
        sheet.write(row, col + 30, 'رقم القرض', cell_format)
        sheet.write(row, col + 31, 'رقم هوية المستفيد', cell_format)
        sheet.write(row, col + 32, 'العمر', cell_format)
        sheet.write(row, col + 33, 'اسم المستفيد', cell_format)
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
                prgoram_typee = "موسمي"

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
            print(pai)
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

            sheet.write(row, col + 13, loaner.partner_id.mobile, cell_format2)
            sheet.write(row, col + 14, loaner.guarantor_id.mobile, cell_format2)
            sheet.write(row, col + 15, loaner.guarantor_id.card_id, cell_format2)
            sheet.write(row, col + 16, loaner.guarantor_id.name, cell_format2)
            sheet.write(row, col + 17, loaner.sumation, cell_format2)
            sheet.write(row, col + 18, loaner.total_amount_due, cell_format2)
            sheet.write(row, col + 19, loaner.total_amount_paid, cell_format2)
            sheet.write(row, col + 20, curr, cell_format2)
            sheet.write(row, col + 21, loaner.principal_amount, cell_format2)
            sheet.write(row, col + 22, loaner.dgrace, cell_format2)
            sheet.write(row, col + 23, loaner.duration - loaner.dgrace, cell_format2)
            sheet.write(row, col + 24, loaner.duration, cell_format2)
            sheet.write(row, col + 25, "", cell_format2)
            sheet.write(row, col + 26, "", cell_format2)
            sheet.write(row, col + 27, intrest_type, cell_format2)
            sheet.write(row, col + 27, loaner.agri_type, cell_format2)
            sheet.write(row, col + 28, prgoram_typee, cell_format2)
            if fin_t_typee == 'islamic':
                fin_typee = 'اسلامي'

            elif fin_t_typee == 'commercial':
                fin_typee = 'تجاري'
            else:
                fin_t_typee = ""
            sheet.write(row, col + 29, fin_typee, cell_format2)
            sheet.write(row, col + 30, loan_num, cell_format2)
            sheet.write(row, col + 31, loaner.partner_id.card_id, cell_format2)
            sheet.write(row, col + 32, loaner.partner_id.age, cell_format2)
            sheet.write(row, col + 33, loaner.partner_id.name, cell_format2)



