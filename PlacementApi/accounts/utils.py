from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from PlacementApi import settings

class MailSender():
    def sendMail(self, subject, template, data, to_emails):
        assert isinstance(to_emails,list)
        html_content = render_to_string(template, data)
        email = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, to_emails)
        email.attach_alternative(html_content, "text/html")
        res = email.send()
        return res

    def send_otp(self, data, email):  
        subject = "NITH Placement Portal Verification"
        to = email
        print("Sending OTP")
        template = 'otp.html'
        res = self.sendMail(subject, template, data, [to])
        return res

    def registration_success(self, data, email):  
        subject = "NITH Placement Portal Registration"
        to = email
        template = 'successful.html'
        res = self.sendMail(subject, template, data, [to])
        return res

    def send_password_reset_mail(self, data, email):  
        subject = "Password Reset Request"
        to = email
        template = 'reset_password.html'
        res = self.sendMail(subject, template, data, [to])
        return res