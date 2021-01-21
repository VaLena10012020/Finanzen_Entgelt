import imaplib
import base64
import os
import email
import email.header
from Utils.MongoLogger import MongoLogger


class connect_to_mail_server:
    def __init__(self,user,password):
            self.user = user
            self.pw = password
    
    def connect_to_server(self):
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmx.net",993)
            self.mail.login(user=self.user,password=self.pw)
            self.mail.select('inbox')
            self.connected = True
        except:
            self.connected = False
    
    def Get_pdfs(self,filepath):
        _, self.data = self.mail.search(None,'ALL')
        self.ids = self.data[0]
        self.hdr_list = list()
        self.pdfs_download_list = list()
        for num in self.ids.split():
            _, self.data_1 = self.mail.fetch(num, '(RFC822)')
            raw_email = self.data_1[0][1]
            raw_email_string = raw_email.decode('iso-8859-1')
            try:
                msg = email.message_from_string(raw_email_string)
            ##### ANPASSEN!! nur für den einen Fehler, log message warnen
            except:
                pass
            self.hdr_list.append(msg['from'])
            
            pdfs_downloaded = 0
            
            if 'valentin' in msg['from'] or 'Valentin' in msg['from']:
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    if fileName[0:7] == "Entgelt" and fileName[-4:] == ".pdf":
                        filePath = os.path.join(filepath, fileName)
                        if not os.path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                            pdfs_downloaded +=1
                            self.pdfs_download_list.append(fileName)
        return  self.pdfs_download_list