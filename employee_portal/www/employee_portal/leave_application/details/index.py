import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user

def get_context(context):
  get_modules(context)
  get_employee_from_user(context)
  leave_name = frappe.form_dict.get("name")
  context.leave = frappe.get_doc("Leave Application", leave_name)
  return context