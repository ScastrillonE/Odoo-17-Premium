# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.sale_planning.tests.common import TestCommonSalePlanning


class TestProjectTask(TestCommonSalePlanning):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'Project 1',
            'allow_timesheets': True,
            'allow_billable': True,
            'sale_line_id': cls.plannable_sol.id,
            'partner_id': cls.planning_partner.id,
        })

    def test_record_timesheet_into_task(self):
        """ Test record timesheet into a task

            Test Case:
            =========
            1. Create a task in the project
            2. Record timesheet on the task
            3. Check that the timesheet is correctly recorded
            4. Check the planning slot generated by the SOL is correctly adapted
        """
        self.plannable_so.action_confirm()
        planning_slot = self.env['planning.slot'].search([('sale_line_id', '=', self.plannable_sol.id), ('start_datetime', '=', False)])
        self.assertEqual(len(planning_slot), 1)
        self.assertEqual(planning_slot.allocated_hours, 10, "Should be equal to the quantity ordered set on the SOL.")
        task = self.env['project.task'].create({
            'name': 'Task 1',
            'project_id': self.project.id,
        })
        self.plannable_sol.update({'task_id': task, 'project_id': self.project})
        self.assertEqual(task.sale_line_id, self.plannable_sol, "Should get the SOL set in the project linked.")
        timesheet = self.env['account.analytic.line'].create({
            'name': 'Timesheet 1',
            'project_id': self.project.id,
            'task_id': task.id,
            'unit_amount': 1.0,
            'employee_id': self.employee_wout.id,
        })
        self.assertEqual(timesheet.so_line, self.plannable_sol, "Should get the SOL set in the task linked.")
        self.assertEqual(planning_slot.allocated_hours, 10, "Should still be equal to the quantity ordered set on the SOL")
        timesheet.action_validate_timesheet()
        self.assertTrue(timesheet.validated, "Timesheet should be validated.")
        self.assertEqual(planning_slot.allocated_hours, 9, "Should be equal to the quantity ordered set on the SOL minus the validated timesheet.")
