from flask_mail import Mail, Message

def create_mail(app):
    mail = Mail()
    mail.init_app(app)
    return mail

def send_email(mail, app_config, recipient_email, adult_count, child_count, cost_per_adult, cost_per_child, total_amount,booking_id):
    subject = 'Booking Confirmation'
    sender = app_config['MAIL_USERNAME']  # Use passed configuration for sender
    
    # Create the email body
    body = (
        f'Dear Customer,\n\n'
        f'Congratulations! You have successfully booked tickets for the museum.\n\n'
        f'Booking Details:\n'
        f'Booking ID: {booking_id}\n'
        f'Number of Adult Tickets: {adult_count} at Rs.{cost_per_adult} per ticket\n'
        f'Number of Child Tickets: {child_count} at Rs.{cost_per_child} per ticket\n\n'
        f'The total amount for your booking is: Rs.{total_amount}\n\n'
        f'Thank you for using our service.\n'
        f'Best regards,\n'
        f'Lineless'
    )
    
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=[recipient_email],
        body=body
    )
    
    try:
        mail.send(msg)
        print(f'Email sent to {recipient_email}')
    except Exception as e:
        print(f'Error sending email: {e}')
