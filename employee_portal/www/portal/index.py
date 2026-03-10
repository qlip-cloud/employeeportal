import frappe
from frappe import _
from employee_portal.utils.permissions import require_employee, get_employee_or_throw
from employee_portal.services.employee_service import EmployeeService
from employee_portal.utils.lookups import get_events, get_announcements


def get_context(context):

    require_employee(lambda: None)()
    
    try:
  
        profile_data = EmployeeService.get_employee_profile()
        
        context.employee = profile_data['employee']
        context.no_cache = 1
        context.show_sidebar = True
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
        
        context.events = get_events(profile_data['employee'].name)
        context.announcements = get_announcements()
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading index page")
        frappe.throw(_("Error al cargar la página de inicio"))