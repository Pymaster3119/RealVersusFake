import imaplib
import email
from email.header import decode_header
import re

username = "cygnus3119@gmail.com"
mail = imaplib.IMAP4_SSL("imap.gmail.com")
key = open("finishedGame/systeminfo.txt", "r")
mail.login('cygnus3119@gmail.com', key.readline().removesuffix("\n"))
key.close()

mail.select("inbox")
status, messages = mail.search(None, "ALL")
mail_ids = messages[0].split()

realimagesright = 0
realimageswrong = 0
fakeimagesright = 0
fakeimageswrong = 0
pattern = r"Real Images Right:\s*(\d+)\s*Real Images Wrong:\s*(\d+)\s*Fake Images Right:\s*(\d+)\s*Fake Images Wrong:\s*(\d+)"
for emailid in mail_ids:
    status, msg_data = mail.fetch(emailid, "(RFC822)")

    # Parse the email content
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = decode_header(msg["subject"])[0][0]
            email_from = decode_header(msg.get("From"))[0][0]
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    try:
                        body = part.get_payload(decode=True).decode()
                        match = re.search(pattern, body)
                        if match:
                            realimagesright += int(match.group(1))
                            realimageswrong += int(match.group(2))
                            fakeimagesright += int(match.group(3))
                            fakeimageswrong += int(match.group(4))

                            # Print the extracted values
                            
                        else:
                            print("Pattern not found in the email body")
                    except:
                        pass
            else:
                # Extract content type of the email
                content_type = msg.get_content_type()

                body = msg.get_payload(decode=True).decode()
                match = re.search(pattern, body)
                if match:
                    realimagesright = int(match.group(1))
                    realimageswrong = int(match.group(2))
                    fakeimagesright = int(match.group(3))
                    fakeimageswrong = int(match.group(4))

                    # Print the extracted values
                    print(f"Real Images Right: {realimagesright}")
                    print(f"Real Images Wrong: {realimageswrong}")
                    print(f"Fake Images Right: {fakeimagesright}")
                    print(f"Fake Images Wrong: {fakeimageswrong}")
                else:
                    print("Pattern not found in the email body")

print(f"Real Images Right: {realimagesright}")
print(f"Real Images Wrong: {realimageswrong}")
print(f"Fake Images Right: {fakeimagesright}")
print(f"Fake Images Wrong: {fakeimageswrong}")
mail.logout()
