import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.leave_application import save_application # type: ignore

def get_context(context):
  get_employee_from_user(context)
  get_modules(context)
  leave_types = frappe.get_all("Leave Type", fields=["*"])
  context.leave_types = leave_types
  return context

@frappe.whitelist()
def send_application(data):
  try:
    if isinstance(data, str):
      data = frappe.parse_json(data)
    if not data.get("leave_type"):
      raise Exception("Leave Type is required")
    if not data.get("from_date"):
      raise Exception("From Date is required")
    if not data.get("to_date"):
      raise Exception("To Date is required")
    
    save_application(data)
    return {"status": "success", "message": "Leave Application saved successfully"}
  except Exception as e:
    return {"status": "error", "message": str(e)}
    

    


