import frappe
from frappe import _
from employee_portal.utils.permissions import require_employee, get_employee_or_throw
from employee_portal.services.employee_service import EmployeeService
from employee_portal.utils.lookups import get_leave_types


def get_context(context):

    require_employee(lambda: None)()
    
    try:
  
        profile_data = EmployeeService.get_employee_profile()
        
        context.employee = profile_data['employee']
        context.mentum_hours = profile_data['mentum_hours']
        context.no_cache = 1
        context.show_sidebar = True
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
        
        context.leave_types = get_leave_types()
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading profile page")
        frappe.throw(_("Error al cargar la página de perfil"))