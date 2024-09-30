
from odoo import fields, models


class AttendanceResCompany(models.Model):

    _inherit = "res.company"

    last_attendants_schedule_work_date = fields.Date(string="Last Attendants Schedule Work Date", readonly=True)
    last_attendants_schedule_work_total = fields.Integer(string="Last Attendants Schedule Work Total", readonly=True)