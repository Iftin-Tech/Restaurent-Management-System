from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils.timezone import now

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.platform_admin.models import Restaurant


def _user_roles(user):
    return set(user.roles.values_list("role__name", flat=True))


def _ensure_role(request, role_name):
    if request.user.is_superuser:
        return
    if role_name not in _user_roles(request.user):
        raise PermissionDenied("You do not have permission to access this dashboard.")


@login_required
def index(request):
    target_tenant = getattr(request, "tenant", None)
    if request.user.is_superuser and not target_tenant:
        context = {
            "total_restaurants": Restaurant.objects.using("default").count(),
            "active_restaurants": Restaurant.objects.using("default").filter(is_active=True).count(),
            "inactive_restaurants": Restaurant.objects.using("default").filter(is_active=False).count(),
            "recent_restaurants": Restaurant.objects.using("default").order_by("-created_at")[:5],
        }
        return render(request, "platform_admin/dashboard.html", context)

    roles = _user_roles(request.user)
    if "manager" in roles or request.user.is_superuser:
        return redirect("dashboard:manager")
    if "cashier" in roles:
        return redirect("dashboard:cashier")
    if "waiter" in roles:
        return redirect("dashboard:waiter")

    raise PermissionDenied("No role is assigned to this account.")


@login_required
def manager_dashboard(request):
    _ensure_role(request, "manager")

    today = now().date()
    today_orders = Order.objects.filter(created_at__date=today)
    context = {
        "today_sales": today_orders.filter(status="PAID").aggregate(total=Sum("total_amount"))["total"] or 0.00,
        "pending_payments": today_orders.filter(status="BILLED").aggregate(total=Sum("total_amount"))["total"] or 0.00,
        "billed_count": today_orders.filter(status="BILLED").count(),
        "paid_count": today_orders.filter(status="PAID").count(),
        "cancelled_count": today_orders.filter(status="CANCELLED").count(),
        "recent_orders": Order.objects.all().order_by("-created_at")[:5],
    }
    return render(request, "dashboard/manager.html", context)


@login_required
def cashier_dashboard(request):
    _ensure_role(request, "cashier")

    today = now().date()
    today_payments = Payment.objects.filter(confirmed_at__date=today, cashier=request.user)
    context = {
        "unpaid_count": Order.objects.filter(status="BILLED").count(),
        "my_collected_today": today_payments.aggregate(total=Sum("amount_paid"))["total"] or 0.00,
        "recent_payments": Payment.objects.order_by("-confirmed_at")[:5],
    }
    return render(request, "dashboard/cashier.html", context)


@login_required
def waiter_dashboard(request):
    _ensure_role(request, "waiter")

    today = now().date()
    my_today_orders = Order.objects.filter(waiter=request.user, created_at__date=today)
    context = {
        "my_receipts_today": my_today_orders.count(),
        "my_sales_generated": my_today_orders.aggregate(total=Sum("total_amount"))["total"] or 0.00,
        "my_recent_orders": Order.objects.filter(waiter=request.user).order_by("-created_at")[:5],
    }
    return render(request, "dashboard/waiter.html", context)
