import frappe
from frappe import _
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.update import update_employee

def get_context(context):
  get_employee_from_user(context)
  get_modules(context)
  context.genders = frappe.get_all("Gender", fields=["gender"])
  context.employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
  context.departments = frappe.get_all("Department", fields=["department_name"])  
  context.designations = frappe.get_all("Designation", fields=["designation_name"])
  
  context.csrf_token = frappe.sessions.get_csrf_token()
  context.no_cache = 1

  return context

@frappe.whitelist()
def save_profile(employee_id, data):
  try:
    if isinstance(data, str):
      data = frappe.parse_json(data)
    
    if not data.get("first_name"):
      raise Exception(_("First Name is required"))
    if not data.get("last_name"):
      raise Exception(_("Last Name is required"))
    if not data.get("dob"):
      raise Exception(_("Date of Birth is required"))
    if not data.get("gender"):
      raise Exception(_("Gender is required"))
    update_employee(employee_id, data)
    return {"status": "success", "message": "Profile updated successfully"}
  except Exception as e:
    return {"status": "error", "message": str(e)}
