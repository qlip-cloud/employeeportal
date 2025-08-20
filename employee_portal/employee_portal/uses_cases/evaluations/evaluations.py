import frappe
from frappe import _
from frappe.utils import get_url, getdate,today # type:ignore

def get_evaluations(user):
    evaluations = frappe.get_all("Performance Evaluation", filters={"owner": user}, fields=["name", "kra_template", "status", "appraisal_date"])
    return evaluations