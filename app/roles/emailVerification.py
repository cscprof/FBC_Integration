from itsdangerous import URLSafeTimedSerializer
from flask import current_app, render_template, url_for
from flask_mail import Mail, Message

mail = Mail()

#Generate Token to Email to Client
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirmation")

#Send Token to Client's Email
def send_verification_email(email): #Note, should almost always be passed 'current_user'.
    token = generate_confirmation_token(email)
    confirm_url = url_for(
        "users.confirm_email", token=token, _external=True
    )
    html = render_template("email/emailMessage.html", confirm_url=confirm_url)
    msg = Message(
        "Please verify your email",
        sender="noreply@flourishBC.com", #This is overridden by SMTP authentication, the email set in config.py will always appear as the sender.
        recipients=[email],
    )
    msg.html = html
    mail.send(msg)

#Confirm a Token Recieved from Client
def confirm_token(token, expiration=3600):  # 3600s = 1 hour
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=expiration)
        return email
    except:
        return False
    
