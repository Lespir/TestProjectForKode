# from mega import Mega
#
# mega = Mega()
# m = mega.login('alecsey.o.nikitin@gmail.com', '62195111aon$')
#
# folder = m.find('KODE')
#
# # file = m.upload('./static/image/back.png', folder[0])
# print(m.export('KODE/back.png'))
accountSID = 'AC28799778e906932bb94ea9939c3e2bb4'
authToken = '3479f2dcade93dab7081be1d6d3af934'
myNumber = '+79062195111'
twilioNumber = '+14159385764'
from twilio.rest import Client


def textmyself(message):
    twilioCli = Client(accountSID, authToken)
    twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)


textmyself('-----------------------------------\n\n\n\n\nПривет')
