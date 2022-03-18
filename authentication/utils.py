from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from six import text_type



def send_email_to_newly_registered_user(username, user_email, activation_url):
    email_subject = "Activate Your Expense Tracker Account"
    email_body = f"Hi {username}! Please verify your account Click here {activation_url}"
    send_mail(email_subject, email_body, "noreply@semicolon.com", [user_email],)

def send_email_for_password_reset(user_email, password_reset_url):
    email_subject = "Reset password of your account"
    email_body = f"Hi there! To reset your password Click here {password_reset_url}"
    send_mail(email_subject, email_body, "noreply@semicolon.com", [user_email],)



class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active)+text_type(user.pk)+text_type(timestamp)
    
token_generator = AppTokenGenerator()