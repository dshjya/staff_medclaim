# Frappe v16 migration notes

Changes made when moving `staff_medclaim` from the v14 branch to v16.
Sources: Frappe "Migrating to version 16" wiki and the v16 apps-screen docs.

## Packaging
- `pyproject.toml`: `requires-python >=3.14`, frappe/erpnext dependency range 16.x.
- `hooks.py`: added `add_to_apps_screen` (Desktop icon). Added `public/images/logo.svg`.
- Added a standard **Staff MedClaim workspace** (19 shortcuts: claims, members, setup, reports). The v16 sidebar is generated from it.

## DocTypes
- All 23 DocTypes: `sort_field` changed from `modified` to `creation` (v16 default; avoids keeping both indexes).
- Test stubs moved from `FrappeTestCase` to `IntegrationTestCase`.

## Behaviour changes in v16 that were handled
| v16 change | Where it mattered | Fix |
|---|---|---|
| `get_all/get_list/get_value` now sort by `creation`, not `modified` | First-match lookups in server and client scripts (Active Insurance Period, Insurance Member, File, Fetch Purpose, **Insurance Form [0]/[1] = OPD/IPD**, Covers and Benefits, Employee Details) | Added explicit `order_by: modified desc` so results match v14 |
| SQL function strings in `fields` (`"sum(x) as total"`) | Server Script "Create Month End Journal Entry - Medical Scheme" | Replaced with a plain Python sum over `approved_amount` |
| Report JS is evaluated in an IIFE (no global leaks) | Claim Summary form calls `open_print_window_all` / `print_summary_report` defined inside report JS | Report JS now exposes `window.open_print_window_all`, `window.print_summary_report_insurance_summary`, `window.print_summary_report_insurance_approved_summary`; Claim Summary script calls those |
| `frappe.get_doc(doctype, {filters})` ordering | Server Script "Monthly Claim Group - Once" | Looks up the name with an explicit order, then `get_doc` |
| Server Scripts disabled by default (v15+) | All scripts | README: `bench set-config -g server_script_enabled true` |

## Other cleanup
- Removed a stray standard print format folder: all three print formats are carried by `fixtures/print_format.json`.

## Known fragile spots (not changed)
- **Insurance Form order:** the claim scripts assume the first Insurance Form record is OPD and the second is IPD (`r.message[0]` / `[1]`). This now depends on `modified desc`; editing an Insurance Form record can swap them. Consider adding a field (for example `form_code`) and looking records up by it.
- The Company name `Common Projects` is hard-coded in two Server Scripts.
- `frappe.flags.in_test` is used in "Set Change Status" (deprecated, still works).
- Print formats: v16 can use a Chrome-based PDF engine, so check layout of all three claim forms.

## Test checklist
1. Install on a fresh v16 site; run `bench migrate`.
2. Open the Staff MedClaim workspace; check every shortcut.
3. Create an Insurance Claim (OPD and Surgical); check the balance table and purpose dropdown.
4. Submit and approve a claim; check the Purchase Order / Purchase Invoice creation.
5. Open Claim Summary and use the three report buttons (group, summary, approved summary) to print.
6. Run each report and each print format.
7. Check the month-end Journal Entry scheduler script (run it once manually).
