import frappe
from frappe import _
from employee_portal.services.employee_service import EmployeeService
from employee_portal.utils.permissions import require_employee


@frappe.whitelist()
@require_employee
def get_profile():
    try:
        return EmployeeService.get_employee_profile()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error getting employee profile")
        frappe.throw(_("Error al obtener el perfil: {0}").format(str(e)))


@frappe.whitelist()
@require_employee
def update_profile(**kwargs):
    try:
        data = kwargs
        
        return EmployeeService.update_employee_profile(data)
        
    except frappe.ValidationError as e:
        return {
            'success': False,
            'message': str(e)
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error updating employee profile")
        return {
            'success': False,
            'message': _("Error al actualizar el perfil")
        }