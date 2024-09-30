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



class LoanPaymentDetail(models.Model):
    _name = 'partner.loan.payments'
    _description = 'Loan Payments'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'payment_no desc'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('approve', 'Approved'),
        ('paid', 'Paid'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    name = fields.Char(
        compute='_get_partnername',
        string='Name',
        store=True
    )
    payment_no = fields.Char(
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

    pay_id = fields.Many2one(
        'partner.loan.details',
        string='Loan Number',
        readonly=False,
        # states={'unpaid': [('readonly', True)]},
        required=True
    )
    payment_date = fields.Date(
        string='Payment Date',
        readonly=False,
        #     states={'unpaid': [('readonly', False)]}
    )

    pay_amt = fields.Float(
        string='Payment Amount',
        digits=(16, 2),
        required=False,
        readonly=False,
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
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=False,
        readonly=True,
        default=lambda self: self.env.user.company_id
    )

    @api.depends('pay_id')
    def _get_partnername(self):
        for install in self:
            install.name = install.pay_id.partner_id.name
            curr_t = self.env['partner.loan.details'].search([('id', '=', self.pay_id.id)])

            print(curr_t.currency_id.symbol)
            install.update({'currency_id': curr_t.currency_id.symbol,
                            })

    def button_confirm(self):
        self.write({'state': 'waiting_approval_1'})

    def button_validate(self):
        seq_no = self.env['ir.sequence'].next_by_code('paym.loan.seq')
        self.write({'state': 'approve', 'payment_no': seq_no})

    def button_refuse(self):
        self.write({'state': 'refuse'})

    def button_cancel(self):
        self.write({'state': 'cancel'})

    def print_receipt(self):
        return self.env.ref('odoo_customer_supplier_loan.print_recipient_pdf').report_action(self)

    def button_pay(self):
        # for loan in self:
        #    loaners = self.env['partner.loan.details'].search([("date_disb", "!=", False), ("state", "=", 'disburse')])

        # loan_ids = self.env['partner.loan.installment.details'].search([("state", "=", 'unpaid')])
        #      print(loan_ids)
        #    print(self.pay_id.id)
        # for id in loan_ids:
        #         print(self.pay_amt)

        loan_ids = self.env['partner.loan.details'].search([("id", "=", self.pay_id.id)])
        for loan_id in loan_ids:
            loan_id.total_amount_paid += self.pay_amt
            loan_id.total_amount_due -= self.pay_amt

        #       print (loan_id.id)

        ids = self.env['partner.loan.installment.details'].search(
            [("loan_id", "=", self.pay_id.id), ("state", "=", 'unpaid')])
        #    print (ids.loan_id)
        # for i in pay_id:
        # print (i.loan_id.id)

        #    loan_id.filtered(lambda line: line.id == 36)
        # print (pay_id.id)
        access_payment = self.pay_amt

        a2 = 0

        new_paym = 0

        #  total_remains = 0
        #     payment = self.pay_amt
        for id in ids:
            #  total_remains = id.remains
            payment = self.pay_amt
            if loan_id.state == 'disburse' or loan_id.state == '1disburse' or loan_id.state == '2disburse':
                if id.principal_amt > 0:

                    if access_payment > 0 and access_payment > id.tot_due and access_payment > id.remains and new_paym == 0 and id.install_no != loan_id.dgrace:

                        id.write({'state': 'paid'})
                        id.total = id.tot_due
                        access_payment -= round((id.remains), 2)
                        id.paid = id.tot_due
                        id.remains = id.tot_due - id.paid
                        if access_payment > id.tot_due:
                            new_paym = 0
                        else:
                            new_paym = 1

                        print(new_paym)

                    elif access_payment > 0 and access_payment > id.tot_due and access_payment > id.remains and new_paym == 0 and id.install_no == loan_id.dgrace:

                        id.write({'state': 'paid'})
                        id.total = id.tot_due
                        access_payment -= round((id.remains), 2)
                        id.paid = id.total + access_payment
                        id.remains = id.tot_due - id.paid
                        loan_id.state = 'closed'
                        if access_payment > id.tot_due:
                            new_paym = 0
                        else:
                            new_paym = 1

                        print(new_paym)
                    elif access_payment > 0 and access_payment < id.tot_due and access_payment > id.remains and new_paym == 1 and id.install_no != loan_id.dgrace:

                        id.write({'state': 'paid'})
                        id.total = access_payment
                        access_payment -= round((id.remains), 2)
                        id.paid = id.total + id.paid
                        id.remains = id.tot_due - id.paid
                        print(new_paym)

                    elif access_payment > 0 and access_payment < id.tot_due and access_payment > id.remains and new_paym == 1 and id.install_no == loan_id.dgrace:

                        id.write({'state': 'paid'})
                        id.total = access_payment
                        access_payment -= round((id.remains), 2)
                        id.paid = id.total
                        id.remains = id.tot_due - id.paid
                        print(new_paym)

                    elif access_payment > 0 and access_payment < id.tot_due and access_payment < id.remains and new_paym == 1 and id.install_no != loan_id.dgrace:

                        #      a2 -=  round(payment - (id.total + id.interest_amt), 2)

                        id.write({'total': access_payment, 'paid': id.total + id.paid, 'remains': id.tot_due - id.paid})

                        #       id.remains = id.tot_due - id.paid
                        id.remains = id.tot_due - id.total
                        id.paid = id.total
                        new_paym = 2
                        print(new_paym)

                    elif access_payment > 0 and access_payment < id.tot_due and access_payment < id.remains and new_paym == 1 and id.install_no == loan_id.dgrace:

                        #      a2 -=  round(payment - (id.total + id.interest_amt), 2)

                        id.write(
                            {'total': access_payment, 'paid': id.total + id.paid, 'remains': id.tot_due - id.paid})

                        #       id.remains = id.tot_due - id.paid

                        id.paid = id.total + access_payment
                        id.remains = id.tot_due - id.paid
                        new_paym = 2
                        print(new_paym)





                    elif access_payment > 0 and access_payment < id.tot_due and access_payment > id.remains and new_paym == 0:

                        #      a2 -=  round(payment - (id.total + id.interest_amt), 2)

                        ##   id.write({'state':'paid'})
                        ##  id.total = access_payment
                        ## access_payment -= round((id.remains), 2)
                        ##  id.paid = id.total + id.paid
                        ##   id.remains = id.tot_due - id.paid
                        id.write({'state': 'paid'})
                        id.total = access_payment
                        access_payment -= round((id.remains), 2)
                        id.paid = id.tot_due
                        id.remains = id.tot_due - id.paid

                        new_paym = 0
                        print(new_paym)
                    elif access_payment > 0 and access_payment < id.tot_due and access_payment < id.remains and new_paym == 0:
                        id.write({'state': 'unpaid'})

                        #   id.paid = id.tot_due + id.paid
                        # id.remains = id.tot_due - id.paid

                        ##   print(new_paym)
                        ## print('test')
                        ##   print(id.remains)
                        ##   access_payment -= round((id.remains), 2)
                        ##  id.paid = access_payment + id.paid
                        ##  id.remains = id.tot_due - id.total
                        id.total = access_payment
                        access_payment -= round((id.remains), 2)
                        #    id.remains = id.tot_due - id.total
                        id.paid = id.total + id.paid
                        id.remains = id.tot_due - id.paid

                    elif access_payment == id.remains:
                        print(new_paym)
                        id.write({'state': 'paid'})
                        id.paid = id.total + id.paid
                        id.remains = id.tot_due - id.paid
                        access_payment = 0

                    #   id.remains = id.tot_due - id.paid

                    #     id.remains = id.tot_due - id.paid
                    #   id.remains = id.tot_due - id.paid

                    #         id.paid = 0 - id.remains

                    self.write({'state': 'paid'})
            else:
                raise Warning(
                    _('The loan request current status must be in Disburse State.'))

    def unlink(self):
        for payment in self.filtered(
                lambda payment: payment.state != 'draft'):
            raise UserError(
                _('You cannot delete payment request which is not in draft state.'))
        return super(LoanPaymentDetail, self).unlink()