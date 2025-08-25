import frappe

from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore
from employee_portal.employee_portal.uses_cases.evaluations.evaluations import get_active_evaluations, get_completed_evaluations  # type: ignore


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  context.active_evaluations = get_active_evaluations(context.employee.name)
  context.completed_evaluations = get_completed_evaluations(context.employee.name)

  return context