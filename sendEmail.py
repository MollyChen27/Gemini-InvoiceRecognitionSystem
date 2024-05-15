import smtplib
from email.mime.text import MIMEText

# 超出預算就send Email
def send_email(subject, body, to):
    
    # 你的郵件地址和密碼
    email = "s110917025@stu.ntue.edu.tw"
    password = "A230780443"

    # 連接郵件服務器
    server = smtplib.SMTP("smtp.gmail.com", 25)
    server.starttls()
    server.login(email, password)

    # 創建郵件內容
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to

    # 發送郵件
    server.sendmail(email, to, msg.as_string())

    # 關閉連接
    server.quit()


# check 是否超出預算
import json

def checkbudget(df):
    # 加載 budget.json 文件
    body = ""
    with open('budget.json', 'r') as f:
        budget_data = json.load(f)

        type_amount = df.groupby([df["date"], df["type"]])["total"].sum()
        
        # 遍历每个组合，并打印对应的值
        for keys, total in type_amount.items():
            date, type_value = keys

            if(total  > budget_data[type_value]):
                body += f"{date} {type_value}總開支已超過預算上限,total 為{total}\n"

    if body:
        send_email("年度超額開支", body, "s110917025@stu.ntue.edu.tw")

