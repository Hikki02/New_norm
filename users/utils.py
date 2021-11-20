
import smtplib


class Util:
    @staticmethod
    def send_email(data):
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login('a.adilet2003@gmail.com', '0897775622zzz')
        server.sendmail('a.adilet2003@gmail.com', [data['to_email']], data['email_body'])
        server.quit()
