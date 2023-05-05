from django.core.mail import send_mail

def send_signup_email(email):
    subject = 'Welcome to My Site'
    message = 'Thank you for signing up!'
    from_email = 'test.omer100@gmail.com' # Your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)