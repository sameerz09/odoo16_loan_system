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
        sheet.write(row, col + 10, _("أصل المحفظة"), cell_format)
        sheet.write(row, col + 9, _("رصيد المحفظة الحالية"), cell_format)
        sheet.write(row, col + 8, _("نوع الضمانة المقدمة"), cell_format)
        sheet.write(row, col + 7, _("ديون معدومة"), cell_format)
        sheet.write(row, col + 6, _("نوع وثيقة المقترض"), cell_format)
        sheet.write(row, col + 5, _("اجمالي المبالغ المستردة"), cell_format)
        sheet.write(row, col + 4, _("فوائد مستردة"), cell_format)
        sheet.write(row, col + 3, _("أصل مبالغ مستردة"), cell_format)
        sheet.write(row, col + 2, _("فوائد على التمويلات"), cell_format)
        sheet.write(row, col + 1, _("تمويلات ممنوحة"), cell_format)

        #sum_dur_unpaid = self.env['partner.loan.type'].search([('loan_id.id', '=', loaner.id)])
        row = 2
        col = 0
        cluster_wallet = 1999009
        sheet.write(row, col + 13, _("برنامج العناقيد"), cell_format2)
        sheet.write(row, col + 11, _("ILS"), cell_format2)
        sheet.write(row, col + 10, _(cluster_wallet), cell_format2)

        sheet.write(row, col + 8, _("كفيل + شيكات"), cell_format2)
        sheet.write(row, col + 7, _("0"), cell_format2)
        sheet.write(row, col + 6, _("هوية شخصية"), cell_format2)
        paid = self.env['partner.loan.details'].search(['|','|',("state", "=", 'disburse'),("state", "=", '1disburse'),("state", "=", '2disburse')])

        if paid:
           sum_clus_paid = paid.filtered(lambda line: line.loan_prog == 'cluster')
           map_c_p = sum_clus_paid.mapped('total_amount_paid')
           sum_c_p = round(sum(map_c_p), 2)
           map_c_i = sum_clus_paid.mapped('total_interest_amount')
           sum_c_i = round(sum(map_c_i), 2)
           map_c_d = sum_clus_paid.mapped('final_total')
           sum_c_d = round(sum(map_c_d), 2)
           cluster_wallet = 2501665.81


        else:
            sum_c_p = 0
            sum_c_i = 0
            sum_c_d = 0

        c_w_balance = round(cluster_wallet - sum_c_d + sum_c_p, 2)
        sheet.write(row, col + 9, _(c_w_balance), cell_format2)
        cluster_groth_wallet = round(c_w_balance / cluster_wallet, 2)
        sheet.write(row, col + 12, _(cluster_groth_wallet), cell_format2)


        sheet.write(row, col + 5, _(sum_c_p), cell_format2)
        sheet.write(row, col + 4, _(sum_c_i), cell_format2)
        origin_paid_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_p_amount = round(sum(origin_paid_ammount), 2)

        sheet.write(row, col + 3, _(sum_c_p - sum_c_i), cell_format2)
        origin_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_amount = round(sum(origin_ammount), 2)
        som_cluster_final_ammount = sum_clus_paid.mapped('final_total')
        s_f_a = sum(som_cluster_final_ammount)

        som_c_i_amount = round(s_f_a - s_o_amount, 2)
        sheet.write(row, col + 2, _(sum_c_i), cell_format2)

        sheet.write(row, col + 1, _(sum_c_d), cell_format2)

        row = 3
        col = 0
        trial_wallet = 150000


        sheet.write(row, col + 13, _("البرنامج التجريبي"), cell_format2)
        sheet.write(row, col + 12, _("0"), cell_format2)
        sheet.write(row, col + 11, _("Dollar"), cell_format2)
        sheet.write(row, col + 10, _(trial_wallet), cell_format2)
        sheet.write(row, col + 8, _("كفيل + شيكات"), cell_format2)
        sheet.write(row, col + 7, _("0"), cell_format2)
        sheet.write(row, col + 6, _("هوية شخصية"), cell_format2)
        paid = self.env['partner.loan.details'].search(['|','|',("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse')])
        if paid:
            sum_trial_paid = paid.filtered(lambda line: line.loan_prog == 'trial')
            map_t_p = sum_trial_paid.mapped('total_amount_paid')
          #  sum_c_p = sum(map_c_p)
          #  m_t_p = sum_clus_paid.mapped('sum_trial_paid')
            sum_t_p = sum(map_t_p)

            map_t_i = sum_trial_paid.mapped('total_interest_amount')
            sum_t_i = sum(map_t_i)
            map_t_d = sum_trial_paid.mapped('final_total')
            sum_t_d = sum(map_t_d)

        else:
            sum_t_p = 0
            sum_t_i = 0
        #t_w_balance = trial_wallet - sum_t_d + sum_t_p
        t_w_balance = 1120.38
        sheet.write(row, col + 9, _(t_w_balance), cell_format2)
        trial_groth_wallet = round(t_w_balance / trial_wallet,2)
        sheet.write(row, col + 12, _(trial_groth_wallet), cell_format2)



        lonns = self.env['partner.loan.details'].search(['|','|','&',("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'trial')])
        paid_intrest = 0
        for lon in lonns:
            unp_count = self.env['partner.loan.installment.details'].search_count([("loan_id", "=", lon.id), ("state", "=", 'unpaid')])
            p_count = self.env['partner.loan.installment.details'].search_count([("loan_id", "=", lon.id), ("state", "=", 'paid')])
            print('unp_count')
            print(unp_count)
            bis = self.env['partner.loan.installment.details'].search([("loan_id", "=", lon.id), ("state", "=", 'unpaid')], limit=1)
            if bis.loan_id:
               print('Loan Name')
               print(bis.name)
               if p_count != 0:

                   total_interest_paid_amount = bis.interest_amt * p_count

               else:

                 total_interest_paid_amount = 0

            paid_intrest += total_interest_paid_amount


        r_paid_i = round(paid_intrest, 2)
        sheet.write(row, col + 5, _(sum_t_p), cell_format2)
        ###sheet.write(row, col + 4, _(r_paid_i), cell_format2)
        sheet.write(row, col + 4, _(''), cell_format2)


        origin_paid_ammount = sum_clus_paid.mapped('principal_amount')
        ###s_o_p_amount = sum(origin_paid_ammount)
        s_o_p_amount = ''

        sheet.write(row, col + 3, _(''), cell_format2)
        origin_ammount = sum_clus_paid.mapped('principal_amount')
        ###s_o_amount = sum(origin_ammount)
        s_o_amount = ''
        som_cluster_final_ammount = sum_clus_paid.mapped('final_total')
       ### s_f_a = sum(som_cluster_final_ammount)
        s_f_a = ''

        ###som_c_i_amount = s_f_a - s_o_amount
        som_c_i_amount = ''
        sheet.write(row, col + 2, _(sum_t_i), cell_format2)

        sheet.write(row, col + 1, _(sum_t_d), cell_format2)
        #####
        #####
        row = 4
        col = 0
        cluster_wallet = 500000
        sheet.write(row, col + 13, _("البرنامج الموسمي"), cell_format2)
        sheet.write(row, col + 11, _("ILS"), cell_format2)
        sheet.write(row, col + 10, _(cluster_wallet), cell_format2)

        sheet.write(row, col + 8, _("كفيل + شيكات"), cell_format2)
        sheet.write(row, col + 7, _("0"), cell_format2)
        sheet.write(row, col + 6, _("هوية شخصية"), cell_format2)
        paid = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed')])

        if paid:
            sum_clus_paid = paid.filtered(lambda line: line.loan_prog == 'seasonal')
            map_c_p = sum_clus_paid.mapped('total_amount_paid')
            sum_c_p = sum(map_c_p)
            map_c_i = sum_clus_paid.mapped('total_interest_amount')
            sum_c_i = sum(map_c_i)
            map_c_d = sum_clus_paid.mapped('final_total')
            sum_c_d = sum(map_c_d)
            cluster_wallet = 500000


        else:
            sum_c_p = 0
            sum_c_i = 0
            sum_c_d = 0

        c_w_balance = cluster_wallet - sum_c_d + sum_c_p
        sheet.write(row, col + 9, _(c_w_balance), cell_format2)
        cluster_groth_wallet = round(c_w_balance / cluster_wallet, 2)
        sheet.write(row, col + 12, _(cluster_groth_wallet), cell_format2)

        sheet.write(row, col + 5, _(sum_c_p), cell_format2)
        sheet.write(row, col + 4, _(sum_c_i), cell_format2)
        origin_paid_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_p_amount = sum(origin_paid_ammount)

        sheet.write(row, col + 3, _(sum_c_p - sum_c_i), cell_format2)
        origin_ammount = sum_clus_paid.mapped('principal_amount')
        s_o_amount = sum(origin_ammount)
        som_cluster_final_ammount = sum_clus_paid.mapped('final_total')
        s_f_a = sum(som_cluster_final_ammount)

        som_c_i_amount = s_f_a - s_o_amount
        sheet.write(row, col + 2, _(sum_c_i), cell_format2)

        sheet.write(row, col + 1, _(sum_c_d), cell_format2)

        row = 14
        col = 0
        ###########
        sheet.merge_range('K13:N13', 'تقرير تمويلات الأنشطة الزراعية للبرنامج التجريبي (دولار)', cell_format)
        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 15
        col = 0
        ###########
        sheet.write(row, col + 13, _("انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(['|','|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("agri_type", "=", 'AG'), ("loan_prog", "=", 'trial')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ##########################################################

   ##     row = 14
      ##  col = 0
        ###########

        row = 16
        col = 0
        sheet.write(row, col + 13, _("انتاج حيواني"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(['|','|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("agri_type", "=", 'AN'), ("loan_prog", "=", 'trial')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ###########

        row = 17
        col = 0
        sheet.write(row, col + 13, _("تسويق زراعي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(['|','|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("agri_type", "=", 'AM'), ("loan_prog", "=", 'trial')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 18
        col = 0
        sheet.write(row, col + 13, _("تصنيع غذائي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(['|','|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("agri_type", "=", 'FM'), ("loan_prog", "=", 'trial')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 19
        col = 0
        sheet.write(row, col + 13, _("الات ﻭ معدات زراعية"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(['|','|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("agri_type", "=", 'AE'), ("loan_prog", "=", 'trial')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)





        ################################################
        ################################################
        sheet.merge_range('F13:I13', 'تقرير تمويلات الأنشطة الزراعية لبرنامج العناقيد (شيكل)', cell_format)
        row = 14
        col = -5
        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 15
        col = -5
        ###########
        sheet.write(row, col + 13, _("انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'cluster'), ("agri_type", "=", 'AG')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ##########################################################

        ##     row = 14
        ##  col = 0
        ###########

        row = 16
        col = -5
        sheet.write(row, col + 13, _("انتاج حيواني"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'trial'), ("loan_prog", "=", 'cluster'),
             ("agri_type", "=", 'AN')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ###########

        row = 17
        col = -5
        sheet.write(row, col + 13, _("تسويق زراعي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'cluster'),
             ("agri_type", "=", 'AM')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 18
        col = -5
        sheet.write(row, col + 13, _("تصنيع غذائي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'cluster'),
             ("agri_type", "=", 'FM')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 19
        col = -5
        sheet.write(row, col + 13, _("الات ﻭ معدات زراعية"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'), ("loan_prog", "=", 'cluster'), ("agri_type", "=", 'AE')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ##########################################################################################################################
        ##########################################################################################################################
        sheet.merge_range('K22:N22', 'تقرير تمويلات الأنشطة الزراعية للبرنامج الموسمي (شيكل)', cell_format)
        row = 22
        col = 0
        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 23
        col = 0
        ###########
        sheet.write(row, col + 13, _("انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("agri_type", "=", 'AG')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ##########################################################

        ##     row = 14
        ##  col = 0
        ###########

        row = 24
        col = 0
        sheet.write(row, col + 13, _("انتاج حيواني"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("agri_type", "=", 'AN')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        ###########

        row = 25
        col = 0
        sheet.write(row, col + 13, _("تسويق زراعي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("agri_type", "=", 'AM')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 26
        col = 0
        sheet.write(row, col + 13, _("تصنيع غذائي"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("agri_type", "=", 'FM')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###########
        row = 27
        col = 0
        sheet.write(row, col + 13, _("الات ﻭ معدات زراعية"), cell_format2)
        origin_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("agri_type", "=", 'AE')])

        map_origin_loan_agri = origin_loan_agri.mapped('principal_amount')
        tot_fees_interest = origin_loan_agri.mapped('total_interest_amount')
        final_total_amount = origin_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)
        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)
        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ###==================================================================================================

        sheet.merge_range('I30:F30', 'تقرير تمويلات الأنشطة الزراعية حسب المشروع لبرنامج العناقيد (شيكل)', cell_format)
        row = 30
        col = -5

        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 31
        col = -5
        ###########
        sheet.write(row, col + 13, _("محاصيل حقلية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'fc')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 32
        col = -5
        #==============================================================
        sheet.write(row, col + 13, _("خضروات مكشوفة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'ev')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 33
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات زينة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'dp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 34
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات طبية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'mp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 35
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("مشاتل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'nu')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 36
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("بستنه شجريية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'ag')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 37
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'vpr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 38
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("ابقار"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'cp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 39
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("الضأن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'lp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 40
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("الماعز"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'gp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 41
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("الدواجن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'pyp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 42
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("النحل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'bp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 43
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج حيواني"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'apr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 44
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("تراكتور"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'trp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 45
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("ترلة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'tsp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 46
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("تنك"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'tkp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 47
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("محراث"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'pwp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 48
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("حصادة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'cep')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 49
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("فرامة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'chp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 50
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("فرازة عسل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'hs')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 51
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("معصرة زيتون"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'op')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 52
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("معدات تصنيع غذائي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'fpe')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 53
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("حلابات اوتوماتيكية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'am')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 54
        col = -5
        # ==============================================================
        sheet.write(row, col + 13, _("بنية تحتية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'cluster'),
             ("sub_agri_type", "=", 'ip')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        ##==============================================================================================================================
        sheet.merge_range('K30:N30', 'تقرير أنشطة الزراعية حسب المشروع للبرنامج الموسمي (شيكل)', cell_format)
        row = 30
        col = 0

        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 31
        col = 0
        ###########
        sheet.write(row, col + 13, _("محاصيل حقلية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'fc')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 32
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("خضروات مكشوفة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'ev')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 33
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات زينة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'dp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 34
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات طبية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'mp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 35
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("مشاتل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'nu')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 36
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("بستنه شجريية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'ag')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 37
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'vpr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 38
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("ابقار"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'cp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 39
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("الضأن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'lp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 40
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("الماعز"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'gp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 41
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("الدواجن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'pyp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 42
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("النحل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'bp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 43
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج حيواني"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'apr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 44
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("تراكتور"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'trp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 45
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("ترلة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'tsp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 46
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("تنك"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'tkp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 47
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("محراث"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'pwp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 48
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("حصادة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'cep')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 49
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("فرامة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'chp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 50
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("فرازة عسل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'hs')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 51
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("معصرة زيتون"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'op')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 52
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("معدات تصنيع غذائي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'fpe')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 53
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("حلابات اوتوماتيكية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'am')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 54
        col = 0
        # ==============================================================
        sheet.write(row, col + 13, _("بنية تحتية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'),
             ("state", "=", 'closed'),
             ("loan_prog", "=", 'seasonal'),
             ("sub_agri_type", "=", 'ip')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)

        #############################-------------------------------------########################
        sheet.merge_range('A30:D30', 'تقرير أنشطة الزراعية حسب المشروع للبرنامج التجريبي (دولار)', cell_format)
        row = 30
        col = -10

        sheet.write(row, col + 13, _("النشاط"), cell_format2)
        sheet.write(row, col + 12, _("أصل القرض"), cell_format2)
        sheet.write(row, col + 11, _("الفوائد و الأرباح"), cell_format2)
        sheet.write(row, col + 10, _("اجمالي المبلغ"), cell_format2)

        row = 31
        col = -10
        ###########
        sheet.write(row, col + 13, _("محاصيل حقلية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'fc')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 32
        col = -10
        #==============================================================
        sheet.write(row, col + 13, _("خضروات مكشوفة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'ev')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 33
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات زينة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'dp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 34
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("نباتات طبية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'mp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 35
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("مشاتل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'nu')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 36
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("بستنه شجريية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'ag')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 37
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج نباتي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'vpr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 38
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("ابقار"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'cp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 39
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("الضأن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'lp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 40
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("الماعز"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'gp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 41
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("الدواجن"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'pyp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 42
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("النحل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'bp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 43
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("مستلزمات انتاج حيواني"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'apr')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 44
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("تراكتور"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'trp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 45
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("ترلة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'tsp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 46
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("تنك"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'tkp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 47
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("محراث"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'pwp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 48
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("حصادة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'cep')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 49
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("فرامة"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'chp')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 50
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("فرازة عسل"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'hs')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 51
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("معصرة زيتون"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'op')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 52
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("معدات تصنيع غذائي"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'fpe')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 53
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("حلابات اوتوماتيكية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'am')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)
        #############################################################
        row = 54
        col = -10
        # ==============================================================
        sheet.write(row, col + 13, _("بنية تحتية"), cell_format2)

        or_loan_agri = self.env['partner.loan.details'].search(
            ['|', '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse'), ("state", "=", 'closed'),
             ("loan_prog", "=", 'trial'),
             ("sub_agri_type", "=", 'ip')])
        map_origin_loan_agri = or_loan_agri.mapped('principal_amount')
        tot_fees_interest = or_loan_agri.mapped('total_interest_amount')
        final_total_amount = or_loan_agri.mapped('sumation')
        sum_agri_loan_prin = sum(map_origin_loan_agri)
        sum_final_interest = sum(tot_fees_interest)
        sum_final_total = sum(final_total_amount)

        sheet.write(row, col + 12, _(sum_agri_loan_prin), cell_format2)

        sheet.write(row, col + 11, _(sum_final_interest), cell_format2)

        sheet.write(row, col + 10, _(sum_final_total), cell_format2)















