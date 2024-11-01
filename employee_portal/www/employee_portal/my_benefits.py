import frappe
from employee_portal.utils.utils import get_modules, get_employee
def get_context(context):
  benefits = frappe.get_all("Employee Benefit", fields=["title", "description", "attachment", "form"])
  context.benefits = benefits
  get_employee(context)
  get_modules(context)
  return context