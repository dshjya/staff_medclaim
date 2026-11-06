import frappe

# Roles that may see every Insurance Member record.
FULL_ACCESS_ROLES = {"Insurance User", "Insurance Manager", "System Manager", "HR Manager"}


def insurance_member_query(user=None):
    """Staff see all members; everyone else only the membership of their own Employee record."""
    user = user or frappe.session.user
    if user == "Administrator":
        return ""
    if FULL_ACCESS_ROLES & set(frappe.get_roles(user)):
        return ""
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not employee:
        return "1=0"
    return "`tabInsurance Member`.`employee` = {0}".format(frappe.db.escape(employee))
