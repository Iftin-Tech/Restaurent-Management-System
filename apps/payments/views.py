from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.permissions import requires_permission
from apps.orders.models import Order
from .models import Payment
from .forms import PaymentForm
from django.db import transaction

@requires_permission('confirm_payment')
def unpaid_orders(request):
    """ Cashier sees all unpaid bills to process. """
    orders = Order.objects.filter(status='BILLED').order_by('created_at')
    return render(request, 'payments/unpaid_orders.html', {'orders': orders})

@requires_permission('confirm_payment')
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, status='BILLED')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.order = order
                payment.cashier = request.user
                payment.save()
                
                order.status = 'PAID'
                order.save()
            
            messages.success(request, f"Payment confirmed for {order.receipt_number}")
            return redirect('payments:unpaid_orders')
    else:
        # Pre-fill amount paid
        form = PaymentForm(initial={'amount_paid': order.total_amount})
        
    return render(request, 'payments/confirm_payment.html', {'order': order, 'form': form})

@requires_permission('cancel_order')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, status='BILLED')
    if request.method == 'POST':
        order.status = 'CANCELLED'
        order.save()
        messages.success(request, f"Order {order.receipt_number} has been cancelled.")
        return redirect('payments:unpaid_orders')
