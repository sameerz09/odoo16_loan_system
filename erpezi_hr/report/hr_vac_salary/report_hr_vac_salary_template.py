from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, time, timedelta

class ReportVacSalary(models.AbstractModel):
    _name = 'report.erpezi_hr.report_hr_vac_salary_template'
    _description = 'Annual Vacation Settlement PDF Report'



    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        list_values = []
        vac_salaries = self.env['hr.vac.salary'].search([("employee_id.company_id", "=", data['form'].get('company_id')[0])])

        if data['form'].get('vac_salary_id') and data['form'].get('vac_salary_id')[0]:
            vac_salaries = vac_salaries.filtered(lambda line: line.id == data['form'].get('vac_salary_id')[0])
        else:
          if data['form'].get('state') and data['form'].get('state') != False:
              vac_salaries = vac_salaries.filtered(lambda line: line.state == data['form'].get('state'))
          if data['form'].get('date_from') and data['form'].get('date_from') != False:
              vac_salaries = vac_salaries.filtered(lambda line: line.vac_date_from >= datetime.strptime(data['form'].get('date_from'), "%Y-%m-%d").date())
          if data['form'].get('date_to') and data['form'].get('date_to') != False:
              vac_salaries = vac_salaries.filtered(lambda line: line.vac_date_to <= datetime.strptime(data['form'].get('date_to'), "%Y-%m-%d").date())



        for vac_salary in vac_salaries:
            employee_state = self._get_employee_state(vac_salary.state)

            input_data = {
                'name': vac_salary.employee_id.local_name,
                'id': vac_salary.employee_id.id,
                'department_name': vac_salary.employee_id.department_id.name,
                'vac_date_to': vac_salary.vac_date_to,
                'vac_date_from': vac_salary.vac_date_from,
                'total_working_days': vac_salary.total_working_days,
                'employee_annual_salary': vac_salary.employee_annual_salary,
                'perc_working_days': vac_salary.perc_working_days,
                'loans_ded': vac_salary.loans_ded,
                'total_ded': vac_salary.total_ded,
                'saudi_ded': vac_salary.saudi_ded,
                'od': vac_salary.od,
                'net_fin': vac_salary.net_fin,
                'last_day_month': vac_salary.last_day_month,
                'resignation_type': '0',
                'total_vac_days': vac_salary.total_vac_days,
                'employee_gratuity_years': vac_salary.employee_gratuity_years,
                'ofa': vac_salary.ofa,
                'travel_allowance': vac_salary.travel_allowance,
                'project_allowance_other': vac_salary.project_allowance_other,
                'other_allowance': vac_salary.other_allowance,
                'house_allowance': vac_salary.house_allowance,
                'project_allowance': vac_salary.project_allowance,
                'transportation_allowance': vac_salary.transportation_allowance,
                'overtime_allowance': vac_salary.overtime_allowance,
                'total_allowance': vac_salary.total_allowance,
                'other_allocations':  vac_salary.other_allocations,
                'state': employee_state
            }
            list_values.append(input_data)

        return {
            'data': data['form'],
            'lines': list_values,
        }

    def _get_employee_state(self, state):

        employee_state = ''

        if state == 'draft':
            employee_state = 'مسودة'
        elif state == 'submit':
            employee_state = 'مؤكدة وبانتظار الموافقة'
        elif state == 'approve':
            employee_state = 'موافق عليها'
        elif state == 'cancel':
            employee_state = 'ملغية او مرفوضة'

        return employee_state



        return employee_contract_type