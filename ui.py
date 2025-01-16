import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Function to send email
def send_email(to_email, subject, message, attachments=[], sender_name=''):
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{gmail_user}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))

    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)

# Streamlit UI
st.title("Email Sender App")
st.write("Upload a CSV file with columns: recipient, subject, message, attachments, sender_name (optional)")

# Gmail credentials input
gmail_user = st.text_input("Gmail User")
gmail_password = st.text_input("Gmail Password", type="password")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    if st.button("Send Emails"):
        if gmail_user and gmail_password:
            for index, row in df.iterrows():
                to_email = row['recipient']
                subject = row['subject']
                message = row['message']
                attachments = row['attachments'].split(';') if pd.notna(row['attachments']) else []
                sender_name = row['sender_name'] if 'sender_name' in row else ''
                if row['confirm_send'] == 'yes':
                    send_email(to_email, subject, message, attachments, sender_name)
                    st.write(f"Message sent to {to_email}")
                else:
                    st.write(f'Ignored send {to_email}')
            st.success("All emails sent successfully.")
        else:
            st.error("Please enter your Gmail credentials.")
