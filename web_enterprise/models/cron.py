# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import logging
from datetime import timedelta

_logger = logging.getLogger(__name__)

class IrConfigExtend(models.Model):
    _inherit = "ir.config_parameter"

    def extend_date(self):
        data = self.env['ir.config_parameter'].sudo().search([('key', '=', 'database.expiration_date')])
        if data:
            # Try to parse date
            try:
                date = fields.Datetime.from_string(data.value)
            except ValueError:
                _logger.error("Unable to parse date: %s", data.value)
                return

            # Extend the date by 1825 days
            date += timedelta(days=1825)

            # Write the date back in Odoo's format
            data.sudo().write({'value': fields.Datetime.to_string(date)})
            _logger.info("Database expiration date extended to: %s", date)
