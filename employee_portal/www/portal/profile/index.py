import frappe
from frappe import _
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  context.genders = frappe.get_all("Gender", fields=["gender"])
  context.employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
  context.departments = frappe.get_all("Department", fields=["department_name"])  
  context.designations = frappe.get_all("Designation", fields=["designation_name"])
  
  context.csrf_token = frappe.sessions.get_csrf_token()
  context.no_cache = 1

  return context
