import frappe

from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore

def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
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