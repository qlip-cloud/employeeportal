import frappe
from frappe import _
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore


def get_context(context):
    is_guest()
    is_employee()
    context.employee = get_employee()
    employee = context.employee
    context.employee = employee
    evaluation_name = frappe.form_dict.name
    if not evaluation_name:
        frappe.throw("No se especificó la evaluación")

    evaluation = frappe.get_doc("Appraisal", evaluation_name)

    context.is_editable = (
        evaluation.status == "Draft" and evaluation.employee == employee.name
    )
    branch = frappe.get_doc("Branch", employee.branch)
    context.branch_leader = frappe.get_value(
        "Employee", branch.leader, "employee_name"
    ) if branch.leader else ""
    context.evaluation = evaluation
    return context  