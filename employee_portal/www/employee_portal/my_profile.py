# about.py
import frappe
from employee_portal.utils.utils import get_modules, get_employee # type: ignore
def get_context(context):
    user = frappe.get_doc("User", frappe.session.user)
    genders = frappe.get_all("Gender", fields=["gender"])
    context.genders = genders
    employment_types = frappe.get_all("Employment Type", fields=["employee_type_name"])
    context.employment_types = employment_types
    departments = frappe.get_all("Department", fields=["department_name"])  
    context.departments = departments
    designations = frappe.get_all("Designation", fields=["designation_name"])
    context.designations = designations
    get_modules(context)
    get_employee(context) 
    employee = context.employee
    if frappe.request.method == "POST":
        update_employee_data(employee)
    return context


def update_employee_data(employee):
    # Obtiene los datos del formulario
    first_name = frappe.form_dict.first_name
    middle_name = frappe.form_dict.middle_name
    last_name = frappe.form_dict.last_name
    full_name = frappe.form_dict.full_name
    dob = frappe.form_dict.dob
    gender = frappe.form_dict.gender
    employee_number = frappe.form_dict.employee_number
    emergency_phone = frappe.form_dict.emergency_phone
    emergency_contact = frappe.form_dict.emergency_contact
    company = frappe.form_dict.company
    employment_type = frappe.form_dict.employment_type
    department = frappe.form_dict.department
    designation = frappe.form_dict.designation
    date_of_joining = frappe.form_dict.date_of_joining
    date_of_leaving = frappe.form_dict.date_of_leaving

    # Actualiza el documento del empleado
    employee.first_name = first_name
    employee.middle_name = middle_name
    employee.last_name = last_name
    employee.employee_name = full_name
    employee.date_of_birth = dob
    employee.gender = gender
    employee.employee_number = employee_number
    employee.emergency_phone_number = emergency_phone
    employee.person_to_be_contacted = emergency_contact
    employee.company = company
    employee.employment_type = employment_type
    employee.department = department
    employee.designation = designation
    employee.date_of_joining = date_of_joining
    employee.contract_end_date = date_of_leaving

    # Guarda los cambios
    employee.save()
    frappe.msgprint("Los datos han sido actualizados exitosamente.")