# -*- coding:utf-8 -*-

from odoo import api, fields, models


class AttendanceResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    week_end = fields.Boolean(string="Weekend")
