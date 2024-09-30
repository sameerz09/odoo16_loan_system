from odoo import models
from datetime import datetime, timedelta
import datetime
from datetime import date
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PartnerXlsx(models.AbstractModel):
    _name = 'report.erpezi_hr.loan_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
      #  print("mmmmmm", data['appointment'])
        sheet = workbook.add_worksheet("Appointment")
        bold = workbook.add_format({'bold': True})
        row = 0
        col = 0
        sheet.write(row, col, 'رقم الهوية او جواز السفر ', bold)
        sheet.write(row, col + 1, 'نوع وثيقة المقترض', bold)
        sheet.write(row, col + 2, 'رمز الجنسية', bold)
        sheet.write(row, col + 3, 'facility ID', bold)
        sheet.write(row, col + 4, 'تصنيف التسهيل', bold)
        sheet.write(row, col + 5, 'تصنيف الحساب', bold)
        sheet.write(row, col + 6, 'رقم الشركة', bold)
        sheet.write(row, col + 7, 'رقم الفرع', bold)
        sheet.write(row, col + 8, 'الشهر', bold)
        sheet.write(row, col + 9, 'السنة', bold)
        sheet.write(row, col + 10, 'نوع التسهيل', bold)
        sheet.write(row, col + 11, 'عملة المنح', bold)
        sheet.write(row, col + 12, 'القطاع الاقتصادي', bold)
        sheet.write(row, col + 13, 'تقييم وضع العميل', bold)
        sheet.write(row, col + 14, 'السقف الممنوح', bold)
        sheet.write(row, col + 15, 'الرصيد المستغل', bold)
        sheet.write(row, col + 16, 'حجم المخصص', bold)
        sheet.write(row, col + 17, 'تاريخ المنح', bold)
        sheet.write(row, col + 18, 'تاريخ استحقاق اخر قسط', bold)
        sheet.write(row, col + 19, 'قيمة الاقساط المستحقة غير المسددة', bold)
        sheet.write(row, col + 20, 'نوع القسط الدوري', bold)
        sheet.write(row, col + 21, 'قيمة القسط الدوري', bold)
        sheet.write(row, col + 22, 'لاجراءات القانونية', bold)
        sheet.write(row, col + 23, 'عدد اقساط التسهيل الممنوح', bold)
        sheet.write(row, col + 24, 'تاريخ اخر قسط تم تسديده', bold)
        sheet.write(row, col + 25, 'فترة السماح', bold)
        sheet.write(row, col + 26, 'سعر الفائدة', bold)
        sheet.write(row, col + 27, 'نوع الفائدة', bold)
        sheet.write(row, col + 28, 'G1', bold)
        sheet.write(row, col + 29, 'رقم الهوية  جواز السفر الأول', bold)
        sheet.write(row, col + 30, 'نوع وثيقة المقترص', bold)
        sheet.write(row, col + 31, ' رمز الجنسية', bold)
        sheet.write(row, col + 32, ' نوع الضمانة المقدمة', bold)
       # loaners = self.env['res.partner'].search([("active", "=", True), ("category.id", "=", 5)])
        loaners = self.env['partner.loan.details'].search([("date_disb", "!=", False), ("state", "=", 'disburse')])

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
        doc_type ='DC'



        for loaner in loaners:
            if loaner.loan_prog == 'trial':
                tot_amt = loaner.principal_amount
            elif loaner.loan_prog == 'cluster':
                tot_amt = loaner.final_total

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

                guar_card_id =  guarantor_id.card_id

            else:
                guar_card_id = ""

          #  print(guarantor_id.id)
           # print(loaner.id)
            last_pay = self.env['partner.loan.installment.details'].search([('loan_id.id','=', loaner.id)], limit=1, order="id desc")
            last_pay_date = self.env['partner.loan.installment.details'].search([('loan_id.id', '=', loaner.id), ('state', '=', 'paid')], limit=1, order="id desc")
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
            #print (d2)
            sum_unpaid = self.env['partner.loan.installment.details'].search([('loan_id.id','=', loaner.id), ('state','=', 'unpaid'), ('date_from', '<', d2)])
            sum_u = sum_unpaid.filtered(lambda line: line.loan_id.id == loaner.id)
            pai = 0
            if sum_u:
                for sum in sum_u:
                    pai += sum.total
            print (pai)
            if loaner.company_id.id == 1:
                   curr = 'ILS'
            elif loaner.company_id.id == 2:
                   curr = 'USD'
            if loaner.loan_prog == 'trial':
                intrest_amt = 0.03
            elif loaner.loan_prog == 'cluster':
                intrest_amt = 4000

            intrest_type = '9'
            #month = loaner.date_disb
            month = loaner.date_disb.strftime("%m")
            year = loaner.date_disb.strftime("%Y")
            G1 = loaner.principal_amount
           # month = datetime.datetime.strptime(str(loaner.date_disb), '%Y-%m-%d').date()
            row += 1
            sheet.write(row, col, id, bold)
            sheet.write(row, col + 1, loan_doc_type, bold)
            sheet.write(row, col + 2, nationality_symbol, bold)
            sheet.write(row, col + 3, facility_id, bold)
            sheet.write(row, col + 4, facility_category, bold)
            sheet.write(row, col + 5, account_type, bold)
            sheet.write(row, col + 6, company_id, bold)
            sheet.write(row, col + 7, branch_id, bold)
            sheet.write(row, col + 8, month, bold)
            sheet.write(row, col + 9, year, bold)
            sheet.write(row, col + 10, facility_type, bold)
            sheet.write(row, col + 11, curr, bold)
            sheet.write(row, col + 12, economic_sector, bold)
            sheet.write(row, col + 13, cus_eval_stat, bold)
            sheet.write(row, col + 14, tot_amt, bold)
            sheet.write(row, col + 15, balance_amt, bold)
            sheet.write(row, col + 16, alocation_amt, bold)
            sheet.write(row, col + 17, date_disb, bold)
            sheet.write(row, col + 18, last_date, bold)
            sheet.write(row, col + 19, pai, bold)
            sheet.write(row, col + 20, line_type, bold)
            sheet.write(row, col + 21, line_amt, bold)
            sheet.write(row, col + 22, legal, bold)
            sheet.write(row, col + 23, line_count, bold)
            sheet.write(row, col + 24, last_paid_date, bold)
            sheet.write(row, col + 25, grace, bold)
            sheet.write(row, col + 26, intrest_amt, bold)
            sheet.write(row, col + 27, intrest_type, bold)
            sheet.write(row, col + 28, G1, bold)
            sheet.write(row, col + 29, guar_card_id, bold)