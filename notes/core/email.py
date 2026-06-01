import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading

def send_verification_email_async(to_email, code):
    """
    Asynchronously send verification code email using SMTP_SSL.
    """
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    sender_email = "2691285194@qq.com"
    sender_password = "pfzhrllczhdbdicg"
    
    subject = "校园闲置时光胶囊 - 登录验证码"
    content = f"""
    <html>
      <body style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #fff9f2; padding: 20px; color: #4a4a4a;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; padding: 30px; border: 1px solid #f2e5d7; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
          <h2 style="color: #ff9f69; text-align: center; margin-bottom: 25px; font-weight: bold;">校园闲置时光胶囊</h2>
          <p style="font-size: 16px; line-height: 1.6;">您好！</p>
          <p style="font-size: 16px; line-height: 1.6;">您正在登录/注册【校园闲置时光胶囊】系统，您的登录验证码为：</p>
          <div style="background: #fff9f2; border: 1px dashed #ff9f69; border-radius: 12px; padding: 15px; font-size: 32px; font-weight: bold; text-align: center; color: #ff9f69; margin: 25px 0; letter-spacing: 5px;">
            {code}
          </div>
          <p style="font-size: 14px; color: #777; line-height: 1.6;">提示：该验证码将在 5 分钟内有效。为了您的账户安全，请勿将验证码泄露给他人。如果您没有请求此验证码，请直接忽略本邮件。</p>
          <hr style="border: 0; border-top: 1px solid #f2e5d7; margin: 25px 0;" />
          <p style="font-size: 12px; color: #bbb; text-align: center;">治愈系轻暖闲置物语平台 · 感谢有你</p>
        </div>
      </body>
    </html>
    """
    
    def send_action():
        try:
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = f"校园闲置时光胶囊 <{sender_email}>"
            msg['To'] = to_email
            
            # Connect to QQ Mail SMTP server using SSL
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())
            server.quit()
            print(f"[Email Service] Code {code} successfully sent to {to_email}")
        except Exception as e:
            print(f"[Email Service] Failed to send email to {to_email}: {e}")

    # Run in background thread to avoid blocking the main Flask thread
    thread = threading.Thread(target=send_action)
    thread.start()
