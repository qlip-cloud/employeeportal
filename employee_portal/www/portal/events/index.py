import frappe
import json
from frappe import _
from employee_portal.utils.permissions import require_employee, get_employee_or_throw
from employee_portal.services.employee_service import EmployeeService
from employee_portal.utils.lookups import get_events


def get_context(context):

    require_employee(lambda: None)()
    
    try:
  
        profile_data = EmployeeService.get_employee_profile()
        
        context.employee = profile_data['employee']
        context.no_cache = 1
        
        context.title = _("Mis Eventos")
        context.parents = [
            {"name": _("Portal"), "route": "/portal"}
        ]
        
        events = get_events(context.employee.name)
        # Convertir datetime a string para JSON
        for event in events:
            if 'start' in event and hasattr(event['start'], 'isoformat'):
                event['start'] = event['start'].isoformat()
            if 'end' in event and hasattr(event['end'], 'isoformat'):
                event['end'] = event['end'].isoformat()
        
        context.events = json.dumps(events)
    except frappe.PermissionError:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error loading profile page")
        frappe.throw(_("Error al cargar la página de perfil"))


