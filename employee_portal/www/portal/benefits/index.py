import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user
def get_context(context):
  benefits = frappe.get_all("Employee Benefit", fields=["title", "description", "attachment", "form"])
  context.benefits = benefits
  get_employee_from_user(context)
  get_modules(context)
  return context