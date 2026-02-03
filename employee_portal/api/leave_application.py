import frappe
from frappe import _
from employee_portal.services.employee_service import EmployeeService
from employee_portal.services.leave_service import LeaveService
from employee_portal.utils.permissions import require_employee


@frappe.whitelist()
@require_employee
def approve_leave_application(leave_application_name, approver_user, **kwargs):
    try:
        return LeaveService.approve_leave_application(leave_application_name, approver_user)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error approving leave application")
        frappe.throw(_("Error al aprobar la solicitud de permiso/ausencia: {0}").format(str(e)))

@frappe.whitelist()
@require_employee
def create_leave_application(data, mentum_hours, **kwargs):
    try:
        return LeaveService.create_leave_application(data, mentum_hours)
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating leave application")
        frappe.throw(_("Error al crear la solicitud de permiso/ausencia: {0}").format(str(e)))

@frappe.whitelist()
@require_employee
def create_vacation_leave_application(data, **kwargs):
    try:
        return LeaveService.create_vacation_leave_application(data)
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating vacation leave application")
        frappe.throw(_("Error al crear la solicitud de vacaciones: {0}").format(str(e)))