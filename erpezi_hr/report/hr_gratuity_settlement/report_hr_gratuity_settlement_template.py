from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, time, timedelta

class ReportGratuitySettlement(models.AbstractModel):
    _name = 'report.erpezi_hr.report_hr_gratuity_settlement_template'
    _description = 'End of Service PDF Report'



    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        list_values = []
        resignations = self.env['hr.resignation'].search([("employee_id.company_id", "=", data['form'].get('company_id')[0])])

        if data['form'].get('resignation_id') and data['form'].get('resignation_id')[0]:
            resignations = resignations.filtered(lambda line: line.id == data['form'].get('resignation_id')[0])
        else:
          if data['form'].get('state') and data['form'].get('state') != False:
              resignations = resignations.filtered(lambda line: line.state == data['form'].get('state'))
          if data['form'].get('date_from') and data['form'].get('date_from') != False:
              resignations = resignations.filtered(lambda line: line.expected_revealing_date >= datetime.strptime(data['form'].get('date_from'), "%Y-%m-%d").date())
          if data['form'].get('date_to') and data['form'].get('date_to') != False:
              resignations = resignations.filtered(lambda line: line.expected_revealing_date <= datetime.strptime(data['form'].get('date_to'), "%Y-%m-%d").date())
          if data['form'].get('employee_contract_type') and data['form'].get('employee_contract_type') != False:
              resignations = resignations.filtered(lambda line: line.gratuity_id.employee_contract_type == data['form'].get('employee_contract_type'))
          if data['form'].get('resignation_type') and data['form'].get('resignation_type') != False:
              resignations = resignations.filtered(lambda line: line.resignation_type == data['form'].get('resignation_type'))



        for resign in resignations:
            employee_state = self._get_employee_state(resign.state)
            employee_contract_type = self._get_contract_type(resign.gratuity_id.employee_contract_type)
            employee_resignation_type = self._get_contract_resignation_type(resign.resignation_type)

            input_data = {
                'name': resign.employee_id.local_name,
                'id': resign.employee_id.id,
                'department_name': resign.department_id.name,
                'joined_date': resign.joined_date,
                'approved_revealing_date': resign.approved_revealing_date,
                'expected_revealing_date': resign.expected_revealing_date,
                'resignation_type': employee_resignation_type,
                'notice_period': resign.notice_period,
                'employee_gratuity_years': resign.gratuity_id.employee_gratuity_years,
                'employee_contract_type': employee_contract_type,
                'employee_basic_salary': resign.gratuity_id.employee_basic_salary,
                'annual_vacation_remaining_cash': resign.gratuity_id.annual_vacation_remaining_cash,
                'unpaid_vacation_num': resign.gratuity_id.unpaid_vacation_num,
                'annual_vacation_remaining': resign.gratuity_id.annual_vacation_remaining,
                'total_loan_lines_remaining': resign.gratuity_id.total_loan_lines_remaining,
                'employee_gratuity_amount': resign.gratuity_id.employee_gratuity_amount,
                'total_employee_gratuity_amount': resign.gratuity_id.total_employee_gratuity_amount,
                'payslip_net_salary': resign.gratuity_id.payslip_net_salary,
                'absence_num':  resign.gratuity_id.absence_num,
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
        elif state == 'confirm':
            employee_state = 'مؤكدة وبانتظار الموافقة'
        elif state == 'approved':
            employee_state = 'موافق عليها'
        elif state == 'cancel':
            employee_state = 'ملغية او مرفوضة'

        return employee_state

    def _get_contract_resignation_type(self, resignation_type):

        employee_resignation_type = ''

        if resignation_type == 'normalResLess10':
            employee_resignation_type = 'استقالة عادية لأقل من 10 سنوات'
        elif resignation_type == 'normalResMore10':
            employee_resignation_type = 'استقالة عادية لأكثر من 10 سنوات'
        elif resignation_type == 'endContractNo80':
            employee_resignation_type = 'انتهاء العقد بناءً على إنهاء العقد بناءً على المادة رقم 80'
        elif resignation_type == 'endContractNo81':
            employee_resignation_type = 'انتهاء العقد بناءً على إنهاء العقد بناءً على المادة رقم 81'
        elif resignation_type == 'terminationContract':
            employee_resignation_type = 'إنهاء العقد'

        return employee_resignation_type

    def _get_contract_type(self, contract_type):

        employee_contract_type = ''

        if contract_type == 'limited':
            employee_contract_type = 'محدود'
        elif contract_type == 'unlimited':
            employee_contract_type = 'غير محدود'


        return employee_contract_type