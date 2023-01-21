import imaplib
import email
from email.header import decode_header
import html2text

class emailFetch:

    # account credentials
    def __init__(self):
        self.username = "cursedskank@gmail.com"
        self.password = ""

    # create an IMAP4 class with SSL security
    def imap(self):
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticating with username and password that has been fetched
        imap.login(self.username, self.password)
        status, messages = imap.select("INBOX")
        # number of top emails to fetch
        n = 2
        # total number of emails
        messages = int(messages[0])
        # list to store emails, to be fed to vectorizer
        listEmail = []
        h = html2text.HTML2Text()
        h.ignore_links = False
        for i in range(messages, messages-n, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("Subject:", subject)
                    print("From:", From)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain":
                                #print text/plain emails and skip attachments
                                listEmail.append(body)
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            listEmail.append(body)
                    print("="*100)
                    print("Body: ", h.handle(body))
        # close the connection and logout
        return listEmail
        imap.close()
        imap.logout()
