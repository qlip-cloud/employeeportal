import frappe
from frappe import _
def get_modules(context):
  context.modules = [
    {"name": "Inicio", "url": "/portal"},
    {"name": "Mis Datos", "url": "/portal/profile"},
    {"name": "Mis Eventos", "url": "/portal/events"},
    {"name": "Mis Permisos/Ausencias", "url": "/portal/leave_application"},
    {"name": "Mis Vacaciones", "url": "/portal/vacations"},
    {"name": "Mi Dotación", "url": "/portal/endowment"},
    {"name": "Mis Beneficios", "url": "/portal/benefits"},
    {"name": "Mis Evaluaciones", "url": "/portal/performance_review"},
    {"name": "Documentos y Políticas", "url": "/portal/documents"},
    {"name": "Soporte", "url": "/portal/help"},
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
