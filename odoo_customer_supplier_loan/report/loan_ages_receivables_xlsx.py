from odoo import models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp

class LoanAgesReceivables(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.loan_ages_receivables_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        # Setup the worksheet and formatting
        sheet = workbook.add_worksheet("Loan Report")
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        cell_format2 = workbook.add_format({'align': 'center', 'border': True})

        # Set column properties
        sheet.set_column(0, 0, None, cell_format)
        sheet.merge_range('Y1:AH1', 'Loan Aging Report', cell_format)

        # Table header
        row = 1
        col = 0
        headers = [
            'Loan Classification', 'Total Balance', 'Total Due', '>361 Days', '180-360 Days',
            '121-180 Days', '91-120 Days', '61-90 Days', '31-60 Days', '0-30 Days', 'Currency', 'Beneficiary Name'
        ]
        for i, header in enumerate(headers):
            sheet.write(row, col + 23 + i, header, cell_format)

        # Fetching loan data
        loaners = self.env['partner.loan.details'].search([
            '|', '|', ("state", "=", 'disburse'), ("state", "=", '1disburse'), ("state", "=", '2disburse')
        ])

        for loaner in loaners:
            row += 1
            loan_data = self.get_loan_data(loaner)

            # Write data to the report
            sheet.write(row, col + 29, loan_data['loan_type'], cell_format2)
            sheet.write(row, col + 33, loan_data['currency'], cell_format2)
            sheet.write(row, col + 34, loan_data['beneficiary_name'], cell_format2)

            # Aging details
            sheet.write(row, col + 32, loan_data['aging_0'], cell_format2)
            sheet.write(row, col + 31, loan_data['aging_30'], cell_format2)
            sheet.write(row, col + 30, loan_data['aging_60'], cell_format2)
            sheet.write(row, col + 29, loan_data['aging_90'], cell_format2)
            sheet.write(row, col + 28, loan_data['aging_120'], cell_format2)
            sheet.write(row, col + 27, loan_data['aging_180'], cell_format2)
            sheet.write(row, col + 26, loan_data['aging_360'], cell_format2)
            sheet.write(row, col + 25, loan_data['total_ages'], cell_format2)
            sheet.write(row, col + 24, loaner.total_amount_due, cell_format2)
            sheet.write(row, col + 23, loan_data['loan_class'], cell_format2)

    def get_loan_data(self, loaner):
        # Helper function to process loaner data
        data = {}
        data['loan_type'] = self.get_loan_type(loaner.loan_class)
        data['currency'] = loaner.currency_id.name
        data['beneficiary_name'] = loaner.partner_id.name

        # Process aging details
        aging_data = self.calculate_aging(loaner)
        data.update(aging_data)

        # Determine loan classification based on aging
        data['loan_class'] = self.classify_loan(aging_data)

        return data

    def get_loan_type(self, loan_type_code):
        # Mapping loan type codes to descriptive names
        if loan_type_code == 'islamic':
            return 'Islamic'
        elif loan_type_code == 'commercial':
            return 'Commercial'
        return ''

    def calculate_aging(self, loaner):
        # Calculate aging based on installment details
        aging = {
            'aging_0': 0, 'aging_30': 0, 'aging_60': 0, 'aging_90': 0,
            'aging_120': 0, 'aging_180': 0, 'aging_360': 0, 'total_ages': 0
        }
        current_date = datetime.now().date()
        installments = self.env['partner.loan.installment.details'].search([('loan_id', '=', loaner.id), ('state', '=', 'unpaid')])

        for installment in installments:
            if installment.date_to + relativedelta(days=0) <= current_date <= installment.date_to + relativedelta(days=30):
                aging['aging_0'] += installment.remains
            elif installment.date_to + relativedelta(days=31) <= current_date <= installment.date_to + relativedelta(days=60):
                aging['aging_30'] += installment.remains
            elif installment.date_to + relativedelta(days=61) <= current_date <= installment.date_to + relativedelta(days=90):
                aging['aging_60'] += installment.remains
            elif installment.date_to + relativedelta(days=91) <= current_date <= installment.date_to + relativedelta(days=120):
                aging['aging_90'] += installment.remains
            elif installment.date_to + relativedelta(days=121) <= current_date <= installment.date_to + relativedelta(days=180):
                aging['aging_120'] += installment.remains
            elif installment.date_to + relativedelta(days=181) <= current_date <= installment.date_to + relativedelta(days=360):
                aging['aging_180'] += installment.remains
            elif installment.date_to + relativedelta(days=361) <= current_date:
                aging['aging_360'] += installment.remains

        aging['total_ages'] = sum(aging.values())
        return aging

    def classify_loan(self, aging):
        # Loan classification based on aging data
        if aging['aging_360'] > 0:
            return 'Loss'
        elif aging['aging_180'] > 0:
            return 'Under Watch'
        elif aging['aging_90'] > 0:
            return 'Overdue'
        elif aging['aging_30'] > 0:
            return 'Monitored'
        else:
            return 'Current'
