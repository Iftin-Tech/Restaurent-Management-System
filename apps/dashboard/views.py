from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.platform_admin.models import Restaurant

@login_required
def index(request):
    user = request.user
    today = now().date()
    
    # 🚨 SUPER ADMIN PLATFORM CHECK
    target_tenant = getattr(request, 'tenant', None)
    if not target_tenant and user.is_superuser:
        context = {
            'total_restaurants': Restaurant.objects.using('default').count(),
            'active_restaurants': Restaurant.objects.using('default').filter(is_active=True).count(),
            'inactive_restaurants': Restaurant.objects.using('default').filter(is_active=False).count(),
            'recent_restaurants': Restaurant.objects.using('default').order_by('-created_at')[:5],
        }
        return render(request, 'platform_admin/dashboard.html', context)
        
    roles = user.roles.values_list('role__name', flat=True)
    context = {'roles': roles}
    
    if 'manager' in roles or user.is_superuser:
        today_orders = Order.objects.filter(created_at__date=today)
        context['today_sales'] = today_orders.filter(status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0.00
        context['pending_payments'] = today_orders.filter(status='BILLED').aggregate(total=Sum('total_amount'))['total'] or 0.00
        context['billed_count'] = today_orders.filter(status='BILLED').count()
        context['paid_count'] = today_orders.filter(status='PAID').count()
        context['cancelled_count'] = today_orders.filter(status='CANCELLED').count()
        context['recent_orders'] = Order.objects.all().order_by('-created_at')[:5]
        
    elif 'cashier' in roles:
        context['unpaid_count'] = Order.objects.filter(status='BILLED').count()
        today_payments = Payment.objects.filter(confirmed_at__date=today, cashier=user)
        context['my_collected_today'] = today_payments.aggregate(total=Sum('amount_paid'))['total'] or 0.00
        context['recent_payments'] = Payment.objects.order_by('-confirmed_at')[:5]
        
    elif 'waiter' in roles:
        my_today_orders = Order.objects.filter(waiter=user, created_at__date=today)
        context['my_receipts_today'] = my_today_orders.count()
        context['my_sales_generated'] = my_today_orders.aggregate(total=Sum('total_amount'))['total'] or 0.00
        context['my_recent_orders'] = Order.objects.filter(waiter=user).order_by('-created_at')[:5]

    return render(request, 'dashboard/index.html', context)
