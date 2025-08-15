import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user
def get_context(context):
  get_modules(context)
  get_employee_from_user(context)
  context.evaluations = frappe.get_all("Quality Feedback", filters={"document_name": context.employee.user_id}, fields=["*"])
  return context