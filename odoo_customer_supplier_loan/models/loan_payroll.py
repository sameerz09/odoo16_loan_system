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



# import oerplib
# import xmlrpc


# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#     _inherit = 'hr.employee'

#     def get_installment_loan(self, part_id, date_from, date_to=None):
#         if date_to is None:
#             date_to = datetime.now().strftime('%Y-%m-%d')
#         self._cr.execute("SELECT sum(o.principal_amt) from loan_installment_details as o where \
#                             o.partner_id=%s \
#                             AND to_char(o.date_from, 'YYYY-MM-DD') >= %s AND to_char(o.date_from, 'YYYY-MM-DD') <= %s ",
#                             (part_id, date_from, date_to))
#         res = self._cr.fetchone()
#         return res and res[0] or 0.0

#     def get_interest_loan(self, part_id, date_from, date_to=None):
#         if date_to is None:
#             date_to = datetime.now().strftime('%Y-%m-%d')
#         self._cr.execute("SELECT sum(o.interest_amt) from loan_installment_details as o where \
#                             o.partner_id=%s \
#                             AND to_char(o.date_from, 'YYYY-MM-DD') >= %s AND to_char(o.date_from, 'YYYY-MM-DD') <= %s ",
#                             (part_id, date_from, date_to))
#         res = self._cr.fetchone()
#         return res and res[0] or 0.0

class LoanType(models.Model):
    _name = 'partner.loan.type'
    _description = 'Loan Type'
    #     _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # @api.multi
    def onchange_interest_payable(self, int_payble):
        if not int_payble:
            return {'value': {'interest_mode': '', 'int_rate': 0.0}}
        return {}

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done')],
        string='State',
        readonly=True
    )
    name = fields.Char(
        string='Name',
        required=True
    )
    code = fields.Char(
        string='Code'
    )
    int_payable = fields.Boolean(
        string='Is Interest Payable',
        default=False
    )
    interest_mode = fields.Selection(
        selection=[
            ('flat', 'Flat'),
            ('reducing', 'Reducing'),
            ('fees', 'Operation Fees')],
        string='Interest Mode',
        default='flat'
    )
    int_rate = fields.Float(
        string='Rate',
        help='Put interest between 0-100 in range',
        digits=(16, 2),
        required=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=False,
        readonly=True,
        default=lambda self: self.env.user.company_id
    )
    loan_interest_account = fields.Many2one(
        'account.account',
        string="Interest Account"
    )
    #     employee_categ_ids = fields.Many2many(
    #         'hr.employee.category',
    #         'employee_category_loan_type_rel',
    #         'loan_type_id',
    #         'category_id',
    #         'Employee Categories'
    #     )
    #     employee_ids = fields.Many2many(
    #         'hr.employee',
    #         'loan_type_employee_rel',
    #         'loan_type_id',
    #         'employee_id',
    #         "Employee's"
    #     )
    partner_categ_ids = fields.Many2many(
        'res.partner.category',
        'partner_category_loan_type_rel',
        'loan_type_id',
        'category_id',
        'Partner Categories'
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'loan_type_partner_rel',
        'loan_type_id',
        'partner_id',
        "Partner's"
    )

    #     payment_method = fields.Selection(
    #         selection=[
    #         ('salary', 'Deduction From Payroll'),
    #         ('cash', 'Direct Cash/Cheque')],
    #         string='Repayment Method',
    #         default='salary'
    #     )
    payment_method = fields.Selection(
        selection=[
            ('cash', 'Direct Cash/Cheque')],
        string='Repayment Method',
        default='cash'
    )
    #     disburse_method = fields.Selection(
    #         selection=[
    #         ('payroll', 'Through Payroll'),
    #         ('loan', 'Direct Cash/Cheque')],
    #         string='Disburse Method',
    #         default='loan'
    #     )
    disburse_method = fields.Selection(
        selection=[
            ('loan', 'Direct Cash/Cheque')],
        string='Disburse Method',
        default='loan'
    )
    loan_proof_ids = fields.Many2many(
        'partner.loan.proof',
        string='Loan Proofs',
    )


class LoanInstallmentDetail(models.Model):
    _name = 'partner.loan.installment.details'
    _description = 'Loan Installment'
    #     _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # _order = "loan_id desc"

    #    @api.multi
    #    @api.depends('loan_id', 'loan_id.loan_type')
    #    def _check_status(self):
    #        payslip_obj = self.env['hr.payslip']
    #        for install in self:
    #            if install.loan_id:
    #                if install.loan_id.loan_type.payment_method == 'salary' and install.loan_id.state == 'disburse':
    #                    payslips = payslip_obj.search([('contract_id', '=', install.loan_id.employee_id.contract_id.id),
    #                                                 ('date_to', '>=', install.date_from),
    #                                                 ('date_to', '<=', install.date_to)])
    #                    for slip in payslips:
    #                        if slip.state == 'done':
    #                            for line in slip.line_ids:
    #                                if line.salary_rule_id.loan_deduction:
    #                                    install.check_status = True
    #                                    break
    #                            if install.check_status:
    #                                self._cr.execute("update loan_installment_details set state='paid' where id = %s" % (install.id))
    #                                break

    # @api.multi
    @api.depends('loan_id', 'install_no')
    def _get_name(self):
        for install in self:
            install.name = install.loan_id and install.loan_id.name or '' + '/Install/' + str(install.install_no)

    #    test_prepayment_id = fields.Many2one(
    #        'loan.prepayment',
    #        string='Prepayment',
    #        required=False
    #    )
    name = fields.Char(
        compute='_get_name',
        string='Name',
        store=True
    )
    install_no = fields.Integer(
        string='Number',
        required=True,
        readonly=True,
        states={'unpaid': [('readonly', True)]},
        help='Installment number.'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=False,
        readonly=False,
        states={'draft': [('readonly', True)]},
    )
    loan_id = fields.Many2one(
        'partner.loan.details',
        string='Loan',
        readonly=True,
        states={'unpaid': [('readonly', True)]},
        required=False
    )
    date_from = fields.Date(
        string='Date From',
        readonly=True,
        states={'unpaid': [('readonly', True)]}
    )
    date_to = fields.Date(
        string='Date To',
        readonly=True,
        states={'unpaid': [('readonly', True)]}
    )
    payment_date = fields.Date(
        string='Payment Date',
        readonly=False,
        #    states={'unpaid': [('readonly', True)]}
    )
    principal_amt = fields.Float(
        string='Principal Amount',
        digits=(16, 2),
        readonly=True
        # states={'unpaid': [('readonly', True)]}
    )
    amount_already_paid = fields.Float(
        string='Amount Already Paid',
        digits=(16, 2),
        readonly=True,
        states={'unpaid': [('readonly', False)]}
    )
    interest_amt = fields.Float(
        string='Interest Amount',
        digits=(16, 2),
        readonly=True,
        states={'unpaid': [('readonly', True)]}
    )
    int_payable = fields.Boolean(
        related='loan_id.int_payable',
        string='Interest Payable',
        invisible=True,
        store=True,
        default=True,
    )
    loan_type = fields.Many2one(
        related='loan_id.loan_type',
        string='Interest Type',
        store=True
    )

    loan_state = fields.Selection(
        related='loan_id.state',
        string='Loan State',
        store=True
    )
    total = fields.Float(
        string='Lasts Payment',
        digits=(16, 2),
       # states={'paid': [('readonly', False)]},
        readonly=False,
        # readonly=True,
        help='Equated monthly paid installments.'
    )
    paid = fields.Float(
        string='Paid Ammount',
        digits=(16, 2),
    #    states={'paid': [('readonly', True)]},
        # readonly=True,
        help='Equated monthly paid installments.'
    )
    remains = fields.Float(
        string='Remains Ammount',
        digits=(16, 2),
        readonly=False,
      ##  compute="_compute_remains",
        store=True,
        help='Equated monthly Remains installments.'
    )
    tot_sum = fields.Float(
        string='Total Ammount',
        digits=(16, 2),
        readonly=True,
        help='Equated monthly  installments.'
    )

    tot_due = fields.Float(
        string='Total Due',
        digits=(16, 2),
        readonly=False,
        help='Equated Total Due monthly  installments.'
    )

    partner_id = fields.Many2one(
        related='loan_id.partner_id',
        store=True,
        string='Partner',
        readonly=True
    )
    move_id = fields.Many2one(
        'account.move',
        string='Interest on Loan Journal Entry',
        readonly=True
    )
    int_move_id = fields.Many2one(
        'account.move',
        string='Interest Accounting Entry',
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=True,
        states={'unpaid': [('readonly', False)]},
        default=lambda self: self.env.user.company_id
    )
    #    check_status = fields.Boolean(
    #        compute='_check_status',
    #        string='Check Status',
    #        store=True
    #    )
    state = fields.Selection(
        selection=[
            ('unpaid', 'Unpaid'),
            ('approve', 'Confirmed'),
            ('paid', 'Paid'),
            ('rescheduled1', '1st Rescheduled'),
            ('rescheduled2', '2nd Rescheduled'),],
        string='State',
  #      readonly=True,
        default='unpaid',
        track_visibility='onchange',
        store=True,
    )
    loan_partner_type = fields.Selection(
        selection=[('customer', 'Customer'),
                   ('supplier', 'Supplier'),
                   ],
        string='Loan Partner Type',
        default="customer",
    )
    loan_class = fields.Selection(
        selection=[('islamic', 'ISLAMIC'),
                   ('commercial', 'Commercial'),
                   ],
        string='Loan Classification',
        default="islamic",
        stored=True,
    )

   ## @api.depends('total')
   ## def _compute_remains(self):
     ##   """ Compute year from and to required """
      ##  for rec in self:
      ##    ##  rec.remains = rec.tot_due - rec.total
       ##   rec.remains -= rec.paid

 ##  @api.onchange('total')
   ## def check_remains(self):
       ## for rec in self:
            ##rec.remains -= rec.total

    #         return self.write({'state':'unpaid'})
    # @api.multi
    def action_reset(self):
        for rec in self:
            rec.state = 'unpaid'

    #         return self.write({'state':'unpaid'})

    # @api.multi
    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    #         return self.write({'state':'approve'})

    # @api.multi
    def book_interest(self):  # todoprobuse
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            if installment.loan_id.loan_type.payment_method == 'cash':
                if installment.loan_id:
                    if installment.loan_id.state != 'disburse':
                        raise Warning(_('Loan is not Disbursed yet !'))
                    if installment.int_move_id:
                        raise Warning(_('Book interest entry is already generated !'))
                #             period_id = period_pool.find(installment.date_from)[0]
                timenow = time.strftime('%Y-%m-%d')
                address_id = installment.loan_id.partner_id or False
                partner_id = address_id and address_id.id or False

                if not partner_id:
                    raise Warning(_('Please configure Home Address for Partner !'))

                move = {
                    'narration': installment.loan_id.name,
                    'date': installment.date_from,
                    'ref': installment.install_no,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                 'period_id': period_id,
                }
                #                 debit_account_id = installment.loan_id.journal_id2.default_debit_account_id
                #                 if not debit_account_id:
                #                     raise Warning( _('Please configure Debit/Credit accounts on the Journal %s ') % (installment.journal_id.name))
                #                 debit_account_id = debit_account_id.id
                deb_interest_line = (0, 0, {
                    'name': _('Interest of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.partner_loan_account.id,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                     'period_id': period_id,
                    'debit': installment.interest_amt,
                    'credit': 0.0
                })

                cred_interest_line = (0, 0, {
                    'name': _('Interest of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.loan_type.loan_interest_account.id,
                    'journal_id': installment.loan_id.journal_id2.id,
                    #                     'period_id': period_id,
                    'credit': installment.interest_amt,
                    'debit': 0.0
                })
                move.update({'line_ids': [deb_interest_line, cred_interest_line]})
                inst_move_id = move_pool.create(move)
                installment.write({'int_move_id': inst_move_id.id})
        #             if installment.loan_id.journal_id2.entry_posted:
        #                 inst_move_id.post()
        return True

    # @api.multi
    def book_interest1(self):  # ok
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            #            if installment.loan_id:
            #                if installment.loan_id.state == 'draft':
            #                    raise Warning(_('Loan is not confirm/Approved yet !'))
            #                if installment.int_move_id:
            #                    raise Warning(_('Book interest entry is already generated !'))
            #             period_id = period_pool.find(installment.date_from)[0]
            timenow = time.strftime('%Y-%m-%d')
            address_id = installment.loan_id.emp_id or False
            partner_id = address_id and address_id.id or False

            if not partner_id:
                raise Warning(_('Please configure Home Address for Partner !'))

            move = {
                'narration': installment.loan_id.name,
                'date': installment.date_from,
                'ref': installment.install_no,
                'journal_id': installment.loan_id.journal_id2.id,
                #                 'period_id': period_id,
            }
            #             debit_account_id = installment.loan_id.journal_id2.default_debit_account_id
            #             if not debit_account_id:
            #                 raise Warning( _('Please configure Debit/Credit accounts on the Journal %s ') % (installment.loan_id.journal_id2.name))
            #             debit_account_id = debit_account_id.id
            if not installment.loan_id.partner_loan_account:
                raise Warning(_('Please configure Partner account.'))
            deb_interest_line = (0, 0, {
                'name': _('Interest of loan %s') % (installment.loan_id.name),
                'date': installment.date_from,
                'partner_id': partner_id,
                'account_id': installment.loan_id.partner_loan_account.id,
                'analytic_account_id': installment.loan_id.account_analytic_id.id or False,
                'journal_id': installment.loan_id.journal_id2.id,
                #                     'period_id': period_id,
                'debit': installment.interest_amt,
                'credit': 0.0
            })
            cred_interest_line = (0, 0, {
                'name': _('Interest of loan %s') % (installment.loan_id.name),
                'date': installment.date_from,
                'partner_id': partner_id,
                'account_id': installment.loan_id.loan_type.loan_interest_account.id,
                'journal_id': installment.loan_id.journal_id2.id,
                #                     'period_id': period_id,
                'credit': installment.interest_amt,
                'debit': 0.0
            })
            move.update({'line_ids': [deb_interest_line, cred_interest_line]})
            inst_move_id = move_pool.create(move)
            installment.write({'int_move_id': inst_move_id.id})
        #             if installment.loan_id.journal_id2.entry_posted:#todoprobuse
        #                 inst_move_id.post()
        #             inst_move_id.post()
        return True

    # @api.multi
    def pay_installment1(self):  # ok
        ctx = dict(self._context or {})
        ctx.update(recompute=True)
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            if installment.loan_id.loan_type.payment_method == 'cash':
                #                 period_id = period_pool.find(installment.date_from)[0]
                timenow = time.strftime('%Y-%m-%d')
                address_id = installment.loan_id.emp_id or False
                partner_id = address_id and address_id.id or False

                if not partner_id:
                    raise Warning(_('Please configure Home Address for Partner !'))

                move = {
                    'narration': installment.loan_id.name,
                    'date': installment.date_from,
                    'ref': installment.install_no,
                    'journal_id': installment.loan_id.journal_id1.id,
                    #                     'period_id': period_id,
                }
                if not installment.loan_id.journal_id1.default_debit_account_id:
                    raise Warning(_('Please configure Debit/Credit accounts on the Journal %s ') % (
                        installment.loan_id.journal_id1.name))
                if not installment.loan_id.partner_loan_account:
                    raise Warning(_('Please give partner account.'))
                debit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.journal_id1.default_debit_account_id.id,
                    'journal_id': installment.loan_id.journal_id1.id,
                    #                         'period_id': period_id,
                    'debit': installment.total,
                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.partner_loan_account.id,
                    'journal_id': installment.loan_id.journal_id1.id,
                    #                         'period_id': period_id,
                    'debit': 0.0,
                    'analytic_account_id': installment.loan_id.account_analytic_id.id or False,
                    'credit': installment.total,
                })
                move.update({'line_ids': [debit_line, credit_line]})
                move_id = move_pool.create(move)
                installment.write({'state': 'paid', 'move_id': move_id.id})
                installment.loan_id.compute_installments()
                #                 if installment.loan_id.journal_id1.entry_posted:
                #                     move_id.post()#todoprobuse
                #                 move_id.post()
                #                self.pool.get('employee.loan.details').compute_installments(cr, uid, [installment.loan_id.id], context=context)
                ctx.pop('recompute')
        return True

    # @api.multi
    def pay_installment(self):  # ok #probusetodo when call from form view of opening balance
        ctx = dict(self._context or {})
        move_pool = self.env['account.move']
        #         period_pool = self.env['account.period']
        for installment in self:
            if installment.loan_id.state != 'disburse':
                raise Warning(_('Loan is not Disbursed yet !'))
            if installment.loan_id.loan_type.payment_method == 'cash':
                #                 period_id = period_pool.find(installment.date_from)[0]
                timenow = time.strftime('%Y-%m-%d')
                address_id = installment.loan_id.partner_id or False
                partner_id = address_id and address_id.id or False

                if not partner_id:
                    raise Warning(_('Please configure Home Address for partner !'))

                move = {
                    'narration': installment.loan_id.name,
                    'date': installment.date_from,
                    'ref': installment.install_no,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                     'period_id': period_id,
                }
                if not installment.loan_id.journal_id.default_debit_account_id:
                    raise Warning(
                        _('Please configure Debit/Credit accounts on the Journal %s ') % (self.journal_id.name))
                debit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.journal_id.default_debit_account_id.id,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                         'period_id': period_id,
                    'debit': installment.total,
                    'credit': 0.0,
                })
                credit_line = (0, 0, {
                    'name': _('EMI of loan %s') % (installment.loan_id.name),
                    'date': installment.date_from,
                    'partner_id': partner_id,
                    'account_id': installment.loan_id.partner_loan_account.id,
                    'journal_id': installment.loan_id.journal_id.id,
                    #                         'period_id': period_id,
                    'debit': 0.0,
                    'credit': installment.total,
                })
                move.update({'line_ids': [debit_line, credit_line]})
                move_id = move_pool.create(move)
                installment.write({'state': 'paid', 'move_id': move_id.id})
                #                 if installment.loan_id.journal_id.entry_posted:#todoprobuse
                #                     move_id.post()
                #                 move_id.post()
                installment.loan_id.compute_installments()
                if ctx.get('recompute'):
                    ctx.pop('recompute')
            else:
                installment.write({'state': 'paid'})
        return True



class LoanPloicy(models.Model):
    _name = "partner.loan.policy"
    _description = "Loan Policy Details"

    name = fields.Char(
        'Name',
        required=True
    )
    code = fields.Char(
        'Code'
    )
    #     employee_categ_ids = fields.Many2many(
    #         'hr.employee.category',
    #         'employee_category_policy_rel_loan',
    #         'policy_id',
    #         'category_id',
    #         'Employee Categories'
    #     )
    #     employee_ids = fields.Many2many(
    #         'hr.employee',
    #         'policy_employee_rel',
    #         'policy_id',
    #         'employee_id',
    #         "Employee's"
    #     )
    partner_categ_ids = fields.Many2many(
        'res.partner.category',
        'partner_category_policy_rel_loan',
        'policy_id',
        'category_id',
        'Partner Categories'
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'policy_partner_rel',
        'policy_id',
        'partner_id',
        "Partner's"
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self: self.env.user.company_id
    )
    policy_type = fields.Selection(
        selection=[
            ('maxamt', 'Max Loan Amount'),
            ('loan_gap', 'Gap between two loans'),
            #        ('eligible_duration', 'Qualifying Period'),
            #        ('', '')
        ],
        string='Policy Type',
        required=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done')],
        string='State',
        readonly=True
    )
    max_loan_type = fields.Selection(
        selection=[
            # ('basic', 'Basic Salary'),
            # ('gross', 'Gross Salary'),
            ('fixed', 'Fix Amount'),
            ('', '')],
        string='Basis',
        help='As a percentage of Basic/Gross Salary or as a fixed amount',
    )
    policy_value = fields.Float(
        string='Value',
        help='If policy type is Max Loan Amount and Basis is Fixed Amount, then set value as a fixed amount, ie maximum loan that can be taken. \n If policy type is Gap between two loans or Qualifying Period, then set value as a number of months.'
    )


# class HrEmployeeCategory(models.Model):
#     _inherit = "hr.employee.category"
#     _description = "Employee Category"

class PartnerCategory(models.Model):
    _inherit = "res.partner.category"
    _description = "Partner Category"

    loan_policy = fields.Many2many(
        'partner.loan.policy',
        'partner_category_policy_rel_loan',
        'category_id',
        'policy_id',
        string='Loan Policies'
    )
    allow_multiple_loan = fields.Boolean(
        string='Allow Multiple Loans'
    )


# class HrEmployee(models.Model):
#     _inherit = "hr.employee"
#     _description = "Employee"


    # employee_id = fields.Many2one('hr.employee.category', string="Employee", help="Employee")


# class HrSalaryRule(models.Model):
#     _inherit = 'hr.salary.rule'

#    loan_allowance = fields.Boolean(
#        string='Is Loan Allowance'
# )
# loan_deduction = fields.Boolean(
#    string='Is Loan Deduction'
# )

# class LoanPrepayment(models.Model):
#     _name = 'loan.prepayment'
#     _description = 'Loan Prepayment'
#     _inherit = ['mail.thread']
#
#     @api.multi
#     def validate(self):
#         for a in self:
#             pass
#             a.state = 'open1'
# #         return self.write({'state':'open1'})
#
#     @api.multi
#     def validate1(self):
#         for a in self:
#             pass
#             a.state = 'open'
# #         return self.write({'state':'open'})
#
#     @api.multi
#     def set_to_close(self):
#         for rec in self:
#             rec.state = 'close'
# #         return self.write({'state': 'close'})
#
#     @api.multi
#     def set_to_draft(self):
#         for rec in self:
#             rec.state = 'draft'
# #         return self.write({'state': 'draft'})
#
#     @api.model
#     def reducing_balance_method(self, p, r, n):
#         # Determine the interest rate on the loan, the length of the loan and the amount of the loan
#         res = {}
#         for i in range(0, n):
#             step_1_p = p  # principal amount at the beginning of each period
#             step_2_r_m = r / (12 * 100.00)  # interest rate per month
#             step_3_r_m = 1 + step_2_r_m  # add 1 to interest rate per month
#             step_4 = step_3_r_m ** (n - i)  # Raise the step_2_r_m to the power of the number of payments required on the loan
#             step_5 = step_4 - 1  #  minus 1 from step_4
#             step_6 = step_2_r_m / step_5  # Divide the interest rate per month(step_2_r_m) by the step_5
#             step_7 = step_6 + step_2_r_m  # Add the interest rate per month to the step_6
#             step_8_EMI = round(step_7 * step_1_p, 2)  # Total EMI to pay month
#             step_9_int_comp = round(step_1_p * step_2_r_m, 2)  # Total Interest component in EMI
#             step_10_p_comp = round(step_8_EMI - step_9_int_comp, 2)  # Total principal component in EMI
#             p -= step_10_p_comp  # new principal amount
#             res[i] = {'emi':step_8_EMI,
#                       'principal_comp':step_10_p_comp,
#                       'interest_comp':step_9_int_comp
#                       }
#         return res
#
#     @api.model
#     def flat_rate_method(self, principal, rate, duration):
#         return ((principal * rate) / 100)
#
#     @api.multi
#     def create_installments(self):
#         if not self.ids:
#             return True
#         if not self.purchase_date:
#             raise Warning(_('Please give disbursement date.'))
#         else:
#             date_disb = self.purchase_date
#         date_approved_obj = datetime.strptime(date_disb, DEFAULT_SERVER_DATE_FORMAT)
#         installment_obj = self.env['loan.installment.details']
#         ins_ids = installment_obj.search([('test_prepayment_id', '=', self.id)])
#         if ins_ids:
#             ins_ids.unlink()
#         day = date_approved_obj.day
#         month = date_approved_obj.month
#         year = date_approved_obj.year
#         interest_amt = 0.0
#         principal_amt = self.purchase_value / (self.duration or 1.0)
#         if self.int_payable:
#             total_interest_amount = 0.0
#             if self.interest_mode == 'flat':
#                 total_interest_amount = self.flat_rate_method(self.purchase_value, self.int_rate, self.duration)
#             else:
#                 values = self.reducing_balance_method(self.purchase_value, self.int_rate, self.duration)
#                 for key, value in values.iteritems():
#                     total_interest_amount += value['interest_comp']
#             interest_amt = total_interest_amount / (self.duration or 1.0)
#         total = principal_amt + interest_amt
#         if self.interest_mode == 'reducing':
#             reducing_val = self.reducing_balance_method(self.purchase_value, self.int_rate, self.duration)
#
#         old_emi = 0.0
#         old_paid = 0.0
#         for install_no in range(0, self.duration):
#             date_from = datetime(year, month, day)
#             date_to = date_from + relativedelta(months=1)
#             if self.interest_mode == 'reducing':
#                 principal_amt = reducing_val[install_no]['principal_comp']
#                 if self.int_payable:
#                     interest_amt = reducing_val[install_no]['interest_comp']
#                 total = principal_amt + interest_amt
#             day, month, year = date_to.day, date_to.month, date_to.year
#             x = old_emi + old_paid
#             installment_line = {
#                  'install_no':install_no + 1,
#                  'date_from':date_from.strftime('%Y-%m-%d'),
#                  'date_to':date_to.strftime('%Y-%m-%d'),
#                  'principal_amt':principal_amt,
#                  'interest_amt':interest_amt,
#                  'amount_already_paid': x,
#                  'total':total,
#                  'test_prepayment_id':self.id
#              }
#             installment_obj.create(installment_line)
#             old_emi = total
#             old_paid = x
#         return True
#
#     @api.multi
#     def onchange_company_id(self, company_id=False):
#         val = {}
#         if company_id:
#             company = self.env['res.company'].browse(company_id)
# #             if company.currency_id.company_id and company.currency_id.company_id.id != company_id:
# #                 val['currency_id'] = False
# #             else:
# #                 val['currency_id'] = company.currency_id.id#todoprobuse
#         val['currency_id'] = company.currency_id.id
#         return {'value': val}
#
#     @api.one
#     @api.depends('purchase_value', 'total_am')
#     def _amount_residual(self):
#         for s in self:
#             s.value_residual = s.purchase_value - s.total_am
#
#     @api.one
#     @api.depends('depreciation_line_ids')
#     def _total_am(self):
#         for s in self:
#             t = 0.0
#             for k in s.depreciation_line_ids:
#                 if k.state == 'paid':
#                     t += k.total
#             s._total_am = t
#
#     @api.one
#     @api.depends('loan_type')
#     def _get_loan_values(self):
#         for rec in self:
#             allowed_employees = []
#             for categ in rec.loan_type.employee_categ_ids:
#                 allowed_employees += map(lambda x:x.id, categ.employee_ids)
#             allowed_employees += map(lambda x:x.id, rec.loan_type.employee_ids)
#             if rec.emp_id.id in allowed_employees:
#                 rec.int_rate = rec.loan_type.int_rate
#                 rec.interest_mode = rec.loan_type.interest_mode
#                 rec.int_payable = rec.loan_type.int_payable
#
#     value_residual = fields.Float(
#         compute='_amount_residual',
#         digits=dp.get_precision('Account'),
#         string='Closing Balance'
#     )
#     total_am = fields.Float(
#         compute='_total_am',
#         digits=dp.get_precision('Account'),
#         string='Total Deducted'
#     )
#     name = fields.Char(
#         'Name',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]},
#         default='/'
#     )
#     method_prepayment = fields.Selection(
#         selection=[('add', 'Additions to existing loan'),
#         ('new', 'Transfer an existing loan')],
#         string='Method',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]},
#         help="Choose the method to use for booking loans.\n" \
#             " * Additions to existing loan: Add items to existing loan. \n"\
#             " * Transfer an existing loan: select for an already existing loan. Journals must be raised in GL to book the transfer.",
#         default='new'
#     )
#     emp_id = fields.Many2one(
#         'hr.employee',
#         string='Employee',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]}
#     )
#     loan_type = fields.Many2one(
#         'loan.type',
#         string='Loan Type',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]}
#     )
#     user_id = fields.Many2one(
#         'res.users',
#         string='Responsible User',
#         required=False,
#         readonly=True,
#         states={'draft':[('readonly', False)]},
#         default=lambda self: self.env.user
#     )
#     state = fields.Selection(
#         selection=[('draft', 'Draft'),
#         ('open1', 'Confirmed'),
#         ('approve', 'Approved'),
#         ('open', 'Running'),
#         ('close', 'Closed'),
#         ('reject', 'Rejected'),
#         ('cancel', 'Cancelled')],
#         string='State',
#         required=True,
#         readonly=True,
#         default='draft'
#     )
#     journal_id1 = fields.Many2one(
#         'account.journal',
#         string='Repayment Board Journal',
#         required=False,
#         readonly=False,
#         states={'close':[('readonly', True)]}
#     )
#     book_gl = fields.Boolean(
#         string='Book Transfer to GL?',
#         states={'draft':[('readonly', False)]},
#         readonly=True
#     )
#     gl_account_id = fields.Many2one(
#         'account.account',
#         string='GL Account',
#         readonly=True,
#         required=False,
#         states={'draft':[('readonly', False)]}
#     )
#     move_id1 = fields.Many2one(
#         'account.move',
#         string='Journal Entry 1',
#         readonly=True
#     )
#     journal_id = fields.Many2one(
#         'account.journal',
#         string='Book Transfer Journal',
#         required=False
#     )
#     code = fields.Char(
#         string='Reference',
#         readonly=True,
#         states={'draft':[('readonly', False)]}
#     )
#     purchase_value = fields.Float(
#         string='Transferred Balance ',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]}
#     )
#     currency_id = fields.Many2one(
#         'res.currency',
#         string='Currency',
#         required=True,
#         readonly=True,
#         states={'draft':[('readonly', False)]},
#         default=lambda self: self.env.user.company_id.currency_id
#     )
#     company_id = fields.Many2one(
#         'res.company',
#         string='Company',
#         required=True,
#         readonly=True, states={'draft':[('readonly', False)]},
#         default=lambda self:self.env['res.company']._company_default_get('loan.prepayment')
#     )
#     note = fields.Text(string='Note')
#     purchase_date = fields.Date(string='Transfer Date', required=True, readonly=True, help='This date will be the date when the Loan will be considered to be Starting in the system and this date will be used in the Repayment Board.', states={'draft':[('readonly', False)]}, default=time.strftime('%Y-%m-%d'))
#     active = fields.Boolean(string='Active', default=True)
#     employee_loan_account = fields.Many2one('account.account', string="Employee Account", readonly=False, states={'disburse':[('readonly', True)]})
#     duration = fields.Integer(string='Duration(Months)', required=True, readonly=True, states={'draft':[('readonly', False)]})
#     depreciation_line_ids = fields.One2many('loan.installment.details', 'test_prepayment_id', string='Repayments Lines', readonly=True, states={'draft':[('readonly', False)], 'open':[('readonly', False)]})
#     original_amount = fields.Float(string='Original Amount', digits=dp.get_precision('Account'), readonly=True, states={'draft':[('readonly', False)]})
#     account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account', states={'draft':[('readonly', False)]}, readonly=True)
#
#     int_payable = fields.Boolean(compute='_get_loan_values', string='Is Interest Payable', store=True)
#     int_rate = fields.Float(compute='_get_loan_values', string='Rate(Per Annum)', help='Interest rate between 0-100 in range', digits=(16, 2), store=True)
#     interest_mode = fields.Selection(compute='_get_loan_values', selection=[('flat', 'Flat'), ('reducing', 'Reducing'), ('', '')], string='Interest Mode', store=True)
#
#     @api.multi
#     def approve(self):
# #         period_obj = self.env['account.period']
#         move_obj = self.env['account.move']
#         move_line_obj = self.env['account.move.line']
#         currency_obj = self.env['res.currency']
#         for a in self:
#             if a.book_gl:
# #                 period_ids = period_obj.find(a.purchase_date)
#                 move_vals = {
#                     'date': a.purchase_date,
#                     'ref': a.name,
# #                     'period_id': period_ids and period_ids.id or False,
#                     'journal_id': a.journal_id.id,
#                 }
#                 move_id = move_obj.create(move_vals)
#                 journal_id = a.journal_id.id
#                 partner_id = a.emp_id.address_home_id.id
#                 company_currency = a.company_id.currency_id
#                 current_currency = a.currency_id
#                 ctx = dict(self._context or {})
#                 ctx.update({'date': time.strftime('%Y-%m-%d')})
#                 amount = current_currency.compute(a.purchase_value, company_currency)
#
#                 sign = a.journal_id.type == 'purchase' and 1 or -1
#                 if not a.employee_loan_account:
#                     raise Warning( _('Please configure loan account of employee'))
#
#                 move_line_obj.create({
#                     'name': a.name,
#                     'ref': a.name,
#                     'move_id': move_id.id,
#                     'account_id': a.gl_account_id.id,
#                     'debit': 0.0,
#                     'credit': amount,
# #                     'period_id': period_ids and period_ids.id or False,
#                     'journal_id': journal_id,
#                     'partner_id': partner_id,
#                     'currency_id': company_currency.id <> current_currency.id and current_currency.id or False,
#                     'amount_currency': company_currency.id <> current_currency.id and -sign * a.purchase_value or 0.0,
#                     'date': a.purchase_date,
#                 })
#                 move_line_obj.create({
#                     'name': a.name,
#                     'ref': a.name,
#                     'move_id': move_id.id,
#                     'account_id': a.employee_loan_account.id,
#                     'analytic_account_id': a.account_analytic_id.id or False,
#                     'credit': 0.0,
#                     'debit': amount,
# #                     'period_id': period_ids and period_ids.ids or False,
#                     'journal_id': journal_id,
#                     'partner_id': partner_id,
#                     'currency_id': company_currency.id <> current_currency.id and current_currency.id or False,
#                     'amount_currency': company_currency.id <> current_currency.id and sign * a.purchase_value or 0.0,
#                     'date': a.purchase_date,
#                 })
#                 a.write({'move_id1': move_id.id})
#                 a.state = 'approve'
# #         return self.write({'state': 'approve'})
#
#     @api.multi
#     def set_to_cancel(self):
#         for rec in self:
#             rec.state = 'cancel'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:










