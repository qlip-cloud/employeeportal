import frappe

DOCTYPE = "Leave Application"

def save_application(data):
  try:
    leave_application = frappe.new_doc(DOCTYPE)
    for key, value in data.items():
      setattr(leave_application, key, value)
    leave_application.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": "Leave Application saved successfully"}
  except Exception as e:
    frappe.db.rollback()
    return {"status": "error", "message": str(e)}