# about.py
import frappe
from employee_portal.utils.utils import get_modules # type: ignore
def get_context(context):
    user = frappe.get_doc("User", frappe.session.user)
    employee = frappe.get_doc("Employee", {"user_id": user.name})
    context.employee = employee
    genders = frappe.get_all("Gender", fields=["gender"])
    context.genders = genders
    employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
    context.employment_types = employment_types
    departments = frappe.get_all("Department", fields=["department_name"])  
    context.departments = departments
    designations = frappe.get_all("Designation", fields=["designation_name"])
    context.designations = designations
    get_modules(context)
    return context