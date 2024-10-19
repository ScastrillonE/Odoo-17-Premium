/** @odoo-module **/

import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add('test_shop_floor', {test: true, steps: () => [
    {
        content: 'Select the workcenter the first time we enter in shopfloor',
        trigger: 'button input[name="Savannah"]'
    },
    {
        content: 'Select the second workcenter',
        trigger: 'button input[name="Jungle"]'
    },
    { trigger: '.modal-footer button:contains("Confirm")' },
    {
        content: 'Open the employee panel',
        trigger: 'button[name="employeePanelButton"]'
    },
    {
        content: 'Add operator button',
        trigger: 'button:contains("Operator")'
    },
    {
        content: 'Select the Marc Demo employee',
        trigger: '.modal-body .popup .selection div:contains("Marc Demo")'
    },
    {
        content: 'Go to workcenter Savannah from MO card',
        trigger: '.o_mrp_record_line button span:contains("Savannah")'
    },
    {
        content: 'Start the workorder on header click',
        trigger: '.o_finished_product span:contains("Giraffe")'
    },
    {
        content: 'Register production check',
        trigger: '.o_mrp_record_line .btn.fa-plus'
    },
    {
        content: 'Instruction check via form',
        trigger: '.o_mrp_record_line span:contains("Instructions")'
    },
    { trigger: 'button[barcode_trigger="Next"]' },
    {
        content: 'Component not tracked registration and continue production',
        trigger: 'button[barcode_trigger="continue"]'
    },
    {
        content: 'Add 2 units',
        trigger: '.o_field_widget[name="qty_done"] input',
        extra_trigger: '.o_field_widget[name="qty_done"] input:propValue("0.00")',
        run: 'text 2',
    },
    {
        trigger: 'button[barcode_trigger="Next"]',
        extra_trigger: '.o_field_widget[name="qty_done"] input:propValue("2.00")',
    },
    { trigger: '.modal-header .btn-close' },
    {
        content: 'Fast check last instruction step',
        trigger: '.o_mrp_record_line .fa-square-o',
    },
    {
        content: 'Close first operation',
        trigger: '.card-footer button[barcode_trigger="cloWO"]',
    },
    {
        content: 'Switch to second workcenter for next operation',
        extra_trigger: '.o_nocontent_help',
        trigger: '.o_control_panel_actions button:contains("Jungle")',
    },
    {
        content: 'Open the setting menu',
        trigger: '.card-footer button.fa-ellipsis-v',
    },
    {
        content: 'Move the operation back to first workcenter',
        trigger: 'button[name="moveToWorkCenter"]',
    },
    { trigger: '.o_mrp_workcenter_dialog button input[name="Savannah"]' },
    { trigger: '.modal-footer button:contains("Confirm")' },
    {
        content: 'Switch to first workcenter for operation',
        trigger: '.o_control_panel_actions button:contains("Savannah")',
    },
    {
        content: 'Refresh',
        trigger: '.fa-refresh',
    },
    {
        content: 'Open the setting menu',
        trigger: '.card-footer button.fa-ellipsis-v',
    },
    {
        content: 'Add an operation button',
        trigger: 'button[name="addComponent"]',
    },
    {
        content: 'Add Color',
        trigger: '.o_field_widget[name=product_id] input',
        run: 'text color'
    },
    { trigger: '.ui-menu-item > a:contains("Color")' },
    { trigger: 'button[name=add_product]' },
    { trigger: '.o_mrp_record_line .btn-secondary:contains("2")' },
    { trigger: 'button[barcode_trigger=cloWO]' },
    { trigger: 'button[barcode_trigger=cloMO]' },
    {
        content: 'Leave shopfloor',
        extra_trigger: '.o_nocontent_help',
        trigger: '.o_home_menu .fa-sign-out',
    },
    {
        trigger: '.o_home_menu',
        isCheck: true,
    }
]})
