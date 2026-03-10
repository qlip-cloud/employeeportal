import frappe
from frappe import _
from employee_portal.utils.permissions import require_employee, get_employee_or_throw
from employee_portal.services.employee_service import EmployeeService
from employee_portal.services.leave_service import LeaveService


def get_context(context):

    require_employee(lambda: None)()
    
    try:
  
        profile_data = EmployeeService.get_employee_profile()
        leave_data = LeaveService.get_employee_leaves(profile_data['employee'].name)
        my_employees_leaves = LeaveService.get_my_employees_leaves()
        context.employee = profile_data['employee']
        context.my_employees_leaves = my_employees_leaves
        context.mentum_hours = profile_data['mentum_hours']
        context.leaves = leave_data
        context.no_cache = 1
        context.show_sidebar = True
        
        context.title = _("Mis Permisos/Ausencias")
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
        
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading leave application page")
        frappe.throw(_("Error al cargar la página de permisos/ausencias"))