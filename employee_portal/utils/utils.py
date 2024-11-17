import frappe
from frappe import _
def get_modules(context):
  context.modules = [
    {"name": "Inicio", "url": "/employee_portal"},
    {"name": "Mis Datos", "url": "/employee_portal/my_profile"},
    {"name": "Mis Eventos", "url": "/employee_portal/my_events"},
    {"name": "Mis Permisos/Ausencias", "url": "/employee_portal/my_leaves"},
    {"name": "Mis Beneficios", "url": "/employee_portal/my_benefits"},
    {"name": "Mis Evaluaciones", "url": "/employee_portal/my_evaluations"},
    {"name": "Dotación", "url": "/employee_portal/endowment"},
    {"name": "Documentos y Políticas", "url": "/employee_portal/documents"},
    {"name": "Soporte", "url": "/employee_portal/help"},
  ]
  return context

def get_employee_from_user(context, user=None):
    """
    Fetches the Employee document linked to the given user.

    Args:
        user (str): The user ID (optional). Defaults to the current session user.

    Returns:
        frappe._dict: The Employee document if found.

    Raises:
        frappe.PermissionError: If the user is not logged in or not linked to an employee.
    """
    if not user:
      user = frappe.session.user

    if user == "Guest":
      raise frappe.PermissionError("Log in to access this page.")

    try:
      user_doc = frappe.get_doc("User", user)
      employee = frappe.get_doc("Employee", {"user_id": user_doc.name})
      context.employee = employee
      return context
    except frappe.DoesNotExistError:
      raise frappe.PermissionError("You are not authorized to access this page.")
