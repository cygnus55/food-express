from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task

from .models import Order, OrderItem


@shared_task
def order_created_successfully(order_id):
    """
        task to send an email-notification when an order is successfully created.
    """

    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    subject = 'Order created successfully.'
    html_message = render_to_string('orders/order_created_mail.html', {'order': order, 'order_items': order_items})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject,
                plain_message,
                'foodexpressnepal@gmail.com',
                [order.customer.user.email,],
                html_message=html_message
                )
    return mail_sent