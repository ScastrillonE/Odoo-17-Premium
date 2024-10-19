# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CodaBox Bridge',
    'version': '1.0',
    'author': 'Odoo',
    'website': 'https://www.odoo.com/documentation/17.0/applications/finance/fiscal_localizations/belgium.html#codabox',
    'category': 'Accounting/Localizations',
    'description': 'CodaBox integration to retrieve your CODA and SODA files.',
    'depends': [
        'account_reports',
        'l10n_be_codabox',
    ],
    'auto_install': True,
    'data': [
        'data/ir_cron.xml',
        'security/l10n_be_codabox_security.xml',
        'views/res_config_settings_views.xml',
        'wizard/soda_import_wizard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_be_codabox_bridge/static/src/components/**/*',
        ],
    },
    'license': 'OEEL-1',
}
