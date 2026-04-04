# 🍽️ Restaurant Management System — Architecture Document

---

## 1. Full Project Architecture

```
Type:        Multi-Tenant SaaS
Backend:     Django (Python)
Database:    PostgreSQL (one per tenant + one central)
Frontend:    HTML Templates + Tailwind CSS + JavaScript + DataTables
Auth:        Django Custom Auth + Role-Based Permissions
Hosting:     Single server, single codebase, multiple databases
```

### High-Level Flow

```
Browser Request
     │
     ▼
Django Middleware (Tenant Detection)
     │
     ├── Identifies which restaurant (tenant)
     │
     ▼
Switch Database Connection → Tenant DB
     │
     ▼
Django View (with Role + Permission Check)
     │
     ▼
Template (Tailwind CSS + DataTables)
     │
     ▼
Response to Browser
```

---

## 2. Folder Structure

```
restaurant_saas/                        ← Django project root
│
├── config/                             ← Project config (settings, urls, wsgi)
│   ├── settings/
│   │   ├── base.py                     ← Shared settings
│   │   ├── development.py              ← Dev settings
│   │   └── production.py              ← Prod settings
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                               ← All Django apps
│   ├── platform/                       ← Super Admin: manage restaurants
│   ├── accounts/                       ← Users, roles, permissions
│   ├── restaurants/                    ← Restaurant profile management
│   ├── dashboard/                      ← Role-based dashboards
│   ├── menu/                           ← Categories + menu items
│   ├── orders/                         ← Order creation + receipts
│   ├── payments/                       ← Payment confirmation
│   ├── reports/                        ← Sales + performance reports
│   └── core/                           ← Shared utilities, middleware, base models
│
├── templates/                          ← Global HTML templates
│   ├── base.html
│   ├── platform/
│   ├── accounts/
│   ├── dashboard/
│   ├── menu/
│   ├── orders/
│   ├── payments/
│   └── reports/
│
├── static/                             ← CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                              ← Uploaded files
├── manage.py
└── requirements.txt
```

---

## 3. App Structure (Each App Contains)

```
app_name/
├── models.py       ← Database models
├── views.py        ← Business logic + responses
├── forms.py        ← Django forms
├── urls.py         ← URL routing
├── admin.py        ← Django admin config
├── apps.py         ← App config
└── templates/
    └── app_name/   ← HTML templates for this app
```

---

## 4. Database Design

### 4A. Platform Database (Central)
> Stores restaurant registry and their database connection info

**Table: Restaurant**
| Field         | Type         | Notes                        |
|---------------|--------------|------------------------------|
| id            | AutoField PK |                              |
| name          | CharField    | Restaurant name              |
| subdomain     | CharField    | Unique identifier e.g. "abc" |
| db_name       | CharField    | PostgreSQL database name     |
| db_host       | CharField    | Database host                |
| db_port       | IntegerField | Default: 5432                |
| db_user       | CharField    | DB username                  |
| db_password   | CharField    | DB password (encrypted)      |
| is_active     | BooleanField | Enable/disable tenant        |
| created_at    | DateTimeField|                              |

**Table: SuperAdmin**
| Field     | Type      | Notes               |
|-----------|-----------|---------------------|
| id        | PK        |                     |
| username  | CharField |                     |
| email     | CharField |                     |
| password  | CharField | Hashed              |

---

### 4B. Tenant Database (Per Restaurant)
> Each restaurant has its own PostgreSQL database with this schema

**Table: User**
| Field       | Type         | Notes                     |
|-------------|--------------|---------------------------|
| id          | PK           |                           |
| username    | CharField    |                           |
| email       | CharField    |                           |
| password    | CharField    | Hashed                    |
| is_active   | BooleanField |                           |
| created_at  | DateTimeField|                           |

**Table: Role**
| Field | Type      | Notes                         |
|-------|-----------|-------------------------------|
| id    | PK        |                               |
| name  | CharField | manager / waiter / cashier    |

**Table: UserRole** (Many-to-Many)
| Field   | Type | Notes            |
|---------|------|------------------|
| user_id | FK   | → User           |
| role_id | FK   | → Role           |

**Table: MenuCategory**
| Field     | Type         |
|-----------|--------------|
| id        | PK           |
| name      | CharField    |
| is_active | BooleanField |

**Table: MenuItem**
| Field       | Type          |
|-------------|---------------|
| id          | PK            |
| category_id | FK            |
| name        | CharField     |
| price       | DecimalField  |
| is_active   | BooleanField  |

**Table: Order**
| Field          | Type          | Notes                       |
|----------------|---------------|-----------------------------|
| id             | PK            |                             |
| receipt_number | CharField     | Auto-generated, unique      |
| waiter_id      | FK → User     |                             |
| table_number   | CharField     | Optional                    |
| status         | CharField     | BILLED / PAID / CANCELLED   |
| created_at     | DateTimeField |                             |
| notes          | TextField     | Optional                    |

**Table: OrderItem**
| Field      | Type         |
|------------|--------------|
| id         | PK           |
| order_id   | FK → Order   |
| item_id    | FK → MenuItem|
| quantity   | IntegerField |
| unit_price | DecimalField |
| subtotal   | DecimalField |

**Table: Payment**
| Field          | Type          | Notes                        |
|----------------|---------------|------------------------------|
| id             | PK            |                              |
| order_id       | FK → Order    | One-to-One                   |
| cashier_id     | FK → User     |                              |
| method         | CharField     | cash/edahab/zaad/card        |
| amount_paid    | DecimalField  |                              |
| confirmed_at   | DateTimeField |                              |

---

## 5. Tenant Database Strategy

```
Strategy: Database-per-Tenant (Separate PostgreSQL databases)

How it works:
1. Every restaurant registered on the platform gets its own PostgreSQL database
2. The central (platform) database stores the connection info for each restaurant
3. On each HTTP request:
   a. Middleware reads the request (subdomain or session)
   b. Looks up the restaurant in the platform DB
   c. Dynamically connects to that restaurant's database
   d. All queries in that request run against the tenant DB

Why this approach:
- Full data isolation between restaurants
- Easy to backup/restore per tenant
- Scalable
- No risk of data leaking between tenants

Migration Strategy:
- When a new restaurant is created → a new PostgreSQL DB is created
- A management command runs migrations on the new tenant DB automatically
- Schema is identical across all tenant databases
```

---

## 6. Step-by-Step Implementation Roadmap

| Step | Task                          | Description                                              |
|------|-------------------------------|----------------------------------------------------------|
| 1    | ✅ Architecture & Planning     | This document                                            |
| 2    | Project Scaffold              | Create Django project + all apps + settings split        |
| 3    | Multi-Tenant System           | Central DB, tenant DB routing, middleware                |
| 4    | Accounts + Roles + Permissions| Custom user, roles, permission decorators                |
| 5    | Menu Module                   | Categories, items, pricing, admin UI                     |
| 6    | Orders Module                 | Post-service order entry, receipt generation, print      |
| 7    | Payments Module               | Cashier confirms payment, method selection               |
| 8    | Dashboard                     | Role-based summaries and stats                           |
| 9    | Reports Module                | Sales, performance, date-filtered reports                |
| 10   | UI System                     | base.html, sidebar per role, Tailwind, DataTables        |
| 11   | Final Review & Fix            | Audit, fix bugs, setup guide, run instructions           |
