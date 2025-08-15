import frappe
from frappe import _

def is_guest():
  frappe.clear_cache()
  frappe.website.render.clear_cache()
  is_guest = (frappe.session.user == 'Guest')
  if is_guest:
    frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
  return is_guest

def is_employee():
  frappe.clear_cache()
  frappe.website.render.clear_cache()
  is_employee = frappe.db.exists("Employee", {"user_id": frappe.session.user})
  if not is_employee:
    frappe.throw(_("Necesita iniciar sesión como empleado para acceder a esta página"), frappe.PermissionError)
  return is_employee

