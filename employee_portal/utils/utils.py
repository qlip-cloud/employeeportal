import frappe
def get_modules(context):
  context.modules = [
    {"name": "Inicio", "url": "/employee_portal", "icon": "home"},
    {"name": "Mis Datos", "url": "/employee_portal/my_profile", "icon": "user"},
    {"name": "Mis Beneficios", "url": "/employee_portal/my_benefits", "icon": "gift"},
    {"name": "Mis Permihnsos/Ausencias", "url": "/employee_portal/my_leaves", "icon": "calendar-alt"},
    {"name": "Mis Eventos", "url": "/employee_portal/my_events", "icon": "calendar"},
    {"name": "Mis Evaluaciones", "url": "/employee_portal/my_evaluations", "icon": "star"},
    {"name": "Noticias", "url": "/employee_portal/news", "icon": "newspaper"},
    {"name": "Documentos y Políticas", "url": "/employee_portal/documents", "icon": "file"},
    {"name": "Soporte", "url": "/employee_portal/help", "icon": "question-circle"},
  ]
  return context

def get_employee(context):
  user = frappe.get_doc("User", frappe.session.user)
  employee = frappe.get_doc("Employee", {"user_id": user.name})
  if employee:
    context.employee = employee
  else:
    context.employee = user
  return context