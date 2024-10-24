import frappe
from employee_portal.utils.utils import get_modules, get_employee
def get_context(context):
  get_modules(context)
  get_employee(context)
  context.leaves = frappe.get_all("Leave Application", filters={"employee": context.employee.name}, fields=["*"])
  return context