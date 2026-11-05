# Staff MedClaim

Medical insurance claim management for employees and their dependents, built on Frappe / ERPNext.

## Features

- Insurance members, dependents, schemes, periods and covers/benefits setup
- Employee details with HR verification and approval
- Insurance claims (OPD and Surgical/Hospital) with bill details and attachments
- Balance tracking per cover (limit, pending, approved, balance) with limit warnings
- Claim approval by officer and manager, with automatic Purchase Order creation
- Monthly claim groups, claim summaries and month-end Journal Entry
- Script reports: Insurance Summary Check, Scheme Details, Monthly Group Reports, Purchase Order, Summary and Details reports
- Print formats for Doctor Recommendation, Indoor and OPD claim forms
- Roles: Insurance Member, Insurance User, Insurance Manager

## Requirements

- Frappe and ERPNext (same version as the branch you install)
- Server Scripts enabled on the site

## Installation

```bash
cd ~/frappe-bench
bench get-app https://github.com/<your-username>/staff_medclaim --branch <branch>
bench --site <your-site> install-app staff_medclaim
bench --site <your-site> migrate
```

Use the branch that matches your Frappe version (for example `version-14`).

For a private repository, `bench get-app` asks for your GitHub username and a Personal Access Token.

## Setup after install

1. **Enable Server Scripts** (v14):
   ```bash
   bench --site <your-site> set-config server_script_enabled true
   bench restart
   ```
2. **Company:** the scheduled scripts use a Company named `Common Projects`. Create it, or edit the Server Scripts to use your company name.
3. **Company custom fields:** fill in these fields on the Company record:
   - Journal Entry Debit Account
   - Insurance Expense Account
   - Insurance Payable Account
4. **PDF merge library:** the claim attachment dialog loads `pdf-lib.min.js` from `/assets/staff_medclaim/js/`. Make sure the file is in `staff_medclaim/public/js/`, then run `bench build --app staff_medclaim`.
5. **Roles:** assign Insurance Member, Insurance User and Insurance Manager to your users.
6. Create the master data in this order: Insurance Form, Covers and Benefits, Support Scheme, Insurance Scheme, Insurance Period, Insurance Member.

## What is included in the app

| Item | Where |
|---|---|
| DocTypes | `staff_medclaim/staff_medclaim/doctype/` |
| Print formats | `staff_medclaim/staff_medclaim/print_format/` and fixtures |
| Roles, permissions, custom fields, list view settings | `staff_medclaim/fixtures/` |
| Client Scripts, Server Scripts, Reports | `staff_medclaim/fixtures/` |

## Exporting changes

After changing roles, permissions, scripts, reports or custom fields on your site, export them back into the app:

```bash
bench --site <your-site> export-fixtures --app staff_medclaim
```

Then commit and push.

## License

MIT
