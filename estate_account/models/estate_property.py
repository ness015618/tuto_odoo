from odoo import models, Command
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold(self):
        _logger.warning("🚨 estate_account's action_mark_as_sold() CALLED")
        
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise ValueError("Aucun journal de vente trouvé. Veuillez en créer un.")

        for property in self:
            invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create({
                'move_type': 'out_invoice',
                'partner_id':  property.buyer_id.id,
                'name': "Invoice",
                "journal_id": journal.id,
                'invoice_line_ids': [
                    Command.create({
                        "name": "Invoice line",
                        "quantity": 1,
                        "price_unit": (property.selling_price * 0.06) + 100
                    })
                ]
                })
            
            _logger.warning(f"✅ Invoice created: ID={invoice.id}, Partner={invoice.partner_id.name}, State={invoice.state}")

        return super().action_mark_as_sold()