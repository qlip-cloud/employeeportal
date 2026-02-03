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
        context.leave = LeaveService.get_leave_details(frappe.local.request.args.get('name'))
        context.has_permission_to_approve = LeaveService.has_permission_to_approve(frappe.session.user, context.leave)
        context.no_cache = 1
        context.show_sidebar = True
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
        
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading leave application page")
        frappe.throw(_("Error al cargar la página de permisos/ausencias"))