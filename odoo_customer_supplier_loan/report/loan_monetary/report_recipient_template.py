from odoo import models, api, fields
class Recipienttemplate(models.AbstractModel):
    _name = 'report.odoo_customer_supplier_loan.report_recipient_template'
    @api.model
    def _get_report_values(self, docids, data):
        """in this function can access the data returned from the button
        click function"""
        model_id = data['report.recipient.template']
        value = []
        query = """SELECT *
                        FROM sale_order as so
                        JOIN sale_order_line AS sl ON so.id = sl.sale_order_id
                        WHERE sl.id = %s"""
        value.append(report.recipient.template)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }