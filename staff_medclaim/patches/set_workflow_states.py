import frappe


def execute():
    """Give existing Employee Details a workflow state. Claim Approval already uses claim_status."""
    if frappe.db.has_column("Employee Details", "workflow_state"):
        frappe.db.sql("""
            update `tabEmployee Details` set workflow_state = case
                when docstatus = 2 then 'Cancelled'
                when docstatus = 1 then 'Approved'
                when ifnull(verify, 0) = 1 then 'Verified'
                else 'Draft' end
            where ifnull(workflow_state, '') = ''
        """)
    # Claim Approval: map the legacy "Completed"-style blanks to a valid state
    frappe.db.sql("""
        update `tabClaim Approval` set claim_status = case
            when docstatus = 1 and ifnull(rejected, 0) = 1 then 'Rejected'
            when docstatus = 1 then 'Approved'
            when docstatus = 2 then 'Cancelled'
            else 'To Confirm' end
        where ifnull(claim_status, '') = ''
    """)
