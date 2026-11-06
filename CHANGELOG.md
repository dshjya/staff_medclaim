# Changelog – hardened build (based on version-16)

Static review and patch only. **Nothing here has been run on a live site; test on staging with the checklist at the end.**

## Security
| ID | Change |
|---|---|
| S1 | `update_assessment` ("Verify Claim Documents"): needs Insurance User/Manager, claim must be submitted and not grouped, only valid values and status changes, only a Manager can set the manager decision, no `db.commit()`. |
| S2 | `update_claim_group_status`, `get_claim_group`, `get_used_claim_groups`: staff roles only. |
| S3 | `get_claim_pending_data`, `get_claim_approved_data`: a non-staff user can only read their own membership. |
| S4 | New Server Script **Validate Insurance Claim** (Before Save): membership must be Active and submitted, an Active/Extended period must exist, non-staff can only claim for their own membership, and non-staff cannot set status/approval fields. **Limit checks are still client-side** (needs a business decision: block or warn). |
| S5 | Insurance Member role lost write/create/amend on *Insurance Member*; new hook `permission_query_conditions` so non-staff only see their own membership. |
| S8 | Purchase Order description no longer takes `claim_note` from the request and is HTML-escaped. |
| Reports | *Insurance Summary Check* used `get_all` + raw SQL (any member saw every member's totals). Now uses permission-aware `get_list` and restricts the SQL to the visible members. |

## Functional
| ID | Change |
|---|---|
| F1 | Cancelling a Claim Approval now cancels the Purchase Invoice, then the PO, returns the claims to "Accepted by Manager" and re-opens the group. |
| F2 | "Auto Update Period Status" fixed (it filtered on a field `status` that does not exist on Insurance Member) and **enabled**. |
| F3 | Pending balance now counts *Partially Checked* and no longer counts the two *Declined* statuses. |
| F5 | Group job now runs 23:40, journal entry 23:55 (days 28–31). Company comes from Global Defaults (falls back to "Common Projects"). `frappe.log_error` arguments corrected; debug logging of amounts removed. |
| Claim Approval | *Check Verification Before Submit* lets a rejected approval submit without both checks. |
| F9 | Notifications: *Insurance Claim Submitted* (to Insurance User) and *Insurance Claim Status Changed* (to the claim owner). Status changes made with `db.set_value` do not fire notifications. |

## Workflows (ACTIVE)
`Claim Approval Workflow` and `Employee Details Workflow` are installed **active**.

- **Claim Approval:** To Confirm → (Officer) Checked by Officer → (Manager) Checked by Manager → Approve / Reject. Revoke goes back one step (Officer from Checked by Officer, Manager from Checked by Manager). Approve/Reject submit the document, so the Purchase Order and Invoice are still created as before. Cancel is a Manager transition.
- **Employee Details:** Draft (Employee) → Pending Verification → Verified (HR User) → Approved (HR Manager, submits) with Return and Revoke. Verify and Approve tick themselves and are read-only on the form.
- The old check boxes are locked on both forms; "Set Change Status" keeps them in step with the state.
- Patch `set_workflow_states` gives existing records a starting state when you run `bench migrate`.
- **Insurance Claim Workflow (ACTIVE)** – see the next section.

Ways to roll back: untick *Is Active* on the workflow. The legacy logic returns automatically.

## Insurance Claim Workflow (ACTIVE)
State field: `claim_status`. Flow:

Draft → **Submit** → Submitted → (Officer) **Partially Check** / **Accept** / **Decline** → Accepted or Declined by Officer → (Manager) **Accept** / **Decline** → Accepted or Declined by Manager → **Send to Doctor** → Sent to Doctor → **Approve** / **Reject** (Manager) → Approved or Rejected.

- **Bill checks:** the officer still sets Accepted/Declined per bill on the claim and presses *Update*, then picks the workflow action. Accept needs every bill assessed and none declined; Decline needs every bill assessed and at least one declined. Partially Check needs at least one assessed bill.
- **Revoke:** officer can revoke Accepted/Declined by Officer back to Submitted (assessments are cleared). Manager can revoke Accepted/Declined by Manager back to Accepted by Officer; Accepted by Manager can only be revoked while the claim is not in a monthly group.
- **Cancel:** Insurance Manager, only before grouping (Insurance User has no cancel permission on this doctype, so it was not given a Cancel action).
- **Self approval:** the officer and manager decision actions disallow the claim's owner, so staff cannot check their own claim. System steps (Submit, Send to Doctor, Approve, Reject) allow it so the monthly print and approval do not fail on such a claim.
- **Server:** new script *Insurance Claim Workflow Sync* (Before Save of a submitted document) sets Officer/Manager decision, accepted amount and clears assessments on revoke, so month-end grouping (which looks for "Accepted by Manager" + officer "Accepted") keeps working.
- **Client:** in the claim form script `set_assesment` no longer changes status, the two decision handlers do nothing, and the two decision fields are always read-only.
- **Disabled:** the API *Verify Claim Documents* (not used by any form) is disabled because it wrote status directly and would bypass the workflow.
- **Depends on:** Claim Approval submit moves claims Sent to Doctor / Accepted by Manager to Approved / Rejected, so the person submitting must hold Insurance Manager.
- **Roll-back:** untick *Is Active* on the workflow.

## Print formats and reports
- Hard-coded "2026" in the Indoor and Doctor Recommendation forms now shows the claim's insurance period year.
- Rows and check boxes no longer split across pages; table headers repeat.
- Report layouts were not redesigned (not rendered here).

## Clean-up
- Custom fields are now limited to Company, Supplier, Purchase Order, Journal Entry and Payment Entry. The ones on Instructor, Course Schedule, Student, Material Request and Loan Disbursement were removed from `fixtures/custom_field.json`. `hooks.py` now also filters Custom Field fixtures by doctype, so removed fields are not exported again.
- Removed the empty `education_details_section` break from Employee Details (unused, no label). On an existing site, delete the three old custom fields with *Customize Form* or the Custom Field list if they are already installed (also Material Request and Loan Disbursement).

## Not changed (needs a decision or a live test)
- Skip period (Spectacles) and max days per event (Non-paying wards) are still not enforced.
- Insurance Form lookups by position (`[0]`/`[1]`) in the claim client script.
- Insurance Member "Update Member Dependent" still resets docstatus directly.
- Server-side balance/limit enforcement (S4 note above).
- No automated tests (all test files are stubs).

## Staging test checklist
1. Member calls `update_assessment` / `update_claim_group_status` → refused.
2. Member opens another member's balance, Insurance Member record, or Summary Check row → refused / not shown.
3. Member creates a claim for someone else's membership → refused.
4. Officer and manager complete the normal claim flow; month-end jobs group it; approval submits and creates PO + PI.
5. Cancel that approval → PI and PO cancelled, claims and group reopened.
6. Let a period pass its end date → status moves via the daily job.
7. Run an OPD claim end to end through the Insurance Claim Workflow (member submits, officer assesses and accepts, manager accepts, month-end group, print, approval) and a surgical claim; try each Revoke and a Cancel.
8. Print all three claim forms and check the year, page breaks and layout.
8. Walk all three workflows on staging, including Revoke, Reject and Cancel, and confirm the Purchase Order and Invoice appear on Approve.
