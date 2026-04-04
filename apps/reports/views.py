from django.shortcuts import render
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta
import datetime
import json
from apps.accounts.permissions import requires_permission
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment

def get_date_range(request):
    """ Standardized filter for all reports. """
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    
    today = timezone.now().date()
    if start and end:
        try:
            sd = datetime.datetime.strptime(start, '%Y-%m-%d').date()
            ed = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        except:
            ed = today
            sd = ed - timedelta(days=30)
    else:
        ed = today
        sd = ed - timedelta(days=30)
    
    return sd, ed

@requires_permission('view_order')
def sales_report(request):
    sd, ed = get_date_range(request)
    # PAID orders only for Sales report
    sales = Order.objects.filter(status='PAID', created_at__date__gte=sd, created_at__date__lte=ed).order_by('-created_at')
    total = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return render(request, 'reports/sales.html', {
        'reports': sales, 'total': total, 'sd': sd, 'ed': ed, 'title': 'Sales Report'
    })

@requires_permission('view_order')
def cashier_report(request):
    sd, ed = get_date_range(request)
    payments = Payment.objects.filter(confirmed_at__date__gte=sd, confirmed_at__date__lte=ed).order_by('-confirmed_at')
    total = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    return render(request, 'reports/cashier.html', {
        'payments': payments, 'total': total, 'sd': sd, 'ed': ed, 'title': 'Cashier Collections'
    })

@requires_permission('view_order')
def pending_report(request):
    # BILLED orders that are not yet PAID
    pending = Order.objects.filter(status='BILLED').order_by('-created_at')
    total = pending.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return render(request, 'reports/pending.html', {
        'reports': pending, 'total': total, 'title': 'Pending Orders'
    })

@requires_permission('view_order')
def cancelled_report(request):
    sd, ed = get_date_range(request)
    cancelled = Order.objects.filter(status='CANCELLED', created_at__date__gte=sd, created_at__date__lte=ed).order_by('-created_at')
    
    return render(request, 'reports/cancelled.html', {
        'reports': cancelled, 'sd': sd, 'ed': ed, 'title': 'Cancelled Orders'
    })

@requires_permission('view_order')
def top_items_report(request):
    sd, ed = get_date_range(request)
    items = (
        OrderItem.objects.filter(order__status='PAID', order__created_at__date__gte=sd, order__created_at__date__lte=ed)
        .values('menu_item__name')
        .annotate(qty=Sum('quantity'), revenue=Sum(F('quantity') * F('unit_price')))
        .order_by('-revenue')
    )
    
    return render(request, 'reports/top_items.html', {
        'items': items, 'sd': sd, 'ed': ed, 'title': 'Top Selling Items'
    })

@requires_permission('view_order')
def waiter_perf_report(request):
    sd, ed = get_date_range(request)
    waiter_stats = (
        Order.objects.filter(created_at__date__gte=sd, created_at__date__lte=ed)
        .values('waiter__username')
        .annotate(orders=Count('id'), total=Sum('total_amount'))
        .order_by('-total')
    )
    
    return render(request, 'reports/waiter_perf.html', {
        'stats': waiter_stats, 'sd': sd, 'ed': ed, 'title': 'Waiter Performance'
    })
