import frappe
from frappe import _
from functools import wraps


def clear_cache():
    frappe.clear_cache()
    frappe.website.render.clear_cache()


def is_guest():
    clear_cache()
    return frappe.session.user == 'Guest'


def is_employee():
    clear_cache()
    return frappe.db.exists("Employee", {"user_id": frappe.session.user})


def get_current_employee():
    if not is_employee():
        return None
    return frappe.get_doc("Employee", {"user_id": frappe.session.user})


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_guest():
            frappe.throw(
                _("Necesita iniciar sesión para acceder a esta página"),
                frappe.PermissionError
            )
        return func(*args, **kwargs)
    return wrapper


def require_employee(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_employee():
            frappe.throw(
                _("Necesita iniciar sesión como empleado para acceder a esta página"),
                frappe.PermissionError
            )
        return func(*args, **kwargs)
    return wrapper


def get_employee_or_throw():
    employee = get_current_employee()
    if not employee:
        frappe.throw(
            _("Necesita iniciar sesión como empleado para acceder a esta página"),
            frappe.PermissionError
        )
    return employee

def redirect_after_login(user=None):
    clear_cache()

    if is_guest():
        return "/login"

    if is_employee():
        return "/portal"
    else:
        return "/tickets"
def has_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_roles = frappe.get_roles(frappe.session.user)
            if not any(role in user_roles for role in roles):
                frappe.throw(
                    _("No tiene permisos para realizar esta acción"),
                    frappe.PermissionError
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

