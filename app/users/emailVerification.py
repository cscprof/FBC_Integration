from itsdangerous import URLSafeTimedSerializer
from flask import current_app, render_template, url_for
from flask_mail import Mail, Message

mail = Mail()

#Generate Token to Email to Client
def verify_generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirmation")

#Send email verification link
def send_verification_email(email): #Note, should almost always be passed 'current_user'.
    token = verify_generate_confirmation_token(email)
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
def verify_confirm_token(token, expiration=3600):  # 3600s = 1 hour
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=expiration)
        return email
    except:
        return False
    



#Generate Token to Email to Client
def password_reset_generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset")

    #Send password reset link to Client's Email
def send_password_reset_email(email):
    token = password_reset_generate_confirmation_token(email)
    confirm_url = url_for(
        "users.reset_password", token=token, _external=True
    )
    html = render_template("login/emailMessage.html", confirm_url=confirm_url)
    msg = Message(
        "Password Reset Requested",
        sender="noreply@flourishBC.com", #This is overridden by SMTP authentication, the email set in config.py will always appear as the sender.
        recipients=[email],
    )
    msg.html = html
    mail.send(msg)

def password_reset_confirm_token(token, expiration=3600):  # 3600s = 1 hour
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="password-reset", max_age=expiration)
        return email #redirects user to confirm_url set in send_password_reset_email
    except:
        return False
