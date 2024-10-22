# about.py
import frappe

def get_context(context):
    employee = frappe.get_doc("Employee", frappe.session.user)
    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name", "employee_name"])
    context.employee = employee
    return context