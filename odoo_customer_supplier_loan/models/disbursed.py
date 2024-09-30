import dateutil
import odoo.addons.decimal_precision as dp

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import Warning
from odoo.exceptions import UserError, ValidationError





class LoanDisbursmentDetail(models.Model):
    _name = 'partner.loan.disbursmens'
    _description = 'Loan Disbursments'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'disbursment_no desc'

    import dateutil
    import odoo.addons.decimal_precision as dp

    import time
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Confirm'),
        ('validate', 'Validate'),
        ('approve', 'Approve'),
        ('paid', 'Disbursed'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    name = fields.Char(
        compute='_get_partnername',
        string='Name',
        store=True
    )
    disbursment_no = fields.Char(
        string='Payment Number',
        required=False,
        readonly=True,
        #  states={'unpaid': [('readonly', True)]},
        help='Payment number.'
    )
    currency_id = fields.Char(
        string='Currency',
        required=False,
        readonly=True,
        #        compute='_get_partnername',
    )

    loan_id = fields.Many2one(
        'partner.loan.details',
        string='Loan Number',
        readonly=False,
        # states={'unpaid': [('readonly', True)]},
        required=True
    )
    disbursment_date = fields.Date(
        string='Disbursment Date',
        readonly=False,
        #     states={'unpaid': [('readonly', False)]}
    )
    loan_amt = fields.Float(
        string='Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_partnername',
        store = True
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    pay_amt = fields.Float(
        string='Disbursment Amount',
        digits=(16, 2),
        required=False,
        readonly=False,
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )
    remain_amt = fields.Float(
        string='Remains Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        # states={'unpaid': [('readonly', True)]}
        #  states = {'approve': [('readonly', True)], 'refuse': [('readonly', True)], 'cancel': [('readonly', True)]},
    )
    payment_method = fields.Selection(
        selection=[('cash', 'Direct Cash/Cheque')],
        string='Repayment Method',
        default='cash'
    )
    installment_lines = fields.One2many(
        'partner.loan.installment.details',
        'loan_id',
        'Installments',
        copy=False
    )
    current_disbursment = fields.Selection(
        selection=[('1', 'First Payment'),
                   ('2', 'Second Payment'),
                   ('3', 'Third Payment'),
                   ],
      # default='1',
        compute = '_get_partnername',
        string='Current Disbursment',
        stored=True,
        readonly=True
        # stored=True,
    )
    total_disbursments = fields.Selection(
        selection=[('1', 'One Payment'),
                   ('2', 'Two Payments'),
                   ('3', 'Three Payment'),
                   ],
        compute = '_get_partnername',
    #    default='1',
        string='Total Disbursment',
        # default="1",
        stored=True,
        readonly = True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=False,
        readonly=True,
        default=lambda self: self.env.user.company_id
    )

    @api.depends('loan_id')
    def _get_partnername(self):
        loan_ids = self.env['partner.loan.details'].search([("id", "=", self.loan_id.id)])
        for install in self:
            install.name = install.loan_id.partner_id.name

        for id in loan_ids:
            self.update({'currency_id': loan_ids.currency_id.symbol, 'loan_amt': loan_ids.principal_amount
                            })

            if id.no_paym == '1':
               self.total_disbursments = '1'
            elif id.no_paym == '2':
                self.total_disbursments = '2'
            elif id.no_paym == '3':
                self.total_disbursments = '3'

            if id.disburse_times == 0:
               self.current_disbursment = '1'
            elif id.disburse_times == 1:
                self.current_disbursment = '2'
            elif id.disburse_times == 2:
                self.current_disbursment = '3'
            else:
                self.current_disbursment = '3'

           # if id.state == 'approved' or id.state == '1disburse' or id.state == '2disburse' or id.state == 'disburse':
            if id.state == 'approved':
               self.remain_amt = id.total_amount_due
            else:
                self.remain_amt = id.disburse_remains



            #elif id.state == 'disburse':
           # elif id.state =='1disburse':
            #elif id.state == '1disburse':






    def button_confirm(self):

        self.write({'state': 'waiting_approval_1'})



                  #  print(self.remain_amt)
               # raise Warning(
                    # _('The loan request current status must be in Disburse State. '))

    def button_validate(self):
        self.write({'state': 'validate'})

    def button_refuse(self):
        self.write({'state': 'refuse'})

    def button_cancel(self):
        self.write({'state': 'cancel'})
    def button_resset(self):
        self.write({'state': 'waiting_approval_1'})

    def print_receipt(self):
        return self.env.ref('odoo_customer_supplier_loan.print_disbursment_pdf').report_action(self)

    def button_pay(self):
        self.disbursment_no = self.env['ir.sequence'].next_by_code('paym.loan.disburse.seq')
        loan_ids = self.env['partner.loan.details'].search([("id", "=", self.loan_id.id)])

        for id in loan_ids:
                if id.state == 'approved' or id.state == '1disburse' or id.state == '2disburse':
                   if id.principal_amount > 0 and id.disburse_remains == 0 and id.disburse_times == 0 and self.pay_amt < id.principal_amount:
                          if id.grace_period == '0':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=0)
                          elif id.grace_period == '1':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=1)
                          elif id.grace_period == '2':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=2)
                          elif id.grace_period == '3':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=3)
                          elif id.grace_period == '4':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=4)
                          elif id.grace_period == '5':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=5)
                          elif id.grace_period == '6':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=6)

                          id.write({'date_disb_grace': new_grace_date, 'date_disb': self.disbursment_date, 'first_dis_date': self.disbursment_date, 'state': '1disburse'})
                          self.write({'state': 'paid'})
                          self.remain_amt = id.total_amount_due - self.pay_amt
                         # self.remain_amt = id.principal_amount - self.pay_amt
                      #    self.remain_amt = id.total_amount_due
                          id.disburse_remains = self.remain_amt
                          if id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                              raise Warning(
                                  _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))
                          else:
                              id.disburse_times += 1
                          id.installment_lines.unlink()
                          id.create_installments(id)

                   elif id.principal_amount > 0 and id.disburse_times == 0 and self.pay_amt >= id.principal_amount:
                          if id.grace_period == '0':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=0)
                          elif id.grace_period == '1':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=1)
                          elif id.grace_period == '2':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=2)
                          elif id.grace_period == '3':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=3)
                          elif id.grace_period == '4':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=4)
                          elif id.grace_period == '5':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=5)
                          elif id.grace_period == '6':
                            new_grace_date = self.disbursment_date + dateutil.relativedelta.relativedelta(months=6)

                          id.write({'date_disb_grace': new_grace_date, 'date_disb': self.disbursment_date, 'first_dis_date': self.disbursment_date, 'state': 'disburse'})
                          self.write({'state': 'paid'})
                          self.remain_amt = id.total_amount_due - self.pay_amt
                         # self.remain_amt = id.principal_amount - self.pay_amt
                      #    self.remain_amt = id.total_amount_due
                          id.disburse_remains = self.remain_amt
                          if id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                              raise Warning(
                                  _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))
                          else:
                              id.disburse_times += 1
                          id.installment_lines.unlink()
                          id.create_installments(id)


                   elif id.principal_amount > 0 and id.disburse_remains != 0 and id.disburse_times == 1 and self.pay_amt < id.disburse_remains:
                      id.write({'second_dis_date': self.disbursment_date, 'state': '2disburse'})
                      self.write({'state': 'paid'})
                      self.remain_amt = id.disburse_remains - self.pay_amt
                      id.disburse_remains = self.remain_amt
                      if id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                         raise Warning(
                          _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))
                      else:
                         id.disburse_times += 1
                   elif id.principal_amount > 0 and id.disburse_remains != 0 and id.disburse_times == 1 and id.principal_amount >= id.disburse_remains:
                      id.write({'second_dis_date': self.disbursment_date, 'state': 'disburse'})
                      self.write({'state': 'paid'})
                      self.remain_amt = id.disburse_remains - self.pay_amt
                      id.disburse_remains = self.remain_amt
                      if id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                         raise Warning(
                          _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))
                      else:
                         id.disburse_times += 1

                   elif id.principal_amount > 0 and id.disburse_remains != 0 and id.disburse_times == 2:
                      id.write({'third_dis_date': self.disbursment_date, 'state': 'disburse'})
                      self.write({'state': 'paid'})
                      self.remain_amt = id.disburse_remains - self.pay_amt
                      id.disburse_remains = self.remain_amt
                      if id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                         raise Warning(
                          _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))
                      else:
                         id.disburse_times += 1


                   elif id.disburse_times > 0 and id.disburse_remains == 0:
                        raise Warning(
                            _('This loan was fully disbursed.'))

                   elif id.principal_amount > 0 and id.disburse_remains != 0 and self.pay_amt > id.disburse_remains:
                        raise Warning(
                          _('The amount of the disbursement exceeds the amount of the remaining disbursement.'))

                   else:
                       raise Warning(


                        _('The amount of the disbursement exceeds the amount of the loan'))

                else:
                    raise Warning(_('The Loan status is not in approve state'))


    def unlink(self):
        for payment in self.filtered(
                lambda payment: payment.state != 'draft'):
            raise UserError(
                _('You cannot delete disbursment request which is not in draft state.'))
        return super(LoanDisbursmentDetail, self).unlink()