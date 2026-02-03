import frappe

def get_genders():
  genders = frappe.get_all("Gender", fields=["gender"], order_by="name asc", ignore_permissions=True)
  return genders


def get_events(employee_name):
  query= f"""SELECT event_name as title, location, start_time as start, end_time as end, event_status as status, introduction, trainer_name
            FROM `tabTraining Event`
            INNER JOIN `tabTraining Event Employee` ON `tabTraining Event`.name = `tabTraining Event Employee`.parent
            WHERE `tabTraining Event Employee`.employee = '{employee_name}'"""
  events = frappe.db.sql(query, as_dict=1)
  return events

def get_leave_types():
    leave_types = frappe.get_all(
        "Leave Type",
        fields=["name"],
        order_by="name asc",
        ignore_permissions=True
    )
    return leave_types

def get_announcements():
    query = """
    SELECT
      name, title, content, published_on, image
    FROM
      `tabAnnouncement`
    WHERE
      published_on <= CURDATE()
    ORDER BY
      published_on DESC
  """
    return frappe.db.sql(query, as_dict=True)

def get_employees_list():
    employees = frappe.get_all(
        "Employee",
        fields=["name", "employee_name"],
        order_by="employee_name asc",
        ignore_permissions=True
    )
    return employees

def get_employee_benefits():
    benefits = frappe.get_all("Employee Benefit", fields=["title", "description", "attachment", "form"])
    return benefits

def get_documents():
    documents = frappe.get_all("Policy File", fields=["title", "file"])
    return documents