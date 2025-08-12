import frappe

DOCTYPE = "Endowment"
CHILD_TABLE = "Endowment Item"

def save_endowment(data, items):
    try:
        endowment = frappe.new_doc(DOCTYPE)

        for key, value in data.items():
            if (key != "items"):
                setattr(endowment, key, value)


        for item in items:
            endowment.append("items", {
                "article": item.get("article"),
                "quantity": int(item.get("quantity")),
                "description": item.get("description"),
                "size": item.get("size")
            })
        
        endowment.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Endowment saved successfully"}

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in save_endowment: {str(e)}")
        return {"status": "error", "message": str(e)}

