<!-- STEP 1  -->

Build a production-ready multi-tenant SaaS Restaurant Billing and POS System using Django, PostgreSQL, Django ORM, HTML templates, Tailwind CSS, JavaScript, and DataTables.

Architecture:

* Single codebase
* Multi-tenant SaaS
* Each restaurant has its own separate PostgreSQL database
* One central platform database stores restaurant info and database connections
* Each tenant database shares the same schema
* Clean modular Django apps

Important Real-World Workflow (DO NOT CHANGE):
This system must match Somali restaurant operations:

1. Customer arrives and sits.
2. Waiter takes order verbally.
3. Waiter tells kitchen verbally (NO kitchen screen, NO kitchen system).
4. Kitchen prepares food.
5. Waiter serves food.
6. After customer finishes, waiter goes to cashier area (ONLY place with computer).
7. Waiter enters the order into the system at that time.
8. Waiter prints receipt and gives it to customer.
9. Customer goes to cashier to pay.
10. Cashier verifies the receipt in the system.
11. Cashier confirms payment.
12. Only cashier can confirm payment.

Core Business Rules:

* No kitchen dashboard
* No real-time order tracking
* No tablets for waiters
* System is mainly for billing, payment confirmation, and reporting
* Orders are created AFTER service, not before
* Cashier is the only one allowed to confirm payment

Order Status:

* BILLED (receipt printed, unpaid)
* PAID (cashier confirmed payment)
* CANCELLED

Roles:

* Super Admin (platform owner)
* Restaurant Manager
* Waiter
* Cashier

Permission Rules:

* Users can have multiple roles
* Waiter cannot confirm payment
* Cashier cannot create orders
* Manager has full restaurant access

Modules Required:

* platform (super admin)
* accounts
* restaurants
* dashboard
* menu
* orders
* payments
* reports
* core

Now do NOT generate code yet.

First generate ONLY:

1. Full project architecture
2. Folder structure
3. App structure
4. Database design for:

   * platform database
   * tenant database
5. Tenant database strategy
6. Step-by-step implementation roadmap

Wait for next instruction before coding.


<!-- STEP 2 — PROJECT SCAFFOLD -->

Now generate the Django project scaffold.

Requirements:
- Create modular apps:
  - platform
  - accounts
  - restaurants
  - dashboard
  - menu
  - orders
  - payments
  - reports
  - core

- Split settings into:
  - base.py
  - development.py
  - production.py

- Include:
  - templates/
  - static/
  - media/

- Each app must include:
  - models.py
  - views.py
  - forms.py
  - urls.py
  - admin.py
  - templates/app_name/

Do not implement logic yet.
Only structure.



<!-- STEP 3 — MULTI-TENANT SYSTEM -->
Now implement multi-tenant SaaS architecture.

Requirements:
- Central platform database
- Separate PostgreSQL database per restaurant
- Store db_name, db_host, db_user in platform DB
- Dynamically connect to correct database per request

Generate:
- platform models for restaurants and database config
- tenant resolution logic
- middleware or service for tenant detection
- database routing strategy
- migration strategy for tenant databases

Explain clearly and then generate code.

<!-- STEP 4 — ACCOUNTS + ROLES + PERMISSIONS -->
Now implement authentication and authorization.

Requirements:
- Custom User model
- Roles:
  - Manager
  - Waiter
  - Cashier
- Role + Permission system
- User can have multiple roles

Permissions:
- create_order
- print_receipt
- view_orders
- confirm_payment
- cancel_order
- view_reports
- manage_menu
- manage_users

Rules:
- Waiter → create + print only
- Cashier → confirm payment only
- Manager → full access

Generate:
- models
- forms
- views
- urls
- admin
- permission checks

<!-- STEP 5 — MENU MODULE -->

Now implement menu module.

Features:
- menu categories
- menu items
- price
- active/inactive

Generate:
- models
- forms
- views
- urls
- admin
- templates
- DataTables listing

<!-- STEP 6 — ORDERS MODULE (CRITICAL) -->
Now implement orders module.

Important:
- Order is created AFTER customer eats
- Waiter uses cashier computer

Features:
- create order
- add items
- quantity
- subtotal
- total
- generate receipt number
- print receipt

Order status:
- BILLED
- PAID
- CANCELLED

Rules:
- Waiter creates order
- Waiter prints receipt
- Waiter cannot confirm payment

Generate full module code.

<!-- STEP 7 — PAYMENTS MODULE -->
Now implement payments module.

Workflow:
- Customer brings receipt
- Cashier verifies
- Cashier confirms payment
- Status changes from BILLED → PAID

Features:
- view unpaid orders
- confirm payment
- cancel order
- payment method:
  - cash
  - edahab
  - zaad
  - card

Generate:
- models
- views
- forms
- templates
- permission checks

<!-- STEP 8 — DASHBOARD -->

Now implement dashboards.

Manager:
- today sales
- billed orders
- paid orders
- pending payments
- cancelled orders
- top items

Cashier:
- unpaid orders
- paid orders
- recent payments

Waiter:
- my orders
- receipts created today

Generate:
- views
- templates
- summary queries


<!-- STEP 9 — REPORTS -->
Now implement reports.

Reports:
- daily sales
- paid orders
- unpaid orders
- cancelled orders
- top selling items
- cashier collections
- waiter performance

Use:
- DataTables
- date filters

Generate full module.

<!-- STEP 10 — UI SYSTEM -->

Now generate frontend UI.

Requirements:
- base.html
- sidebar per role
- navbar
- Tailwind design
- DataTables integration
- receipt print layout

Keep clean and modern.

<!-- STEP 11 — FINAL FIX -->
Now review the whole system.

Fix:
- missing imports
- broken urls
- template errors
- permission issues
- tenant bugs

Then provide:
- final structure
- setup guide
- migration steps
- run instructions


