import frappe

DOCTYPE = "Employee"

def update_employee(employee_id, data):
  try:
    employee = frappe.get_doc(DOCTYPE, employee_id)
    for key, value in data.items():
      setattr(employee, key, value)
    employee.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": "Employee updated successfully"}
  except Exception as e:
    frappe.db.rollback()
    return {"status": "error", "message": str(e)}

