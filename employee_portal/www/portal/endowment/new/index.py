import frappe
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.endowment import save_endowment

def get_context(context):
    get_modules(context)
    get_employee_from_user(context)
    context.csrf_token = frappe.sessions.get_csrf_token()
    return context

@frappe.whitelist()
def send_endowment(data):
    try:
        if isinstance(data, str):
            data = frappe.parse_json(data)
        
        required_fields = ["employee", "amount", "department", "period"]
        for field in required_fields:
            if not data.get(field):
                raise Exception(f"{field.replace('_', ' ').title()} is required")

        data["items"]
        response = save_endowment(data, data.get("items", []))

        if response.get("status") == "error":
            frappe.log_error(f"Error saving endowment: {response.get('message')}")
            return {"status": "error", "message": response.get("message")}

        return {"status": "success", "message": "Endowment saved successfully"}

    except Exception as e:
        frappe.log_error(f"Exception in send_endowment: {str(e)}")
        return {"status": "error", "message": str(e)}

'''
@frappe.whitelist()
def upload_invoice():
    file = frappe.request.files['invoice']
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file.filename,
        "is_private": 1,
        "content": file.read()
    })
    file_doc.insert()
    return {"status": "success", "file_url": file_doc.file_url}
'''
