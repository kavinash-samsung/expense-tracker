from email.message import EmailMessage

def send_email_to_newly_registered_user(user_email):
    email_subject = "Activate Your Account"
    email_body = ""
    email = EmailMessage(
        email_subject,
        email_body,
        "noreply@semicolon.com",
        [user_email],


    )