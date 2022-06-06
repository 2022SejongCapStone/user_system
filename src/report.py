import sys, os
import smtplib
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonmodule as jm


class SMTPclient():
    
    def __init__(self):
        self.msg = MIMEMultipart()
        self.msg['From'] = jm.get_secret("MSGFROM")
        self.msg['To'] = jm.get_secret("MSGTO")
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = Header(s='[Warning][Team뭉게구름] 정보 유출 탐지 알람', charset='utf-8')
        
        
    def makeBody(self, content):
        body = MIMEText(content, 'html', _charset='utf-8')
        self.msg.attach(body)
        
    
    def attachFile(self, filelist):
        for f in filelist:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            self.msg.attach(part)
            
            
    def sendMail(self):
        mailServer = smtplib.SMTP_SSL('smtp.gmail.com')
        mailServer.login(jm.get_secret("MSGFROM"), jm.get_secret("TOKEN"))
        mailServer.send_message(self.msg)
        mailServer.quit()


if __name__ == "__main__":
    content = '''
    <h1>파일 유출이 탐지되었습니다!</h1>
    <h2>지금 바로 첨부된 파일을 열어 유출된 파일 정보를 확인하시길 바랍니다!</h2><br><br><br><br>


    저희 서비스를 사용해주셔서 감사합니다!<br>
    저희는 세종대학교 정보보호학과 뭉게구름입니다😊
    '''
    mail = SMTPclient()
    mail.makeBody(content)
    mail.attachFile(["../report/testreport.html"])
    mail.sendMail()