# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_be_codabox_show_iap_token = fields.Boolean(related="company_id.l10n_be_codabox_show_iap_token")

    def l10n_be_codabox_refresh_connection_status(self):
        self.ensure_one()
        return self.company_id._l10n_be_codabox_is_connected()

    def l10n_be_codabox_open_soda_mapping(self):
        self.ensure_one()
        if not self.l10n_be_codabox_soda_journal:
            raise UserError(_("You must select a journal in which SODA's will be imported."))
        wizard = self.env['soda.import.wizard'].create({
            'soda_files': {},
            'soda_code_to_name_mapping': {},
            'company_id': self.company_id.id,
            'journal_id': self.l10n_be_codabox_soda_journal.id,
        })
        return {
            'name': _('SODA Mapping'),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'view_mode': 'form',
            'view_id': self.env.ref('l10n_be_codabox_bridge.soda_import_wizard_view_form_codabox').id,
            'res_model': 'soda.import.wizard',
            'res_id': wizard.id,
            'target': 'new',
            'context': {
                'soda_mapping_save_only': True,
            },
        }
