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

    required_fields = ["leave_type", "from_date", "to_date", "department"]
    for field in required_fields:
      if not data.get(field):
        raise Exception(f"{field.replace('_', ' ').title()} is required")

    response = save_application(data) 

    if response.get("status") == "error":
      frappe.log_error(f"Error saving leave application: {response.get('message')}")
      return {"status": "error", "message": response.get("message")}

    return {"status": "success", "message": "Leave Application saved successfully :)"}

  except Exception as e:
    frappe.log_error(f"Exception in send_application: {str(e)}")
    return {"status": "error", "message": str(e)}


    


