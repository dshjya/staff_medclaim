# Staff MedClaim

Medical insurance claim management for employees and their dependents, built on Frappe / ERPNext.

**This branch (`version-16`) targets Frappe and ERPNext v16.**
For Frappe v14/v15, use the `version-14` branch.

## Features

- Insurance members, dependents, schemes, periods and covers/benefits setup
- Employee details with HR verification and approval
- Insurance claims (OPD and Surgical/Hospital) with bill details and attachments
- Balance tracking per cover (limit, pending, approved, balance) with limit warnings
- Claim approval by officer and manager, with automatic Purchase Order creation
- Monthly claim groups, claim summaries and month-end Journal Entry
- Script reports: Insurance Summary Check, Scheme Details, Monthly Group Reports, Purchase Order, Summary and Details reports
- Print formats for Doctor Recommendation, Indoor and OPD claim forms
- A "Staff MedClaim" workspace and apps-screen icon (Frappe v16 desk)
- Roles: Insurance Member, Insurance User, Insurance Manager

## Requirements

- Frappe v16 and ERPNext v16
- Python 3.14+ and Node.js 24+ (Frappe v16 requirements)
- Server Scripts enabled

## Installation

```bash
cd ~/frappe-bench
bench get-app https://github.com/<your-username>/staff_medclaim --branch version-16
bench --site <your-site> install-app staff_medclaim
bench --site <your-site> migrate
```

For a private repository, `bench get-app` asks for your GitHub username and a Personal Access Token.

## Setup after install

1. **Enable Server Scripts** (disabled by default since v15):
   ```bash
   bench set-config -g server_script_enabled true
   bench restart
   ```
   Site/common config is cached for up to one minute in v16, so allow a moment before testing.
2. **Company:** the scheduled scripts use a Company named `Common Projects`. Create it, or edit the Server Scripts to use your company name.
3. **Company custom fields:** fill in these fields on the Company record:
   - Journal Entry Debit Account
   - Insurance Expense Account
   - Insurance Payable Account
4. **Desk icon:** if the app does not appear on the Desktop after install, run
   ```bash
   bench --site <your-site> migrate
   bench create-desktop-icons-and-sidebar
   ```
   then refresh the browser.
5. **PDF merge library:** the claim attachment dialog loads `pdf-lib.min.js` from `/assets/staff_medclaim/js/`. It is included in `staff_medclaim/public/js/`. Run `bench build --app staff_medclaim` after install.
6. **Roles:** assign Insurance Member, Insurance User and Insurance Manager to your users.
7. Create the master data in this order: Insurance Form, Covers and Benefits, Support Scheme, Insurance Scheme, Insurance Period, Insurance Member.

## What is included in the app

| Item | Where |
|---|---|
| DocTypes | `staff_medclaim/staff_medclaim/doctype/` |
| Workspace | `staff_medclaim/staff_medclaim/workspace/` |
| Roles, permissions, custom fields, list view settings | `staff_medclaim/fixtures/` |
| Client Scripts, Server Scripts, Reports, Print Formats | `staff_medclaim/fixtures/` |

## Exporting changes

After changing roles, permissions, scripts, reports or custom fields on your site, export them back into the app:

```bash
bench --site <your-site> export-fixtures --app staff_medclaim
```

Then commit and push.

## Migrating from the v14 version

See [V16_MIGRATION_NOTES.md](V16_MIGRATION_NOTES.md) for what changed and what to test.

## Hardened build

This copy includes security and functional fixes, two active workflows and two notifications. After `bench migrate` run `bench --site <site> clear-cache`. Read **CHANGELOG.md** before deploying; three workflows (Insurance Claim, Claim Approval, Employee Details) are active.

## License

MIT
