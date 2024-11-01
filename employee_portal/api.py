import frappe
from frappe.utils import getdate # type: ignore

@frappe.whitelist()
def get_events():
    events = frappe.get_all('Event',
                            fields=['name', 'subject as title', 'starts_on as start', 'ends_on as end', 'status'])
    return events
