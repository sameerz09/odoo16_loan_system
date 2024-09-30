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


class LoanPaymentReschedule(models.Model):
    _name = 'partner.loan.payments.reschedule'
    _description = 'Loan Payments Reschedule'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'resch_no desc'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('approve', 'Approved'),
        ('reschedule', 'Rescheduled'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    name = fields.Char(
        compute='_get_partnernames',
        string='Name',
        store=True
    )
    resch_no = fields.Char(
        string='Reschedule Number',
        required=False,
        readonly=True,
        help='Payment number.'
    )
    currency_id = fields.Char(
        string='Currency',
        required=False,
        readonly=True,
        store=True,
        compute='_get_customer_name',
    )

    loan_id = fields.Many2one(
        'partner.loan.details',
        string='Loan Number',
        readonly=False,
        required=True
    )
    reschedule_date = fields.Date(
        string='Reschedule Date',
        readonly=False,
        required=True,
        default=fields.Datetime.now
    )

    pay_amt = fields.Float(
        string='Payment Principal Amount',
        digits=(16, 2),
        required=True,
        readonly=True,  # Set the field as readonly
        compute='_compute_pay_amt',  # Use a compute method to dynamically set the value
        store=True,  # Optionally store the computed value in the database
    )


    pay_int_amt = fields.Float(
        string='Payment Interest Amount',
        digits=(16, 2),
        required=True,
        readonly=True,
        default=0.0  # Set default value as 0.0 and make the field read-only
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
    customer = fields.Char(
        string='Customer Name',
        required=False,
        readonly=True,
        compute='_get_customer_name',
        store=True

    )
    guarantor = fields.Char(
        string='Guarantor Name',
        required=False,
        readonly=True,
        compute='_get_customer_name',
        store=True
    )
    age = fields.Char(
        string='Customer Age',
        required=False,
        readonly=True,
        compute='_get_customer_name',
        store=True

    )

    tot_loan_amt = fields.Float(
        string='Total Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )

    bal_loan_amt = fields.Float(
        string='Balance Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    tot_org_amt = fields.Float(
        string='Total Orginal Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    tot_rest_org_amt = fields.Float(
        string='Total Rest Orginal Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_balance_intrest',
        default=0,
        store=True
    )
    tot_due_org_amt = fields.Float(
        string='Total Due Orginal Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    totint_loan_amt = fields.Float(
        string='Total Interest Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    rest_int_loan_amt = fields.Float(
        string='Rest Interest Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_balance_intrest',
        default=0,
        store=True
    )
    due_int_loan_amt = fields.Float(
        string='Due Interest Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    totcomm_loan_amt = fields.Float(
        string='Total Commission Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    rest_comm_loan_amt = fields.Float(
        string='Rest Interest Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    due_comm_loan_amt = fields.Float(
        string='Due Comm Loan Amount',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    aging1 = fields.Float(
        string='31 to 90 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        compute='_get_line_ids',
        store=True,
        default=0,
    )
    aging2 = fields.Float(
        string='91 to 180 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    aging3 = fields.Float(
        string='181 to 270 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    aging4 = fields.Float(
        string='271 to 360 Aging Days',
        digits=(16, 2),
        required=False,
        readonly=True,
        default=0,
    )
    class_comp = fields.Selection(
        selection=[('1', 'Regular'),
                   ('2', 'Under Suerveillance'),
                   ('3', 'Below The Level'),
                   ('4', 'Doubtful Debts'),
                   ('5', 'Losses'),
                   ],
        string='Commitment Type',
        readonly=True,
        required=True,
        default='1'

    )
    reschedule_start_date = fields.Date(
        string='Reschedule Start Date',
        readonly=False,
        required=True,
        default=fields.Datetime.now,
    )
    install_no = fields.Integer(
        string='Number of Installments',
        required=True,
        readonly=False,
        default=1,
        states={'approve': [('readonly', True)]},
        help='Installment number.'
    )

    @api.depends('loan_id')  # Ensure the field updates when the loan_id field changes
    def _compute_pay_amt(self):
        for record in self:
            if record.loan_id:
                # Assuming there's a field in 'partner.loan.details' that holds the current balance
                record.pay_amt = record.loan_id.total_amount_due
            else:
                record.pay_amt = 0.0

    @api.depends('loan_id')
    def _get_customer_name(self):
        now = datetime.now()
        t1 = now.date()
        laswk = t1 + dateutil.relativedelta.relativedelta(days=-7)
        t3 = (t1 - laswk).days
        loans = self.env['partner.loan.details'].search([('id', '=', self.loan_id.id)], limit=1)
        for loan in loans:
            self.update({
                'currency_id': loan.currency_id.symbol, 'customer': loan.partner_id.name, 'age': loan.partner_id.age,
                'guarantor': loan.guarantor_id.name
            })

    @api.model
    def _get_line_ids(self):
        """Update the classification based on the age of unpaid installments."""
        current_date = fields.Date.context_today(self)

        unpaid_installments = self.env['partner.loan.installment.details'].search([("state", "=", 'unpaid')])
        loan_ids_to_update = {}

        for installment in unpaid_installments:
            days_past_due = (current_date - installment.date_from).days
            class_comp = None

            if 30 <= days_past_due <= 90:
                class_comp = '1'
            elif 91 <= days_past_due <= 180:
                class_comp = '2'
            elif 181 <= days_past_due <= 270:
                class_comp = '3'
            elif 271 <= days_past_due <= 360:
                class_comp = '4'

            if class_comp:
                loan_ids_to_update[installment.loan_id.id] = class_comp

    @api.depends('loan_id')
    def _get_balance_interest(self):
        """Compute the remaining interest and balance amounts based on the loan's status and unpaid installments."""
        unpaid_installments = self.env['partner.loan.installment.details'].search(
            [("loan_id", "=", self.loan_id.id), ("state", "=", 'unpaid')])
        unpaid_count = len(unpaid_installments)

        loan = self.env['partner.loan.details'].browse(self.loan_id.id)

        if not loan:
            return

        print(f'Loan Program: {loan.loan_prog}, Unpaid Count: {unpaid_count}')

        if loan.loan_prog == 'trial' and unpaid_count > 0:
            total_unpaid_interest = sum(inst.interest_amt for inst in unpaid_installments)
            self.rest_int_loan_amt = total_unpaid_interest
            self.bal_loan_amt = loan.total_amount_due
            self.tot_rest_org_amt = loan.total_amount_due - total_unpaid_interest

        elif loan.loan_prog in ['cluster', 'seasonal'] and unpaid_count > 0:
            self.tot_rest_org_amt = loan.total_amount_due
            self.bal_loan_amt = self.tot_rest_org_amt
            self.rest_comm_loan_amt = 0  # No outstanding commission for these programs

        else:
            self.rest_int_loan_amt = 0
            self.tot_rest_org_amt = 0
            self.bal_loan_amt = 0
            self.rest_comm_loan_amt = 0

    def unlink(self):
        """Prevent deletion of reschedule requests that are not in 'draft' state."""
        if any(resch.state != 'draft' for resch in self):
            raise UserError(_('You cannot delete reschedule request which is not in draft state.'))
        return super(LoanPaymentReschedule, self).unlink()

    def button_confirm(self):
        """Set the state of the reschedule request to 'waiting_approval_1' indicating submission for approval."""
        self.write({'state': 'waiting_approval_1'})

    def button_validate(self):
        """Approve the reschedule request and generate a unique sequence number for it."""
        sequence_number = self.env['ir.sequence'].next_by_code('paym.loan.resch.seq')
        self.write({'state': 'approve', 'resch_no': sequence_number})

    def button_refuse(self):
        """Refuse the reschedule request, setting its state to 'refuse'."""
        self.write({'state': 'refuse'})

    def button_cancel(self):
        """Cancel the reschedule request, setting its state to 'cancel'."""
        self.write({'state': 'cancel'})

    def print_receipt(self):
        """Print a receipt for the reschedule request."""
        return self.env.ref('odoo_customer_supplier_loan.print_recipient_pdf').report_action(self)


    def button_pay(self):
        loan_details = self.env['partner.loan.details'].search([('id', '=', self.loan_id.id)], limit=1)

        unpaid_installments = self.env['partner.loan.installment.details'].search(
            [("loan_id", "=", self.loan_id.id), ("state", "=", 'unpaid')])

        if loan_details.resch_times == 0:
            unpaid_installments.update({'state': 'rescheduled1'})
        elif loan_details.resch_times == 1:
            unpaid_installments.update({'state': 'rescheduled2'})

        last_installment = self.env['partner.loan.installment.details'].search(
            [("loan_id", "=", self.loan_id.id), '|', ("state", "=", 'paid'), ("state", "=", 'rescheduled1')],
            limit=1, order='id desc')
        new_installment_number = last_installment.install_no + 1

        installment_obj = self.env['partner.loan.installment.details']
        loan_obj = self.env['partner.loan.details'].search([("id", "=", self.loan_id.id)])

        for installment_number in range(0, self.install_no):
            start_date = self.reschedule_start_date + relativedelta(months=installment_number)
            end_date = start_date + relativedelta(months=1)

            principal_amount = self.pay_amt / self.install_no
            interest_amount = self.pay_int_amt / self.install_no
            total_amount = principal_amount + interest_amount

            for loan in loan_obj:
                if loan.state in ['disburse', '1disburse', '2disburse']:
                    if loan_details.resch_times < 2:
                        loan.update({'resch_times': loan_details.resch_times})

                        installment_line = {'install_no': new_installment_number,
                                            'date_from': start_date,
                                            'date_to': end_date,
                                            'principal_amt': principal_amount,
                                            'interest_amt': interest_amount,
                                            'tot_sum': total_amount,
                                            'total': 0,
                                            'tot_due': total_amount,
                                            'remains': total_amount,
                                            'loan_id': last_installment.loan_id.id
                                            }
                        installment_obj.create(installment_line)
                        new_installment_number += 1

                        self.write({'state': 'reschedule'})
                    else:
                        raise Warning(
                            _('The loan has exceeded the maximum number of reschedules allowed.'))
                else:
                    raise Warning(
                        _('The loan request status must be "Disburse" to proceed with rescheduling.'))

        loan_details.resch_times += 1

        return True

    def button_remove_installments_and_decrement(self):
        self.ensure_one()
        if not self.reschedule_start_date or not self.install_no:
            raise UserError(_("Reschedule start date or installment number is not set."))

        Installment = self.env['partner.loan.installment.details']

        # Delete all installments with state 'unpaid'
        unpaid_installments = Installment.search([
            ('loan_id', '=', self.loan_id.id),
            ('state', '=', 'unpaid')
        ])
        unpaid_installments.unlink()

        # Search for all installments with state 'rescheduled2'
        rescheduled2_installments = Installment.search([
            ('loan_id', '=', self.loan_id.id),
            ('state', '=', 'rescheduled2')
        ])

        if rescheduled2_installments:
            # Change the state of these installments to 'unpaid'
            rescheduled2_installments.write({'state': 'unpaid'})
        else:
            # If no 'rescheduled2' installments, search for 'rescheduled1'
            rescheduled1_installments = Installment.search([
                ('loan_id', '=', self.loan_id.id),
                ('state', '=', 'rescheduled1')
            ])
            if rescheduled1_installments:
                # Change the state of these installments to 'unpaid'
                rescheduled1_installments.write({'state': 'unpaid'})

        # Decrement the resch_times in the associated loan if it's not already zero
        if self.loan_id and self.loan_id.resch_times > 0:
            self.loan_id.resch_times -= 1
        else:
            raise UserError(_("No previous reschedules recorded or reschedule count is already at zero."))

        self.state = 'draft'

        return True
