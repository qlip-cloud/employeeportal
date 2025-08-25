import frappe
from frappe import _
from frappe.utils import get_url, getdate,today # type:ignore

def get_active_evaluations(employee_id):
    evaluations = frappe.get_all("Appraisal", filters={"employee": employee_id, "status": "Draft"}, fields=["*"])
    return evaluations

def get_completed_evaluations(employee_id):
    evaluations = frappe.get_all("Appraisal", filters={"employee": employee_id, "status": "Submitted"}, fields=["*"])
    return evaluations