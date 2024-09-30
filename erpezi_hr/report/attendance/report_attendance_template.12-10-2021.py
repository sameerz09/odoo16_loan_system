from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, time, timedelta

class ReportAttendance(models.AbstractModel):
    _name = 'report.erpezi_hr.report_attendance_template'
    _description = 'Attendance PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        list_values=[]
        weekend_days=[]
        employees = self.env['hr.employee'].search([("company_id", "=", data['form'].get('company_id')[0]),
                                                    ("active", "=", True),
                                                   ])

        attendences = self.env['hr.attendance'].search([("employee_id.company_id", "=", data['form'].get('company_id')[0]),
                                                        ("employee_id.active", "=", True),
                                                        ("check_in", ">=", data['form'].get('date_from')),
                                                        ("check_out", "<=", data['form'].get('date_to')),
                                                       ])

        holidays = self.env['hr.leave'].search([("employee_id.company_id", "=", data['form'].get('company_id')[0]),
                                                        ("employee_id.active", "=", True),
                                                        ("state", "=", 'validate'),
                                                        ("date_from", ">=", data['form'].get('date_from')),
                                                        ("date_to", "<=", data['form'].get('date_to')),
                                                       ])

        overtimes = self.env['hr.overtime'].search([
                                                    ("employee_id.company_id", "=", data['form'].get('company_id')[0]),
                                                    ("employee_id.active", "=", True),
                                                    ("state", "=", 'approved'),
                                                    ("date_from", ">=", data['form'].get('date_from')),
                                                    ("date_to", "<=", data['form'].get('date_to')),
                                                ])



        for employee in employees:
            employee_required_hours = 7
            employee_holidays_paid_hours = 0
            employee_holidays_unpaid_hours = 0
            employee_holidays_formal_hours = 0
            employee_holidays_personal_hours = 0
            employee_early_out_hours = 0
            employee_late_leave_hours = 0
            employee_attendences_hours = 0
            employee_weekend_number= 0
            employee_overtime_hours = 0

            employee_attendences = attendences.filtered(lambda line: line.employee_id.id == employee.id)
            employee_overtime = overtimes.filtered(lambda line: line.employee_id.id == employee.id)

            if employee_attendences:
                attendences_hours = employee_attendences.mapped('worked_hours')
                employee_attendences_hours = sum(attendences_hours)

            if employee_overtime:
                overtime_hours = employee_overtime.mapped('days_no_tmp')
                employee_overtime_hours = sum(overtime_hours)

           # if employee.resource_calendar_id:
            #    employee_resource_calendar_attendances = resource_calendar_attendances.filtered(lambda line: line.calendar_id.id == employee.resource_calendar_id.id)
            #if employee_resource_calendar_attendances:
            #    for attendanc in employee_resource_calendar_attendances:
            #        if attendanc.week_end != False and attendanc.week_end != None:
              #         weekend_days.append(int(attendanc.dayofweek))



         #   dateB = datetime.strptime(data['form'].get('date_to'),'%Y-%m-%d')
        #    dateA = datetime.strptime(data['form'].get('date_from'),'%Y-%m-%d')
          #  delta = timedelta(1)
         #   while dateB != dateA:
          #      dateB -= delta
           #     if dateB.isoweekday() in weekend_days:
          #          employee_weekend_number += 1

         #   employee_required_hours = employee.resource_calendar_id.hours_per_day * ((datetime.strptime(data['form'].get('date_to'),'%Y-%m-%d') - datetime.strptime(data['form'].get('date_from'),'%Y-%m-%d')).days + 1)
         #   employee_weekend_number_hours = employee.resource_calendar_id.hours_per_day * employee_weekend_number;

            employee_weekend_number_hours = 1
            employee_holidays = holidays.filtered(lambda line: line.employee_id.id == employee.id)

            holiday_statues_paid = ['AV', 'SV', 'SL', 'EL']
            holiday_statues_unpaid = ['UL', 'A', 'UV']
            holiday_leaves_formal = ['BL', 'BT']
            holiday_leaves_personal = ['PL']
            holiday_early_out = ['EO']
            holiday_late_leave = ['LL']

            employee_holidays_paid = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_statues_paid)
            if employee_holidays_paid:
               for holiday_paid in employee_holidays_paid:
                    employee_holidays_paid_hours += holiday_paid.number_of_days * employee.resource_calendar_id.hours_per_day

            employee_holidays_unpaid = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_statues_unpaid)
            if employee_holidays_unpaid:
                for holiday_unpaid in employee_holidays_unpaid:
                    employee_holidays_unpaid_hours += holiday_unpaid.number_of_days * employee.resource_calendar_id.hours_per_day

            employee_holidays_formal = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_leaves_formal)
            if employee_holidays_formal:
                for holiday_formal in employee_holidays_formal:
                    employee_holidays_formal_hours += holiday_formal.number_of_days * employee.resource_calendar_id.hours_per_day

            employee_holidays_personal = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_leaves_personal)
            if employee_holidays_personal:
                for holiday_personal in employee_holidays_personal:
                    employee_holidays_personal_hours += holiday_personal.number_of_days * employee.resource_calendar_id.hours_per_day

            employee_early_out = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_early_out)
            if employee_early_out:
                for holiday_early_out in employee_early_out:
                    employee_early_out_hours += holiday_early_out.number_of_days * employee.resource_calendar_id.hours_per_day

            employee_late_leave = employee_holidays.filtered(lambda line: line.holiday_status_id.code in holiday_late_leave)
            if employee_late_leave:
                for holiday_late_leave in employee_late_leave:
                    employee_late_leave_hours += holiday_late_leave.number_of_days * employee.resource_calendar_id.hours_per_day

            attendences_hours_percent = 100 - (((employee_required_hours - employee_attendences_hours) / employee_required_hours) * 100)
            holiday_hours_percent = 100 - (((employee_required_hours - employee_weekend_number_hours) / employee_required_hours) * 100)

            real_attendences_hours = employee_attendences_hours + employee_weekend_number_hours
            real_attendences_hours_percent = attendences_hours_percent + holiday_hours_percent
            if employee_attendences_hours == 0:
               real_attendences_hours = 0
               real_attendences_hours_percent = 0

            input_data = {
                'name': employee.local_name,
                'id': employee.id,
                'required_hours': employee_required_hours,
                'holidays_paid_hours': employee_holidays_paid_hours,
                'holidays_unpaid_hours': employee_holidays_unpaid_hours,
                'holidays_formal_hours': employee_holidays_formal_hours,
                'holidays_personal_hours': employee_holidays_personal_hours,
                'early_out_hours': employee_early_out_hours,
                'late_leave_hours': employee_late_leave_hours,
                'attendences_hours': employee_attendences_hours,
                'attendences_hours_percent': attendences_hours_percent,
                'real_attendences_hours_percent': real_attendences_hours_percent,
                'real_attendences_hours': real_attendences_hours,
                'overtime_hours': employee_overtime_hours
            }
            list_values.append(input_data)

        return {
            'data': data['form'],
            'lines': list_values,
        }
