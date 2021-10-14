import smtplib, json
import datetime as dt


print(type(dt.datetime.today().hour))


fh = open("../Data/email_data.json", "r")
email_data = json.load(fh)
fh.close()

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()
print(email_data['email'])
server.login(email_data['email'], email_data['password'])

phone_address = f'{email_data["phone"]}@txt.att.net'
print(phone_address)

server.sendmail('1111111111', phone_address, "test")

