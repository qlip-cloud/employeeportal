import frappe

DOCTYPE = "Leave Application"

def save_application(data):
  try:
    leave_application = frappe.new_doc(DOCTYPE)
    for key, value in data.items():
      setattr(leave_application, key, value)
    leave_application.flags.notify = False
    leave_application.flags.notify_leave_approver = False
    leave_application.flags.notify_employee = False
    leave_application.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": "Leave Application saved successfully"}
  except Exception as e:
    frappe.db.rollback()
    frappe.log_error(f"Error in save_application: {str(e)}")
    return {"status": "error", "message": str(e)}
