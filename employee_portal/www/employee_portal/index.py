import frappe
def get_context(context):
  user = frappe.get_doc("User", frappe.session.user)
  announcements = frappe.get_all("Announcement", fields=["name", "title", "content", "published_on", "image"], order_by="published_on desc")
  context.user = user
  context.announcements = announcements
  context.modules = [
    {"name": "Inicio", "url": "/employee_portal", "icon": "home"},
    {"name": "Mis Datos", "url": "/employee_portal/my_profile", "icon": "user"},
    {"name": "Mis Beneficios", "url": "/employee_portal/my_benefits", "icon": "gift"},
    {"name": "Mis Permisos/Ausencias", "url": "/employee_portal/my_leaves", "icon": "calendar-alt"},
    {"name": "Mis Eventos", "url": "/employee_portal/my_events", "icon": "calendar"},
    {"name": "Mis Evaluaciones", "url": "/employee_portal/my_evaluations", "icon": "star"},
    {"name": "Noticias", "url": "/employee_portal/news", "icon": "newspaper"},
    {"name": "Documentos y Políticas", "url": "/employee_portal/documents", "icon": "file"},
    {"name": "Soporte", "url": "/employee_portal/help", "icon": "question-circle"},
  ]
  return context