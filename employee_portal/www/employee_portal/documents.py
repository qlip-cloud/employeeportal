import frappe
from employee_portal.utils.utils import get_modules, get_employee

def get_context(context):
  get_modules(context)
  get_employee(context)
  context.documents = frappe.get_all("Document", fields=["*"])
  return context