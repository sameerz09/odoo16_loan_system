
{
    'name': 'ERP_EZI HR',
    'version': '16.0.1.1.0',
    'summary': 'Manage HR',
    'description': """
        Helps you to manage HR of your company's staff.
        """,
    'category': 'HR',
    'author': "Mutaz Zuhairi",
    'company': 'EZI Code',
    'maintainer': 'Mutaz Zuhairi',
    'website': "",
    'depends': [
          'resource','hr_attendance','hr_gratuity_settlement', 'hr_resignation',
    ],
    'data': [
        'report/report.xml',
        'views/attendance/customResourceCalendarAttendance_views.xml',
        'views/res_company/res_company_views.xml',
      #  'views/attendance/hr_attendance_views.xml',
        'wizard/attendance/attendance_report_wizard.xml',
      #  'wizard/hr_gratuity_settlement/hr_gratuity_settlement_report_wizard.xml',
     #   'wizard/hr_vac_salary/hr_vac_salary_report_wizard.xml',
        'report/attendance/report_attendance_template.xml',
    #    'report/hr_gratuity_settlement/report_hr_gratuity_settlement_template.xml',
        'report/attendance/report_attendance_template225.xml',
'report/attendance/report_bonds_template.xml',
   #     'report/hr_vac_salary/report_hr_vac_salary_template.xml'
    ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
