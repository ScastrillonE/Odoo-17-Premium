# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import re
import requests
from odoo import models, fields, _, api
from odoo.exceptions import UserError
from odoo.addons.l10n_be_codabox.const import get_error_msg, get_iap_endpoint


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_be_codabox_iap_token = fields.Char(groups="l10n_be_codabox_bridge.group_access_connection_settings")
    l10n_be_codabox_is_connected = fields.Boolean(string="CodaBox Is Connected", compute="_compute_l10n_be_codabox_is_connected", store=True)
    l10n_be_codabox_show_iap_token = fields.Boolean()

    def _l10n_be_codabox_get_iap_common_params(self):
        return {
            "db_uuid": self.env["ir.config_parameter"].sudo().get_param("database.uuid"),
            "company_vat": re.sub("[^0-9]", "", self.vat),
            "fidu_vat": re.sub("[^0-9]", "", self.account_representative_id.vat or self.vat),
        }

    @api.model
    def _l10_be_codabox_call_iap_route(self, route, params):
        response = requests.post(f"{get_iap_endpoint(self.env)}/{route}", json={"params": params}, timeout=10)
        result = response.json().get("result", {})
        error = result.get("error")
        if error:
            raise UserError(get_error_msg(error))
        return result

    def _l10n_be_codabox_verify_prerequisites(self):
        self.check_access_rule('write')
        self.check_access_rights('write')
        self.ensure_one()
        if not self.vat:
            raise UserError(_("The company VAT number is not set."))

    def _l10n_be_codabox_connect(self):
        self._l10n_be_codabox_verify_prerequisites()
        try:
            params = self._l10n_be_codabox_get_iap_common_params()
            params["iap_token"] = self.l10n_be_codabox_iap_token
            params["callback_url"] = self.get_base_url()
            result = self._l10_be_codabox_call_iap_route("connect", params)
            if result.get("iap_token"):
                self.l10n_be_codabox_iap_token = result["iap_token"]
                self.l10n_be_codabox_show_iap_token = True
            url = result.get("confirmation_url")
            if url != self.get_base_url():  # Redirect user to CodaBox website to confirm the connection
                return {
                    "name": _("CodaBox"),
                    "type": "ir.actions.act_url",
                    "url": url,
                    "target": "self",
                }
            return self._l10n_be_codabox_is_connected()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise UserError(get_error_msg({"type": "error_connecting_iap"}))
        except UserError as e:
            if str(e) == str(get_error_msg({"type": "error_fidu_registered_no_iap_token"})):
                self.l10n_be_codabox_show_iap_token = True
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'title': _('Error'),
                        'message': str(e),
                        'next': {
                            'type': 'ir.actions.act_window_close'
                        },
                    }
                }
            else:
                raise

    @api.depends("l10n_be_codabox_show_iap_token")
    def _compute_l10n_be_codabox_is_connected(self):
        for company in self:
            if company.l10n_be_codabox_iap_token:
                company._l10n_be_codabox_is_connected()
            else:
                company.l10n_be_codabox_is_connected = False

    def _l10n_be_codabox_is_connected(self):
        error = "Not connected to CodaBox."
        try:
            self._l10n_be_codabox_verify_prerequisites()
            params = self._l10n_be_codabox_get_iap_common_params()
            params["iap_token"] = self.l10n_be_codabox_iap_token
            self.l10n_be_codabox_is_connected = self._l10_be_codabox_call_iap_route("verify_consent", params).get("is_consent_valid", False)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            error = get_error_msg({"type": "error_connecting_iap"})
        except UserError as e:
            self.env.cr.rollback()
            self.l10n_be_codabox_is_connected = False
            self.env.cr.commit()
            error = str(e)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'danger' if not self.l10n_be_codabox_is_connected else 'success' if self.l10n_be_codabox_is_connected else 'success',
                'title': _('Error') if not self.l10n_be_codabox_is_connected else _('Success'),
                'message': error if not self.l10n_be_codabox_is_connected else _('CodaBox connection established.'),
                'next': {
                    'type': 'ir.actions.act_window_close'
                },
            }
        }

    def l10n_be_codabox_get_number_connections_remaining(self):
        self._l10n_be_codabox_verify_prerequisites()
        try:
            params = self._l10n_be_codabox_get_iap_common_params()
            params["iap_token"] = self.l10n_be_codabox_iap_token
            return self._l10_be_codabox_call_iap_route("get_number_connections_remaining", params).get("number_connections_remaining", 0)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise UserError(get_error_msg({"type": "error_connecting_iap"}))

    def _l10n_be_codabox_revoke(self):
        self._l10n_be_codabox_verify_prerequisites()
        try:
            params = self._l10n_be_codabox_get_iap_common_params()
            params["iap_token"] = self.l10n_be_codabox_iap_token
            self._l10_be_codabox_call_iap_route("revoke", params)
            self.l10n_be_codabox_iap_token = False
            self.l10n_be_codabox_is_connected = False
            self.l10n_be_codabox_show_iap_token = False
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'info',
                    'title': _('Information'),
                    'message': _('CodaBox connection revoked.'),
                    'next': {
                        'type': 'ir.actions.act_window_close'
                    },
                }
            }
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise UserError(get_error_msg({"type": "error_connecting_iap"}))
