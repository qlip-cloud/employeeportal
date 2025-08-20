import frappe
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore

def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  context.endowments = frappe.get_all("Endowment", filters={"employee": context.employee.name}, fields=["*"])
  return context