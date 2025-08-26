import frappe, json


@frappe.whitelist()
def save_profile(employee_id, data):
  try:
    current_user = frappe.session.user

    employee = frappe.get_doc("Employee", employee_id)

    if employee.user_id.lower() != current_user.lower():
      return {
        "status": "error",
        "error": "No tienes permiso para editar este perfil.",
      }

    if isinstance(data, str):
      data=json.loads(data)

    employee = frappe.get_doc("Employee", employee_id)
    employee.update(data)
    employee.save(ignore_permissions=True)
    return {"status": "success"}
  except Exception as e:
    return {"status": "error", "error": str(e)}
