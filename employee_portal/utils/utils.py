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

def get_employee(context):
  if frappe.session.user == "Guest":
      frappe.local.response["type"] = "redirect"
      frappe.local.response["location"] = "/login" 
      return
  user = frappe.get_doc("User", frappe.session.user)
  employee = frappe.get_doc("Employee", {"user_id": user.name})

  if employee:
      context.employee = employee
  else:
      frappe.throw(_("You do not have the necessary permissions to access this page."), frappe.PermissionError)

  return context