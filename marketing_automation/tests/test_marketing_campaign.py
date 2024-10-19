# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.marketing_automation.tests.common import MarketingAutomationCommon
from odoo.tests import tagged, users


@tagged('marketing_automation')
class TestMarketingCampaign(MarketingAutomationCommon):
    @users('user_marketing_automation')
    def test_create_records_with_xml_ids(self):
        # The function tests creation of records.
        # If record is deleted and then re-created it has to get same xmlid.
        email = 'ma.test.new.1@example.com'
        name = 'MATest_new_1'
        create_xmls = {
                'xml_id': 'marketing_automation.mail_contact_temp',
                'values': {
                    'email': email,
                    'name': name,
                }
            }
        self.env['marketing.campaign'].sudo()._create_records_with_xml_ids({'mailing.contact': [create_xmls]})

        # Retrieve the records using the XML IDs and verify they exist
        record = self.env.ref('marketing_automation.mail_contact_temp', raise_if_not_found=False)
        self.assertTrue(record, "Record should exist after creation.")
        self.assertEqual(record.name, name, f"The value should be {name}")
        self.assertEqual(record.email, email, f"The value should be {email}")

        # Now delete the record
        record.unlink()
        self.assertFalse(record.exists(), "Record should be deleted.")
        record = self.env.ref('marketing_automation.mail_contact_temp', raise_if_not_found=False)
        self.assertFalse(record, "The record with XML ID 'marketing_automation.mail_contact_temp' should not exist.")

        # Now re-create record and check values again
        self.env['marketing.campaign'].sudo()._create_records_with_xml_ids({'mailing.contact': [create_xmls]})
        record = self.env.ref('marketing_automation.mail_contact_temp', raise_if_not_found=False)
        self.assertTrue(record, "Record should exist after being re-created.")
        self.assertEqual(record.name, name, f"The value should be {name}")
        self.assertEqual(record.email, email, f"The value should be {email}")
