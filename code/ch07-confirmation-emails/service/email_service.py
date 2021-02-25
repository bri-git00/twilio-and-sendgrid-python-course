from typing import Optional

import python_http_client
import sendgrid

from db.order import Order
from infrastructure import app_secrets


def send_cake_order_receipt(order: Order):
    client = sendgrid.SendGridAPIClient(app_secrets.sendgrid_api_key)

    from_email = sendgrid.From('michael@talkpython.fm', "Michael Kennedy")
    to_email = sendgrid.To(order.user.email, order.user.name)
    subject = sendgrid.Subject("Your order receipt from Cloud City Cakes")
    html = "<h1>Your Receipt</h1>\n<br>\n<br>Thanks for ordering your " \
           f"{order.size} {order.flavour} cake."
    text = "Your Receipt\n\nThanks for ordering your " \
           f"{order.size} {order.flavour} cake."

    message = sendgrid.Mail(from_email, to_email, subject, text, html)

    # TODO: Build PDF invoice
    # TODO: Generate HTML content
    # TODO: Attach the invoice to the email

    # Send the email
    response: python_http_client.client.Response = client.send(message)

    if response.status_code not in {200, 201, 202}:
        raise Exception(f"Error sending email: {response.status_code}")

    print(f"Sent email successfully: Order {order.id} to {order.user.name} at {order.user.email}")
