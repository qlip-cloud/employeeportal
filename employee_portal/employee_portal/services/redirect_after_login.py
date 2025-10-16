import frappe

def handler(user=None):
    frappe.clear_cache()
    frappe.website.render.clear_cache()

    if frappe.session.user == "Guest":
        return "/login"

    roles = frappe.get_roles(frappe.session.user)

    if "Employee" in roles:
        return "/portal"


    return "/"
