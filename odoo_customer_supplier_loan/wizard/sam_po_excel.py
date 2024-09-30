# -*- coding: utf-8 -*-
from odoo import models, _
class PayrollBatchReportXLSX(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.payroll_batch_report'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Appointment")
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        cell_format2 = workbook.add_format({'align': 'center', 'border': True})

        sheet.set_column(0, 0, None, cell_format)

        sheet.set_column(0, 86, 20)
        sheet.merge_range('B1:N1', 'تقرير المحافظ', cell_format)

        row = 1
        col = 0

        sheet.write(row, col + 13, _("اسم المحفظة"), cell_format)
        sheet.write(row, col + 12, _("النمو في المحفظة"), cell_format)
        sheet.write(row, col + 11, _("عملة المحفظة"), cell_format)
        sheet.write(row, col + 10, _("أصل اللمحفظة"), cell_format)
        sheet.write(row, col + 9, _("رصيد المحفظة الحالي"), cell_format)
        sheet.write(row, col + 8, _("نوع الضمانة المقدمة"), cell_format)
        sheet.write(row, col + 7, _("ديون معدومة"), cell_format)
        sheet.write(row, col + 6, _("نوع وثيقة المقترص"), cell_format)
        sheet.write(row, col + 5, _("اجمالي المبالغ المستردة"), cell_format)
        sheet.write(row, col + 4, _("فوائد مستردة"), cell_format)
        sheet.write(row, col + 3, _("اصل مبالغ مستردة"), cell_format)
        sheet.write(row, col + 2, _("فوائد على التمويلات"), cell_format)
        sheet.write(row, col + 1, _("تمويلات ممنوحة"), cell_format)

        #sum_dur_unpaid = self.env['partner.loan.type'].search([('loan_id.id', '=', loaner.id)])
        row = 2
        col = 0
        sheet.write(row, col + 13, _("برنامج العناقيد"), cell_format2)
        sheet.write(row, col + 12, _("0"), cell_format2)
        sheet.write(row, col + 11, _("ILS"), cell_format2)
        sheet.write(row, col + 10, _("10000000"), cell_format2)
        sheet.write(row, col + 9, _("9000"), cell_format2)
        sheet.write(row, col + 8, _("كفيل + شيكات"), cell_format2)
        sheet.write(row, col + 7, _("0"), cell_format2)
        sheet.write(row, col + 6, _("هوية شخصية"), cell_format2)
        paid = self.env['partner.loan.details'].search([("state", "=", 'disburse')])
        if paid:
           sum_clus_paid = paid.filtered(lambda line: line.loan_prog == 'cluster')
           map_c_p = sum_clus_paid.mapped('total_amount_paid')
           sum_c_p = sum(map_c_p)
        else:
            sum_c_p = 0
      ###  cluster_intrest = self.env['partner.loan.installment.details'].search([("state", "=", 'paid')])
       ### if cluster_intrest:
         ###  map_c_i = cluster_intrest.mapped('total_amount_paid')
      ###     sum_c_i = sum(map_c_i)
     ###   else:
        ###   sum_c_i = 0

        #######
        sheet.write(row, col + 5, _(sum_c_p), cell_format2)
        sheet.write(row, col + 4, _(''), cell_format2)

        origin_paid_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_p_amount = sum(origin_paid_ammount)

        sheet.write(row, col + 3, _(s_o_p_amount), cell_format2)
        origin_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_amount = sum(origin_ammount)
        som_cluster_final_ammount = sum_clus_paid.mapped('final_total')
        s_f_a = sum(som_cluster_final_ammount)


        som_c_i_amount = s_f_a - s_o_amount
        sheet.write(row, col + 2, _(som_c_i_amount), cell_format2)


        sheet.write(row, col + 1, _(s_o_amount), cell_format2)

        row = 3
        col = 0

        sheet.write(row, col + 13, _("البرنامج التجريبي"), cell_format2)
        sheet.write(row, col + 12, _("0"), cell_format2)
        sheet.write(row, col + 11, _("Dollar"), cell_format2)
        sheet.write(row, col + 10, _("10000000"), cell_format2)
        sheet.write(row, col + 10, _("9000"), cell_format2)
        sheet.write(row, col + 9, _("9000"), cell_format2)
        sheet.write(row, col + 8, _("كفيل + شيكات"), cell_format2)
        sheet.write(row, col + 7, _("0"), cell_format2)
        sheet.write(row, col + 6, _("هوية شخصية"), cell_format2)
        paid = self.env['partner.loan.details'].search([("state", "=", 'disburse')])
        if paid:
            sum_clus_paid = paid.filtered(lambda line: line.loan_prog == 'trial')
            map_c_p = sum_clus_paid.mapped('total_amount_paid')
            sum_c_p = sum(map_c_p)
        else:
            sum_c_p = 0
       # cluster_intrest = self.env['partner.loan.installment.details'].search([("state", "=", 'paid')])
       # if cluster_intrest:
        #    map_c_i = cluster_intrest.mapped('total_amount_paid')
         #   sum_c_i = sum(map_c_i)
       # else:
        #    sum_c_i = 0

        #######
        sheet.write(row, col + 5, _(sum_c_p), cell_format2)
        sheet.write(row, col + 4, _(''), cell_format2)

        origin_paid_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_p_amount = sum(origin_paid_ammount)

        sheet.write(row, col + 3, _(s_o_p_amount), cell_format2)
        origin_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_amount = sum(origin_ammount)
        som_cluster_final_ammount = sum_clus_paid.mapped('final_total')
        s_f_a = sum(som_cluster_final_ammount)

        som_c_i_amount = s_f_a - s_o_amount
        sheet.write(row, col + 2, _(som_c_i_amount), cell_format2)

        sheet.write(row, col + 1, _(s_o_amount), cell_format2)

        row = 13
        col = 0
        ###########
        sheet.merge_range('K13:N13', 'تقرير تمويلات الانشطة الزراعية', cell_format)
        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 14
        col = 0
        ###########
        sheet.write(row, col + 13, _("انتاج نباتي"), cell_format2)

        origin_loan_agri = self.env['partner.loan.details'].search([("state", "=", 'disburse'), ("agri_type", "=", 'AG')])
     #   filter_origin_loan_agri = origin_loan_agri.filtered(lambda line: line.agri_type == 'AG')
       # sum_origin_loan_agri = sum(origin_loan_agri)

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        sum_agri_loan_prin = sum(map_origin_loan_agri)

        final_total_amount = origin_loan_agri.mapped('final_total')

        sum_final_total = sum(final_total_amount)


        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)


        sheet.write(row, col + 11, _(sum_final_total), cell_format2)



        sheet.write(row, col + 10, _(final_total_amount), cell_format2)

        ##########################################################


        row = 14
        col = 0
        ###########
        sheet.write(row, col + 13, _("انتاج حيواني"), cell_format2)
        row = 15
        col = 0
        ###########
        sheet.write(row, col + 13, _("تسويق زراعي"), cell_format2)
        row = 16
        col = 0
        ###########
        sheet.write(row, col + 13, _("تصنيع غذائي"), cell_format2)
        row = 17
        col = 0
        ###########
        sheet.write(row, col + 13, _("الات و معدات زراعية"), cell_format2)


















