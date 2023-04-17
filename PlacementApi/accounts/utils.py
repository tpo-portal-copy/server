from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from PlacementApi import settings
from django.utils import timezone

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
    

class GetSession():
    def __init__(self,date = timezone.now()) -> None:
        self.date = date
    def CurrentSession(self):
        curr_date = self.date
        date = timezone.datetime(curr_date.year, 7, 1, tzinfo=timezone.get_current_timezone())
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        if curr_date <= date:
            session = str(curr_date.year-1) + "-"+str(curr_date.year)[2:]
        else:
            session = str(curr_date.year) + "-"+str(curr_date.year+1)[2:]
        return session

