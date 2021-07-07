from io import BytesIO
from celery import shared_task
import weasyprint

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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
                ['ch.ramraj35@gmail.com',],
                html_message=html_message
                )
    return mail_sent

@shared_task
def send_invoice(order_id,message):
    """
    Task to send an e-mail notification when an invoice is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    paid = ((not order.verified) and (not order.payment_by_cash)) or (order.verified and (not order.payment_by_cash)) or order.complete

    # create invoice e-mail
    subject = f'Food Express - EE Invoice no. {order.id}'
    email = EmailMessage(subject, message, 'foodexpressnepal@gmail.com', ['ch.ramraj35@gmail.com',])

    #generate PDF
    html = render_to_string('orders/pdf.html', {'order': order, 'payment_received': paid})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'orders/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    #attach PDF file
    email.attach(f'foodexpress_order{order.id}.pdf', out.getvalue(), 'applications/pdf')

    #send e-mail
    email.send()