import frappe
from frappe import _
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore

def get_context(context):
    is_guest()
    is_employee()
    context.employee = get_employee()
    genders = frappe.get_all("Gender", fields=["gender"])
    context.genders = genders
    employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
    context.employment_types = employment_types
    designations = frappe.get_all("Designation", fields=["designation_name"])
    context.designations = designations
    employee = context.employee
    context.employee = employee
    evaluation_name = frappe.form_dict.name
    if not evaluation_name:
        frappe.throw("No se especificó la evaluación")

    evaluation = frappe.get_doc("Evaluation", evaluation_name)

    context.evaluation = evaluation
    return context  