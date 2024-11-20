import frappe
from frappe import _
from employee_portal.utils.utils import get_employee_from_user
def get_context(context):
    get_employee_from_user(context)
    genders = frappe.get_all("Gender", fields=["gender"])
    context.genders = genders
    employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
    context.employment_types = employment_types
    departments = frappe.get_all("Department", fields=["department_name"])  
    context.departments = departments
    designations = frappe.get_all("Designation", fields=["designation_name"])
    context.designations = designations
    employee = context.employee
    context.employee = employee
    csfr_token = frappe.sessions.get_csrf_token()
    frappe.db.commit()
    context.csrf_token = csfr_token
    return context