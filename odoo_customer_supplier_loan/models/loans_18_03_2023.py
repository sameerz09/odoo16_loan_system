# -*- coding: utf-8 -*-
import dateutil
import odoo.addons.decimal_precision as dp
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil
import odoo.addons.decimal_precision as dp
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import Warning
from odoo.exceptions import UserError, ValidationError






class EmployeeLoanDetails(models.Model):
    _name = "partner.loan.details"
    _description = "Partner Loan"
    #     _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = "name desc"

    #     def _get_loan_rec(self, cr, uid, ids, context=None):
    #         result = []
    #         for line in self.pool.get('loan.installment.details').browse(cr, uid, ids, context=context):
    #             result.append(line.loan_id.id)
    #         return result

    # @api.multi
    @api.depends('installment_lines', 'principal_amount', 'int_rate', 'dgrace', 'installment_lines.state')
    def _cal_amount_all(self):
        for rec in self:
            rec.total_amount_paid = 0.0
            rec.total_interest_amount = 0.0
            if rec.int_payable:
                if rec.interest_mode == 'flat':
                    rec.total_interest_amount = self. \
                        flat_rate_method(rec.principal_amount, rec.int_rate, rec.dgrace)
                    rec.sumation = rec.principal_amount + rec.total_interest_amount
                    rec.final_total = rec.sumation
                    rec.cus_rec = rec.final_total - rec.total_interest_amount

                elif rec.interest_mode == 'fees':
                    rec.total_interest_amount = self. \
                        fees_rate_method(rec.principal_amount, rec.int_rate, rec.dgrace)
                    rec.sumation = rec.principal_amount + rec.total_interest_amount
                    rec.final_total = rec.sumation - rec.total_interest_amount
                    rec.cus_rec = rec.final_total - rec.total_interest_amount

                #   rec.simulation = self.\
                #     fees_rate_method(rec.principal_amount, rec.int_rate, rec.duration)

                else:
                    if rec.int_rate > 0:
                        values = self.reducing_balance_method(rec.principal_amount, rec.int_rate, rec.dgrace)
                        # for key, value in values.iteritems():
                        for key, value in values.items():
                            rec.total_interest_amount += value['interest_comp']

            for payment in rec.installment_lines:
                #if payment.total == 'paid':
                if payment.paid > 0:
                    rec.total_amount_paid += payment.paid


        # rec.sumation = rec.principal_amount + rec.total_interest_amount
        #  rec.final_total = rec.sumation - rec.total_interest_amount
        #  rec.cus_rec = rec.final_total - rec.total_interest_amount
            rec.total_amount_due = rec.final_total - rec.total_amount_paid

    # @api.multi
    @api.depends('loan_policy_ids')
    def _calc_max_loan_amt(self):
        for rec in self:
            for policy in rec.loan_policy_ids:
                if policy.policy_type == 'maxamt':
                    #                    if policy.max_loan_type == 'basic':
                    #                        if rec.partner_id.contract_id.wage:
                    #                            rec.max_loan_amt = rec.partner_id.contract_id.wage * policy.policy_value / 100
                    #                    elif policy.max_loan_type == 'gross':
                    #                        rec.max_loan_amt = rec.partner_gross * policy.policy_value / 100
                    #                    else:
                    rec.max_loan_amt = policy.policy_value

                    # @api.one

    def _check_multi_loan(self, partner):
        allow_multiple_loans = partner.allow_multiple_loan
        for categ in partner.category_id:
            if categ.allow_multiple_loan:
                allow_multiple_loans = categ.allow_multiple_loan
                break
        return allow_multiple_loans

    # @api.multi
    @api.depends('loan_type')
    def _get_loan_values(self):
        res = {}
        for rec in self:
            allowed_partners = []
            for categ in rec.loan_type.partner_categ_ids:
                allowed_partners += map(lambda x: x.id, categ.partner_ids)
            allowed_partners += map(lambda x: x.id, rec.loan_type.partner_ids)
          #  if rec.partner_id.id in allowed_partners:
            rec.int_rate = rec.loan_type.int_rate
            rec.interest_mode = rec.loan_type.interest_mode
            rec.int_payable = rec.loan_type.int_payable

    @api.model
    def flat_rate_method(self, principal, rate, dgrace):
        return ((principal * rate) / 100 * self.duration / 12)

    @api.model
    def fees_rate_method(self, principal, rate, dgrace):
        return rate

    @api.depends('loan_type')
    def _compute_proof_loan(self):
        for rec in self:
            rec.loan_proof_ids = rec.loan_type.loan_proof_ids

    @api.model
    def reducing_balance_method(self, p, r, n):
        # Determine the interest rate on the loan, the length of the loan and the amount of the loan
        res = {}
        for i in range(0, n):
            step_1_p = p  # principal amount at the beginning of each period
            step_2_r_m = r / (12 * 100.00)  # interest rate per month
            step_3_r_m = 1 + step_2_r_m  # add 1 to interest rate per month
            step_4 = step_3_r_m ** (
                        n - i)  # Raise the step_2_r_m to the power of the number of payments required on the loan
            step_5 = step_4 - 1  # minus 1 from step_4
            step_6 = step_2_r_m / step_5  # Divide the interest rate per month(step_2_r_m) by the step_5
            step_7 = step_6 + step_2_r_m  # Add the interest rate per month to the step_6
            step_8_EMI = round(step_7 * step_1_p, 2)  # Total EMI to pay month
            step_9_int_comp = round(step_1_p * step_2_r_m, 2)  # Total Interest component in EMI
            step_10_p_comp = round(step_8_EMI - step_9_int_comp, 2)  # Total principal component in EMI
            p -= step_10_p_comp  # new principal amount
            res[i] = {'emi': step_8_EMI,
                      'principal_comp': step_10_p_comp,
                      'interest_comp': step_9_int_comp
                      }
        return res

    def unlink(self):
        for loan in self.filtered(lambda loan: loan.state != 'draft'):
            raise UserError(_('You cannot delete loan request which is not in  draft state.'))
        return super(EmployeeLoanDetails, self).unlink()

    def action_disburse(self):
        for data in self:
            if not data.installment_lines:
                raise ValidationError(_("Please Compute installment"))
            else:
                self.write({'state': 'disburse'})

    #    @api.multi
    #    def _check_status(self):
    #        payslip_obj = self.env['hr.payslip']
    #        for loan in self:
    #            if loan.loan_type.disburse_method == 'payroll' and loan.state == 'approved':
    #                payslips = payslip_obj.search([('contract_id', '=', loan.employee_id.contract_id.id),
    #                                             ('date_to', '>=', loan.date_approved),
    #                                             ('date_from', '<=', loan.date_approved)])
    #                for slip in payslips:
    #                    if slip.state == 'done':
    #                        for line in slip.line_ids:
    #                            if line.salary_rule_id.loan_allowance:
    #                                loan.check_status = True
    #                                break
    #                        if loan.check_status:
    #                            self._cr.execute("update employee_loan_details set state='disburse' where id = %s" % (loan.id))
    #                            break
    @api.model
    def _partner_get(self):
        ids = self.env['res.partner'].search([('user_id', '=', self._uid)], limit=1)
        if ids:
            return ids

    name = fields.Char(
        string='Number',
        readonly=True,
      #  default="New",
        copy=False
    )

    fac_id = fields.Char(
        string='Facility ID',
        readonly=True,
        #default="Facility ID",
        copy=False
    )

    #     employee_id = fields.Many2one(
    #         'hr.employee',
    #         string='Employee',
    #         required=True,
    #         readonly=True,
    #         states={'draft':[('readonly', False)]},
    #         default=_employee_get
    #     )
    employee_id = fields.Many2one('hr.employee', string='Employee responsible',
                                  required=True)

    no_paym = fields.Selection(
        selection=[('1', 'One Payment'),
                   ('2', 'Two Payments'),
                   ('3', 'Three Payments'),
                   ],
        default='1',
        string='Number Of Payments',
        # default="1",
        # stored=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=_partner_get
    )


    guarantor_id = fields.Many2one(
        'res.partner',
        string='Garantor',
        required=True,
        readonly=True,
    #    states={'draft': [('readonly', False)]},
        default=_partner_get
    )

    first_payment = fields.Float(
        string='First Disburse',
        required= True,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        help='Payment Number.'
    )
    seconed_payment = fields.Float(
        string='Second Disburse',
        required=True,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        help='Payment Number.'
    )
    third_payment = fields.Float(
        string='Third Disburse',
        required=True,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        help='Payment Number.'
    )
    first_dis_date = fields.Date(
        string='First Disburse Date',
        readonly=False,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        copy=False
    )
    second_dis_date = fields.Date(
        string='Second Disburse Date',
        readonly=False,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        copy=False
    )
    third_dis_date = fields.Date(
        string='Third Disburse Date',
        readonly=False,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        copy=False
    )

    #     department_id = fields.Many2one(
    #         'hr.department',
    #         string="Department",
    #         states={'paid':[('readonly', True)], 'disburse':[('readonly', True)], 'approved':[('readonly', True)]},
    #     )
    date_applied = fields.Date(
        string='Applied Date',
        required=True,
        readonly=False,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        #  default=fields.Date.context_today
    )
    date_approved = fields.Date(
        string='Approved Date',
        readonly=True,
        copy=False
    )
    date_repayment = fields.Date(
        string='Repayment Date',
        readonly=False,
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)], 'approved': [('readonly', True)]},
        copy=False
    )
    date_disb = fields.Date(
        string='Disbursement Date',
        readonly=False,
        default=fields.Date.today(),
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)]}
    )

    actual_grant_date = fields.Date(
        string='Actual Grant Date',
        readonly=False,
        default=fields.Date.today()
    )

    date_disb_grace = fields.Date(
        string='Disbursement with Grace Date ',
        readonly=False,
        default=fields.Date.today(),
        states={'paid': [('readonly', True)], 'disburse': [('readonly', True)]}
    )
    loan_type = fields.Many2one(
        'partner.loan.type',
        string='Interest Type',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    duration = fields.Integer(
        string='Duration(Months)',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    dgrace = fields.Integer(
        string='Grace Duration(Months)',
        store=True,
        required=True,
        readonly=False

    )


    loan_policy_ids = fields.Many2many(
        'partner.loan.policy',
        'loan_policy_rel',
        'policy_id',
        'loan_id',
        string="Active Policies",
        states={'disburse': [('readonly', True)]}
    )
    int_payable = fields.Boolean(
        compute='_get_loan_values',
        #         multi='type',
        string='Is Interest Payable',
        store=True,
        default=True
    )
    interest_mode = fields.Selection(
        compute='_get_loan_values',
        selection=[('flat', 'Flat'), ('reducing', 'Reducing'), ('fees', 'Operation Fees')],
        #         multi='type',
        string='Interest Mode',
        store=True,
        default=''
    )
    int_rate = fields.Float(
        compute='_get_loan_values',
        string='Rate',
        multi='type',
        help='Interest rate between 0-100 in range',
        digits=(16, 2),
        store=True
    )
    principal_amount = fields.Float(
        string='Principal Amount',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    partner_gross = fields.Float(
        string='Gross Salary',
        help='Partner Gross Salary from Payslip if payslip is not available please enter value manually.',
        required=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    sumation = fields.Float(
        compute='_cal_amount_all',
        string='Total Loan With Fees Cost',
        store=True
    )
    final_total = fields.Float(
        compute='_cal_amount_all',
        string='Total Loan After Fees Deductions',
        store=True
    )
    cus_rec = fields.Float(
        compute='_cal_amount_all',
        string='Customer Amount Recieved',
        store=True
    )
    total_amount_paid = fields.Float(
        compute='_cal_amount_all',
        #         multi="calc",
        string='Received From Partner',
        store=True
    )

    total_interest_amount = fields.Float(
        compute='_cal_amount_all',
        string='Total Fees On Loan',
        store=True
    )
    max_loan_amt = fields.Float(
        compute='_calc_max_loan_amt',
        store=True,
        string='Max Loan Amount'
    )
    installment_lines = fields.One2many(
        'partner.loan.installment.details',
        'loan_id',
        'Installments',
        copy=False
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        readonly=True,
        # states={'draft':[('readonly', False)]},
        default=lambda self: self.env.user.company_id.currency_id
    )
    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user,
        string='User',
        readonly=True,
        required=True,
    )
    partner_loan_account = fields.Many2one(
        'account.account',
        string='Borrower Loan Account',
        #        string="Partner Account",
        readonly=False,
        #        states={'disburse':[('readonly', True)]}
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Disburse Journal',
        help='Journal related to loan for Accounting Entries',
        required=False,
        readonly=False,
        states={'disburse': [('readonly', True)]}
    )
    journal_id1 = fields.Many2one(
        'account.journal',
        string='Loan Repayment Journal',
        required=False,
        readonly=False,
        states={'close': [('readonly', True)]}
    )
    journal_id2 = fields.Many2one(
        'account.journal',
        string='Interest Journal',
        required=False,
        readonly=False,
    )
    move_id = fields.Many2one(
        'account.move',
        string='Disburse Journal Entry',
        readonly=True,
        help='Accounting Entry once loan has been given to Partner',
        copy=False
    )
    loan_proof_ids = fields.Many2many(
        'partner.loan.proof',
        compute='_compute_proof_loan',
        string='Loan Proofs',
    )
    #    check_status = fields.Boolean(
    #        compute='_check_status',
    #        string='Check Status',
    #        store=True
    #    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('applied', 'Applied'),
            ('approved', 'Approved'),
            ('paid', 'Paid'),
            ('1disburse', 'First Disburse'),
            ('2disburse', 'Second Disburse'),
            ('disburse', 'Disbursed'),
            ('rejected', 'Rejected'),
            ('closed', 'Closed'),
            ('cancel', 'Cancelled')],
        string='State',
        readonly=True,
        copy=False,
        default='draft',
        track_visibility='onchange',
    )
    grace_period = fields.Selection(
        selection=[
            ('0', 'No Grace'),
            ('1', 'one month'),
            ('2', 'two months'),
            ('3', 'three months'),
            ('4', 'four months'),
            ('5', 'five months'),
            ('6', 'six months')],
        string='Grace period',
        readonly=False,
        copy=False,
        default='0',
    )
    org_fund = fields.Selection(
        selection=[
            ('gov', 'Government Funding'),
            ('external', 'External Funding')
        ],
        string='Funding Source',
        default='gov',
        readonly=False,
        copy=False,
        required=True,
    )
    organ = fields.Selection(
        selection=[
            ('ifad', 'IFAD'),
            ('external', 'OXFAM'),
            ('gov', 'governmental'),
        ],
        string='Financier Name',
        states={'draft': [('readonly', False)]},
        copy=False,
        required=False,
    )
    notes = fields.Text(
        string='Note'
    )
    total_amount_due = fields.Float(

        help='Remaining Amount due.',
        string='Balance on Loan',
        store=True
    )

    loan_partner_type = fields.Selection(
        selection=[('customer', 'Customer'),
                   ('supplier', 'Supplier'),
                   ],
        string='Loan Partner Type',
        default="customer",
    )
    loan_class = fields.Selection(
        selection=[('islamic', 'Islamic'),
                   ('commercial', 'Commercial'),
                   ],
        string='Loan Classification',

    )
    curr = fields.Selection(
        selection=[('0', ''),
                   ('1', 'Dollar'),
                   ('2', 'Shekel'),
                   ],
        string='Currency',

    )
    loan_prog = fields.Selection(
        selection=[('trial', 'Trial'),
                   ('cluster', 'Cluster Program'),
                   ('seasonal', 'Seasonal'),
                   ],
        string='Loan Program',

    )
    disbursed_account_id = fields.Many2one(
        'account.account',
        string='Disburse Account',
        related="journal_id.default_credit_account_id",
        stored=True,
    )
    interest_receivable_account_id = fields.Many2one(
        'account.account',
        string='Interest Receivable Account',

    )
    interest_account_id = fields.Many2one(
        'account.account',
        string='Interest Account',
        related="journal_id2.default_credit_account_id",
        stored=True,
    )
    interest_loan_journal = fields.Many2one(
        'account.move',
        'Interest On Loan Journal Entry',
        readonly=True,
        copy=False,
    )
    governorate = fields.Selection(
        selection=[('JN', 'Jenin'),
                   ('NJ', 'North Jenin'),
                   ('TS', 'Tubas'),
                   ('TM', 'Tulkarm'),
                   ('NS', 'Nablus'),
                   ('QA', 'Qalqilya'),
                   ('ST', 'Salfit'),
                   ('RH', 'Ramallah'),
                   ('JO', 'Jericho'),
                   ('JM', 'Jerusalem'),
                   ('BM', 'Bethlehem'),
                   ('HN', 'Hebron'),
                   ('NH', 'North Hebron'),
                   ('SH', 'Soutch Hebron'),
                   ('YA', 'Yuta'),
                   ('NA', 'North Gaza'),
                   ('GA', 'Gaza'),
                   ('DH', 'Deir al-Balah'),
                   ('KS', 'Khan Yunis'),
                   ('RA', 'Rafah'),
                   ('NV', 'Northern Valley')
                   ],
        string='Governorate',
        required=True,

    )
    agri_type = fields.Selection(
        selection=[('AG', 'agricultural'),
                   ('AN', 'animal'),
                   ('FM', 'food manufacturing'),
                   ('AE', 'agricultural equipment'),
                   ('AM', 'agricultural marketing'),
                   ],
        string='Project Type',
        required=True,

    )
    sub_agri_type = fields.Selection(
        selection=[('fc', 'محاصيل حقلية'),
                   ('ev', 'خضروات مكشوفة'),
                   ('pv', 'خضروات محمية'),
                   ('dp', 'نباتات زينة'),
                   ('mp', 'نباتات طبية'),
                   ('nu', 'مشاتل'),
                   ('ag', 'بستنه شجريية'),
                   ('vpr', 'مستلزمات انتاج نباتي'),
                   ('cp', 'ابقار'),
                   ('lp', 'الضأن'),
                   ('gp', 'الماعز'),
                   ('pyp', 'الدواجن'),
                   ('bp', 'النحل'),
                   ('apr', 'مستلزمات انتاج حيواني'),
                   ('trp', 'تراكتور'),
                   ('tsp', 'ترلة'),
                   ('tkp', 'تنك'),
                   ('pwp', 'محراث'),
                   ('cep', 'حصادة'),
                   ('chp', 'فرامة'),
                   ('hs', 'فرازة عسل'),
                   ('op', 'معصرة زيتون'),
                   ('fpe', 'معدات تصنيع غذائي'),
                   ('am', 'حلابات اوتوماتيكية'),
                   ('ip', 'بنية تحتية'),
                   ],
        string='مشاريع فرعية',
        default='fc',
        required=True,

    )
    duration = fields.Integer(
        string='Duration(Months)',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    resch_times = fields.Integer(
        string='Number of rescheduling times',
        required=True,
        readonly=True,
        default=0,
    )
    aging1 = fields.Float(
        string='31 to 90 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
       # compute='_get_line_ids',
        store=True,
        default=0,
        #    store=True
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )
    aging2 = fields.Float(
        string='91 to 180 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_customer_name',
        default=0,
        #   store=True
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )
    aging3 = fields.Float(
        string='181 to 270 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_customer_name',
        default=0,
        #    store=True
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )
    aging4 = fields.Float(
        string='271 to 360 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_customer_name',
        default=0,
        #    store=True
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )



    class_comp = fields.Selection(
        selection=[('1', 'Regular'),
                   ('2', 'Under Suerveillance'),
                   ('3', 'Below The Level'),
                   ('4', 'Doubtful Debts'),
                   ('5', 'Losses'),
                   ],
        string='Compliance Classification',
        readonly=True,
        required=True,
        default = '1'

    )
    disburse_remains = fields.Float(
        string='Remains of Disbursment',
        required=True,
        readonly=True,
        default=0,
    )
    disburse_times = fields.Integer(
        string='Number of disbursment times',
        required=True,
        readonly=True,
        default=0,
    )

    @api.onchange('loan_prog', 'principal_amount')
    def _get_intrest(self):
        for sheet in self:

            if sheet.loan_prog == 'cluster' and sheet.principal_amount <= 10000:
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'c01')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 500,
                })

            elif sheet.loan_prog == 'cluster' and sheet.principal_amount > 10000 and sheet.principal_amount <= 30000:
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'c02')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 1500,
                })


            elif sheet.loan_prog == 'cluster' and sheet.principal_amount > 30000 and sheet.principal_amount <= 50000:
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'c03')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 3000,
                })



            elif sheet.loan_prog == 'cluster' and sheet.principal_amount > 50000:
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'c04')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 4000,
                })



            elif sheet.loan_prog == 'trial':
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'HL01')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 3,
                })

            elif sheet.loan_prog == 'seasonal' and sheet.principal_amount == 10000:
                loan_t = self.env['partner.loan.type'].search([('code', '=', 'se01')])
                sheet.update({
                    'loan_type': loan_t,
                    'int_rate': 300,
                })
            for paym in self:
                if paym.no_paym == '1':
                    paym.first_payment = paym.principal_amount

    # @api.onchange('curr')
    # def _get_currenc(self):

    #  if self.curr == "1":
    # user = 2
    #      nstate = {
    #       "company_id": 1,
    #   }
    # ser = self.env['res.users'].browse([('id', '=', 2)])
    # ser.write(nstate)
    #      oerp = oerplib.OERP(server='localhost', database='paci', protocol='xmlrpc')
    #    user_model = oerp.get('res.users')
    #    user_model.write([1], {'company_id': 1})

    #   else:
    ##  oerp = oerplib.OERP(server='localhost', database='paci', protocol='xmlrpc')
    ##  user_model = oerp.get('res.users')
    # # user_model.write([1], {'company_id': 2})
    #  user = 2
    #   nstate = {
    #    "company": 2,
    # }

    @api.onchange('grace_period', 'duration')
    def _get_graceperiod(self):
        for sheet in self:
           # print(sheet.grace_period)
            if sheet.grace_period == '0':
                sheet.dgrace = sheet.duration - 0
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=0)
            elif sheet.grace_period == '1' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 1
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=1)
            elif sheet.grace_period == '2' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 2
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=2)
            elif sheet.grace_period == '3' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 3
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=3)

            elif sheet.grace_period == '4' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 4
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=4)
             #   print(self.date_disb_grace)
            elif sheet.grace_period == '5' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 5
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=5)
            elif sheet.grace_period == '6' and sheet.duration > 0:
                sheet.dgrace = sheet.duration - 6
                self.date_disb_grace = self.date_disb + dateutil.relativedelta.relativedelta(months=6)

    #     @api.one
    #     def copy(self, default=None):
    #         if not default:
    #             default = {}
    #         default.update({
    #             'installment_lines': [],
    #             'date_approved': False,
    #             'date_repayment': False,
    #             'name':False,
    #             'move_id':False,
    #             'state': 'draft'
    #         })
    #         return super(EmployeeLoanDetails, self).copy(default)

    # @api.multi
    ###  # not qulify hashed
    def onchange_loan_type(self, loan_type, partner):
        if loan_type:
            if not partner:
                raise Warning(_('Please specify partner.'))
        loan_type = self.env['partner.loan.type'].browse(loan_type)
        partner_obj = self.env['res.partner'].browse(partner)
        allowed_partners = []
        for categ in loan_type.partner_categ_ids:
            allowed_partners += map(lambda x: x.id, categ.partner_ids)
            allowed_partners += map(lambda x: x.id, loan_type.partner_ids)
        if partner not in allowed_partners:
            raise Warning(_('%s  does not Qualify for %s ') % (partner_obj.name, loan_type.name))
        return {}

    # @api.multi
    def onchange_employee_id(self, partner):
        if not partner:
            return {'value': {'loan_policy_ids': []}}
        partner_obj = self.env['res.partner'].browse(partner)
        policies_on_categ = []
        policies_on_empl = []
        for categ in partner_obj.category_id:
            if categ.loan_policy:
                policies_on_categ += map(lambda x: x.id, categ.loan_policy)
        if partner_obj.loan_policy:
            policies_on_empl = map(lambda x: x.id, partner_obj.loan_policy)
        #         domain = [('partner_id', '=', partner), ('contract_id', '=', partner_obj.contract_id.id), ('code', '=', 'GROSS')]
        #         line_ids = self.env['hr.payslip.line'].search(domain)
        #         department_id = partner_obj.department_id.id or False  #todo check
        department_id = False
        address_id = partner_obj or False
        if not address_id:
            raise Warning(_('There is no home/work address defined for partner : %s ') % (_(partner_obj.name)))
        partner_id = address_id and address_id.id or False
        if not partner_id:
            raise Warning(_('There is no partner defined for partner : %s ') % (_(partner_obj.name)))
        gross_amount = 0.0
        #         if line_ids:
        # #             line = self.env['hr.payslip.line'].browse(line_ids)[0]
        #             line = line_ids[0]
        #             gross_amount = line.amount
        return {'value': {'department_id': department_id,
                          'loan_policy_ids': list(set(policies_on_categ + policies_on_empl)),
                          'partner_gross': gross_amount,
                          'partner_loan_account': address_id.property_account_receivable_id.id or False}}

    # probuse override to fix issue of  when we apply for a loan first loan policy is selected and when we save loan request the loan policy get removed/disappeared and we have to select loan policy again
    @api.model
    def create(self, vals):
        if vals.get('partner_id', False):
            partner_id = vals['partner_id']
            partner = self.env['res.partner'].sudo().browse(partner_id)

            policies_on_categ = []
            policies_on_empl = []
            for categ in partner.category_id:
                if categ.loan_policy:
                    policies_on_categ += map(lambda x: x.id, categ.loan_policy)
            if partner.loan_policy:
                policies_on_empl += map(lambda x: x.id, partner.loan_policy)

            loan_policy_ids = list(set(policies_on_categ + policies_on_empl))
            vals.update({'loan_policy_ids': [(6, 0, loan_policy_ids)]})
       ## if self.loan_prog == 'trial':
         ##   self.update({'int_payable': False})
       ## else:
       ##     self.update({'int_payable': True})


        return super(EmployeeLoanDetails, self).create(vals)

    # @api.multi
    def action_applied(self):
        for loan in self:
            #  ## self.onchange_loan_type(loan.loan_type.id, loan.partner_id.id)
            msg = ''
            if loan.principal_amount <= 0.0:
                msg += 'Principal Amount\n '
            #            if loan.int_payable and loan.int_rate <= 0.0:
            #                msg += 'Interest Rate\n '
            if loan.duration <= 0.0:
                msg += 'Duration of Loan'
            if msg:
                raise Warning(_('Please Enter values greater then zero:\n %s ') % (msg))
            status = self.check_employee_loan_qualification(loan)
            if not isinstance(status, bool):
                raise Warning(_('Loan Policies not satisfied :\n %s ') % (_(status)))
            seq_no = self.env['ir.sequence'].next_by_code('partner.loan.details')
            fac_seq_no = seq_no
            gov = str(self.governorate)
            type = str(self.agri_type)
            year = loan.date_disb.strftime("%Y")
            # seq_no = self.loan_id.name
            #             self.write({'state':'applied', 'name':seq_no})
            loan.state = 'applied'
            #   loan.name = ("% s/% s/% s"%(seq_no,gov,type))
            loan.name = ("% s/% s/% s/% s" % ('LOAN', seq_no, gov, type))
            loan.fac_id = ("% s" % (fac_seq_no))
        return True

    # @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_report(self):
        return self.env.ref('odoo_customer_supplier_loan.partner_loan_report_analysis_regg').report_action(self)

    #         return self.write({'state':'cancel'})

    @api.model
    def check_employee_loan_qualification(self, loan_obj):
        loan_date_today = loan_obj.date_applied
        loan_date_today_obj = datetime.strptime(str(loan_date_today), DEFAULT_SERVER_DATE_FORMAT)
        msg = 'Mr./Mrs. %s does not meet following Loan policies:' % (loan_obj.partner_id.name)
        qualified = True
        allow_multiple_loan = self._check_multi_loan(loan_obj.partner_id)
        allow_multiple_loan = filter(None, [allow_multiple_loan])  # probuse
        if loan_obj.partner_id.loan_defaulter:
            msg += '\n Blacklisted: You are Blacklisted as loan defaulter and hence you cannot apply for a new loan !'
            qualified = False
        if not allow_multiple_loan:
            loans_list = self.search([('state', '=', 'disburse'), ('partner_id', '=', loan_obj.partner_id.id)],
                                     order='date_applied asc')
            if len(loans_list):
                msg += '\n Multiple loan: Multiple loan is not allowed !'
                qualified = False
        for policy in loan_obj.loan_policy_ids:
            if policy.policy_type == 'maxamt':
                if loan_obj.max_loan_amt > 0.0 and loan_obj.principal_amount > loan_obj.max_loan_amt:
                    qualified = False
                    msg += '\n %s :Loan amount is > %s ' % (policy.name, loan_obj.max_loan_amt)

            #             if policy.policy_type == 'loan_gap' and not allow_multiple_loan: #probuse
            if policy.policy_type == 'loan_gap' and allow_multiple_loan:
                loans_list = self.search([('state', '=', 'disburse'), ('partner_id', '=', loan_obj.partner_id.id)],
                                         order='date_applied asc')
                if loans_list:
                    #                     last_loan = self.browse(loans_list[0]) #probuse
                    last_loan = loans_list[0]  # probuse
                    last_loan_date = last_loan.date_applied
                    last_loan_date_obj = datetime.strptime(last_loan_date.strftime('%Y-%m-%d'),
                                                           DEFAULT_SERVER_DATE_FORMAT)
                    # last_loan_date_obj = datetime.strptime(str(last_loan_date), DEFAULT_SERVER_DATE_FORMAT)
                    diff = last_loan_date_obj + relativedelta(months=int(policy.policy_value))
                    if diff > loan_date_today_obj:
                        qualified = False
                        msg += '\n %s :\n\t\t Last loan date: %s \n\t\tGap required(months) : %s \n\t\tcan apply on/after: %s' \
                               % (policy.name, last_loan_date, policy.policy_value, diff.strftime('%Y-%m-%d'))
        #            if policy.policy_type == 'eligible_duration':
        #                contract_date = loan_obj.partner_id.contract_id.date_start
        #                contract_date_obj = datetime.strptime(contract_date, DEFAULT_SERVER_DATE_FORMAT)
        #                actual_date = contract_date_obj + relativedelta(months=int(policy.policy_value))
        #                if actual_date > loan_date_today_obj:
        #                    qualified = False
        #                    msg += '\n %s :\n\t\tContract date: %s  \n\t\tGap required(months):%s \n\t\tcan apply on/after: %s'\
        #                            % (policy.name, contract_date, policy.policy_value, actual_date.strftime('%Y-%m-%d'))
        if not qualified:
            return msg
        return qualified

    ##@api.model
    ## sameer uncoment this method @api.multi on 11-11-2022
    def compute_installments(self):
        for loan in self:
            # loan.installment_lines.unlink()
            if not len(loan.installment_lines):
                self.create_installments(loan)
            elif loan.state == 'applied':
                loan.installment_lines.unlink()
                self.create_installments(loan)
            elif self._context.get('recompute') and loan.int_payable:
                access_payment = 0.0
                duration_left = 0
                prin_amt_received = 0.0
                total_acc_pay = 0.0
                for install in loan.installment_lines:
                    access_payment += round(install.total - (install.principal_amt + install.interest_amt), 2)
                    if install.state in ('paid', 'approve'):
                        prin_amt_received += round(install.principal_amt, 2)
                        continue
                    duration_left += 1
                total_acc_pay = loan.dgrace - duration_left
                new_p = round(loan.principal_amount - round(prin_amt_received, 2) - round(access_payment, 2))
                if loan.interest_mode == 'reducing':
                    if loan.int_rate > 0:
                        reducing_val = self.reducing_balance_method(new_p, loan.int_rate, duration_left)
                if loan.interest_mode == 'flat':
                    interest_amt = 0.0
                    principal_amt = new_p / duration_left
                    if loan.int_payable:
                        interest_amt = self.flat_rate_method(new_p, loan.int_rate, duration_left) / duration_left
                    #  total = principal_amt + interest_amt
                    total = principal_amt
                    # total = 0
                cnt = -1
                if loan.interest_mode == 'fees':
                    interest_amt = 0.0
                    principal_amt = new_p / duration_left
                    if loan.int_payable:
                        interest_amt = 0
                    total = principal_amt
                # total = 0

                cnt = -1
                for install in loan.installment_lines:
                    cnt += 1
                    if install.state in ('paid', 'approve'): continue
                    ##     if loan.interest_mode == 'reducing':
                    if loan.interest_mode:
                        principal_amt = reducing_val[cnt - total_acc_pay]['principal_comp']
                        if loan.int_payable:
                            interest_amt = reducing_val[cnt - total_acc_pay]['interest_comp']
                        total = principal_amt + interest_amt
                    #  total = 0

                    install.write({'principal_amt': principal_amt,
                                   'interest_amt': interest_amt,
                                   'total': total,
                                   })
            else:

                # this is to reload the values
                interest_amt = 0
                total_remains = 0.0
                loan.write({})
                for install in loan.installment_lines:
                    if install.state in ('paid'):
                       total_remains = install.remains
                       total_remains = 0
                    else:
                        install.write({'remains': ((install.principal_amt + install.interest_amt) + total_remains) - install.total,
                                       'tot_sum': install.principal_amt + install.interest_amt,
                                       'tot_due': (install.principal_amt + install.interest_amt) + total_remains})
                        total_remains = 0
        return True

    @api.model
    def create_installments(self, loan):
        date_approved = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        if not loan.date_disb:
            raise Warning(_('Please give disbursement date.'))
        else:
            date_disb_grace = loan.date_disb_grace


        date_approved_obj = datetime.strptime(str(date_disb_grace), DEFAULT_SERVER_DATE_FORMAT)
      #  print(date_disb_grace)
        installment_obj = self.env['partner.loan.installment.details']
        day = date_approved_obj.day
        month = date_approved_obj.month
        year = date_approved_obj.year
        interest_amt = 0.0
        principal_amt = loan.principal_amount / (loan.dgrace or 1.0)
        if loan.int_payable:
            interest_amt = loan.total_interest_amount / (loan.dgrace or 1.0)
        total = principal_amt + interest_amt
        # total = principal_amt + interest_amt
        ## total = principal_amt + interest_amt
        if loan.interest_mode == 'fees':
            interest_amt = 0
            # total = principal_amt + interest_amt
            total = 0
            tot_sum = principal_amt + interest_amt
            remains = 0
        if loan.interest_mode == 'reducing':
            if loan.int_rate > 0.0:
                reducing_val = self.reducing_balance_method(loan.principal_amount, loan.int_rate, loan.dgrace)
        for install_no in range(0, loan.dgrace):
            date_from = datetime(year, month, day)
            date_to = date_from + relativedelta(months=1)
            if loan.interest_mode == 'reducing':
                if loan.int_rate > 0.0:
                    principal_amt = reducing_val[install_no]['principal_comp']
                #                if loan.int_payable:
                if loan.int_payable and loan.int_rate > 0.0:
                    interest_amt = reducing_val[install_no]['interest_comp']
                    ###  total = principal_amt + interest_amt
                    total = 0
                    tot_sum = principal_amt + interest_amt
                    remains = 0

            day, month, year = date_to.day, date_to.month, date_to.year
            installment_line = {'install_no': install_no + 1,
                                'date_from': date_from.strftime('%Y-%m-%d'),
                                'date_to': date_to.strftime('%Y-%m-%d'),
                                'principal_amt': principal_amt,
                                'interest_amt': interest_amt,
                                'tot_sum': principal_amt + interest_amt,
                                'total': 0,
                                'tot_due': principal_amt + interest_amt,
                                'remains': principal_amt + interest_amt,
                                'loan_id': loan.id
                                }
            installment_obj.create(installment_line)

        return True

    # @api.multi
    def _interest_journal(self, loan, move_inrest, vals, partner_id, move_pool):
        interest_move = move_inrest
        # the below loan.journal_id2 is fake variable
        loan.journal_id2 = 1
        if not loan.journal_id2:
            raise Warning(_('Please configure Interest Journal.'))
        if not loan.interest_account_id:
            raise Warning(
                _('Please configure Debit/Credit accounts on the Interest Journal %s ') % (loan.journal_id2.name))
        credit_account_id = loan.interest_account_id.id
        ## the below debit_account_id must be enabled when we are go into accounting
        #   debit_account_id = loan.interest_receivable_account_id.id or False
        ##the below debit_account_id must be deleted because its added manually when we are go into accounting
        debit_account_id = 1
        if not debit_account_id:
            raise Warning(_('Please configure debit account of Interest'))

        debit_line = (0, 0, {
            'name': _('Loan of %s') % (loan.name),
            'date': loan.date_disb_grace,
            'partner_id': partner_id,
            'account_id': debit_account_id,
            'journal_id': loan.journal_id2.id,
            'debit': loan.total_interest_amount,
            'credit': 0.0,
        })
        credit_line = (0, 0, {
            'name': _('Loan of %s') % (loan.name),
            'date': loan.date_disb_grace,
            'partner_id': partner_id,
            'account_id': credit_account_id,
            'journal_id': loan.journal_id2.id,
            'debit': 0.0,
            'credit': loan.total_interest_amount,
        })
        interest_move.update({'line_ids': [debit_line, credit_line]})
        interest_loan_journal_id = move_pool.create(interest_move)
        date_disb_grace = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        if not loan.date_disb:
            vals.update(state='disburse', interest_loan_journal=interest_loan_journal_id.id,
                        date_disb_grace=date_disb_grace)
        else:
            vals.update(state='disburse', interest_loan_journal=interest_loan_journal_id.id)
        return vals

    # @api.multi
    def action_disburse(self):
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for loan in self:
            if loan.loan_type.disburse_method == 'payroll':
                loan.write({'state': 'disburse'})
                return True
            vals = {}
            #             period_id = period_pool.find(loan.date_applied)[0]
            timenow = time.strftime('%Y-%m-%d')
            address_id = loan.partner_id or False
            partner_id = address_id and address_id and address_id.id or False

            if not partner_id:
                raise Warning(_('Please configure Home Address On partner.'))

            move = {
                'narration': loan.name,
                'date': loan.date_disb_grace,
                'ref': loan.name,
                'journal_id': loan.journal_id.id,
                #                 'period_id': period_id.id,
            }
            move_inrest = {
                'narration': loan.name,
                'date': loan.date_disb_grace,
                'ref': loan.name,
                'journal_id': loan.journal_id2.id,
                #                 'period_id': period_id.id,
            }
            ##the below added manualy when go to accounting please delete it
            loan.journal_id = 1
            credit_account_id = loan.journal_id.default_credit_account_id
            if not loan.journal_id:
                raise Warning(_('Please configure Disburse Journal.'))
            if not credit_account_id:
                raise Warning(_('Please configure Debit/Credit accounts on the Journal %s ') % (loan.journal_id.name))
            credit_account_id = credit_account_id.id
            # debit_account_id = loan.partner_loan_account.id or False
            ##the below added manualy when go to accounting please delete it
            debit_account_id = 1
            #       if not debit_account_id:
            #   raise Warning(_('Please configure debit account of partner'))

            debit_line = (0, 0, {
                'name': _('Loan of %s') % (loan.name),
                'date': loan.date_disb_grace,
                'partner_id': partner_id,
                'account_id': debit_account_id,
                'journal_id': loan.journal_id.id,
                #                     'period_id': period_id.id,
                'debit': loan.principal_amount,
                'credit': 0.0,
            })
            credit_line = (0, 0, {
                'name': _('Loan of %s') % (loan.name),
                'date': loan.date_disb_grace,
                'partner_id': partner_id,
                'account_id': credit_account_id,
                'journal_id': loan.journal_id.id,
                #                     'period_id': period_id.id,
                'debit': 0.0,
                'credit': loan.principal_amount,
            })
            if loan.int_rate > 0.0:
                vals = self._interest_journal(loan, move_inrest, vals, partner_id, move_pool)

            move.update({'line_ids': [debit_line, credit_line]})
            move_id = move_pool.create(move)
            date_disb_grace = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if not loan.date_disb_grace:
                vals.update(state='disburse', move_id=move_id.id, date_disb_grace=date_disb_grace)
            else:
                vals.update(state='disburse', move_id=move_id.id)
            loan.write(vals)
        #             if loan.journal_id.entry_posted:#todoprobuse
        #             move_id.post()
        return True

    # @api.multi
    def action_approved(self):
        date_approved = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        date_approved_obj = datetime.strptime(date_approved, DEFAULT_SERVER_DATE_FORMAT)
        for loan in self:
            vals = {}
            if not loan.date_approved:
                vals.update(
                    date_approved=date_approved,
                    state='approved')
            else:
                vals.update(state='approved')

            self.write(vals)

        for data in self:
            if not data.installment_lines:
                raise ValidationError(_("Please Compute installment"))
            else:
                self.write({'state': 'approved'})

        return True

    # @api.multi
    def action_rejected(self):
        for rec in self:
            rec.state = 'rejected'

    #         return self.write({'state':'rejected'})

    # @api.multi
    def action_paid(self):
        for rec in self:
            rec.state = 'paid'

    # @api.multi
    def action_reset(self):
        #         self.write({'state':'draft'})
        for rec in self:
            rec.state = 'applied'


#         from openerp import workflow
#         workflow.trg_delete(self._uid, self._name, self.id, self._cr)
#         workflow.trg_create(self._uid, self._name, self.id, self._cr)
# #        self.workflow_delete()
# #        self.workflow_create()
#         return True
