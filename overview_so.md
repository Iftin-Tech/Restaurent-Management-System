# Guudmarka Mashruuca (Af-Soomaali)

## Hordhac
Mashruucani waa **Restaurant Management System** oo ku dhisan Django, waxaana loo sameeyay qaab **multi-tenant SaaS** ah.  
Taas micnaheedu waa: hal codebase ayaa jira, laakiin makhaayad walba waxay leedahay database u gaar ah.

## Fikradda Ganacsi ee Ugu Muhiimsan
Nidaamkan waxaa si gaar ah loogu waafajiyay habka shaqo ee makhaayadaha Soomaaliyeed:
1. Macaamilku wuu fadhiistaa oo cunteeyaa.
2. Waiter-ka ayaa dalabka af ahaan u qaata.
3. Jikada looma adeegsado screen/system.
4. Marka la dhammeeyo cunnada, waiter-ka wuxuu dalabka ka geliyaa kombiyuutarka cashier-ka.
5. Receipt ayaa la daabacaa.
6. Cashier-ka kaliya ayaa xaqiijin kara lacag bixinta.

## Qaab-dhismeedka Farsamo
- **Platform DB (default):** waxaa lagu kaydiyaa xogta tenant-yada (restaurants) iyo database config-kooda.
- **Tenant DB:** makhaayad walba DB gaar ah ayey leedahay (orders, menu, payments, users, iwm).
- **TenantMiddleware:** wuxuu ka akhriyaa subdomain-ka request-ka, kadibna wuxuu ku xiraa DB-ga tenant-ka saxda ah.
- **Database Router:** `platform_admin` wuxuu ku qasban yahay `default`; apps kale tenant DB ayey raacaan.

## Apps-ka Muhiimka ah
- `platform_admin`: maamulka SaaS (abuurid tenant, activation/deactivation, branding, auto provisioning).
- `accounts`: User custom model, roles (`manager`, `waiter`, `cashier`) iyo role assignment.
- `menu`: categories iyo menu items.
- `orders`: abuurista biilasha, order items, receipt print.
- `payments`: unpaid orders, confirm payment, cancel order.
- `dashboard`: role-based dashboard (manager/cashier/waiter/superadmin).
- `reports`: sales, pending, cancelled, top items, cashier collections, waiter performance.
- `core`: tenant context + DB routing.

## Status-ka Order-ka
- `BILLED` = receipt waa la sameeyay, wali lama bixin.
- `PAID` = cashier ayaa xaqiijiyay lacagta.
- `CANCELLED` = order la joojiyay.

## Waxa Hadda Si Fiican U Shaqeeya
- Tenant creation + DB creation + migration automation.
- POS flow ee waiter-ka.
- Payment confirmation ee cashier-ka.
- Dashboards iyo reports aasaasi ah.
- UI guud oo ku dhisan `base.html` + Tailwind + DataTables.

## Qodobo U Baahan Hagaajin
- Meelo qaar permission names isma waafaqaan (`view_order` vs `view_orders`).
- `production.py` wali waa madhan.
- `asgi.py` iyo `wsgi.py` waxay tixraacayaan `config.settings` guud.
- Credentials qaar waa hardcoded (security risk).
- App-ka `restaurants` inta badan waa scaffold oo wali si buuxda looma isticmaalin.

## Gunaanad
Mashruucu waa mid horumar fiican gaaray oo la jaanqaadaya workflow-ga dhabta ah ee makhaayadaha Soomaaliyeed.  
Waxa ugu muhiimsan ee xiga waa adkeynta security-ga, hagaajinta permission consistency, iyo diyaarinta production settings.

