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


class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Partner"

    loan_policy = fields.Many2many(
        'partner.loan.policy',
        'policy_partner_rel',
        'partner_id',
        'policy_id',
        string='Loan Policies'
    )
    allow_multiple_loan = fields.Boolean(
        string='Allow Multiple Loans'
    )

    loan_defaulter = fields.Boolean(
        string='Loan Defaulter'
    )
    loan_ids = fields.One2many(
        'partner.loan.details',
        'partner_id',
        string='Loans Details',
        readonly=True,
        ondelete="cascade"
    )
    fam_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family', help='Family Information')

    card_id = fields.Char(string='Card ID',
                          required=True,
                          readonly=False)

    job_id = fields.Many2one(
        'hr.employee.category',
        string='Job',
        required=False,
        readonly=False,
        # default=lambda self: self.env.user.company_id
    )
    birthday = fields.Date('Date Of Birth')
    age = fields.Char(string="Calculated Age", compute="_compute_age", store=True)

    # @api.depends('dob')
    # def age_calc(self):
    #     if self.dob is not False:
    #       self.calc_age = (datetime.today().date() - datetime.strptime(str(self.dob),'%Y-%m-%d').date()) // timedelta(days=365)

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday and record.birthday <= fields.Date.today():
                record.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.birthday)).years
            else:
                record.age = 0


