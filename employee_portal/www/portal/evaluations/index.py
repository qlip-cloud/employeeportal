import frappe
import json
from frappe import _
from employee_portal.utils.permissions import require_employee, get_employee_or_throw
from employee_portal.services.employee_service import EmployeeService
from employee_portal.services.evaluation_service import EvaluationService
from employee_portal.utils.lookups import get_documents


def get_context(context):

    require_employee(lambda: None)()
    
    try:
  
        profile_data = EmployeeService.get_employee_profile()
        
        context.employee = profile_data['employee']
        context.no_cache = 1
        context.active_evaluations = EvaluationService.get_active_evaluations_for_employee(context.employee.name)
        context.completed_evaluations = EvaluationService.get_completed_evaluations_for_employee(context.employee.name)
        context.active_evaluations_for_supervisor = EvaluationService.get_active_evaluations_for_supervisor(context.employee.name)
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading support papagege")
        frappe.throw(_("Error al cargar la página de soporte"))


