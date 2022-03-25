from . import Email_send
from . import html_to_pdf



html_to_pdf = html_to_pdf.html_to_pdf


send_email_to_newly_registered_user = Email_send.send_email_to_newly_registered_user     
send_email_for_password_reset = Email_send.send_email_for_password_reset


token_generator = Email_send.token_generator