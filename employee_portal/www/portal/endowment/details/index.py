import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user

def get_context(context):
  get_modules(context)
  get_employee_from_user(context)
  endowment_id = frappe.form_dict.get("name")
  if endowment_id:
    context.endowment = frappe.get_doc("Endowment", endowment_id)
    context.endowment_items = frappe.get_all(
      "Endowment Item",
      filters={"parent": endowment_id},  
      fields=["article", "quantity", "size", "description"] 
    )
  else:
    context.endowment = None
    context.endowment_items = []
  return context