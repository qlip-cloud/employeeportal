import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.leave_application import save_application # type: ignore

def get_context(context):
  get_employee_from_user(context)
  get_modules(context)
  context.employees = frappe.get_all(
      "Employee",
      filters=[["user_id", "!=", frappe.session.user]],  
      fields=["*"]
  )
  return context