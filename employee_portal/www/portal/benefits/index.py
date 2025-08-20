import frappe
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore

def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  benefits = frappe.get_all("Employee Benefit", fields=["title", "description", "attachment", "form"])
  context.benefits = benefits
  
  
  return context