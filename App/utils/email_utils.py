import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_attachment(to_email):
    # Your Gmail address and app-specific password
    from_email = os.getenv("EMAIL")
    app_password = os.getenv("PASSWORD")


    subject = "Exploring Data Science Opportunities – 3+ Years Exp., Currently at LTIMindtree"
    body = "This is a test email sent from Python."

    base_dir = os.getcwd()
    file_path = os.path.join(base_dir,"App", 'assets', 'data', "Akash-Dawari-Resume.pdf")
    attachment_paths = [file_path]

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in attachment_paths:
        try:
            # Open the file in binary mode
            with open(file_path, 'rb') as attachment:
                # Create a MIMEBase object
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            # Encode the file as base64
            encoders.encode_base64(part)

            # Add header for the attachment
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(file_path)}',
            )

            # Attach the file to the email
            msg.attach(part)
        except Exception as e:
            print(f"Could not attach file {file_path}: {e}")

    try:
        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security

        # Login to the server using your app-specific password
        server.login(from_email, app_password)

        # Convert the MIMEMultipart object to a string and send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Usage
# Usage
# send_email_with_attachment("akashsaha308@gmail.com", 
#                            "Exploring Data Science Opportunities – 3+ Years Exp., Currently at LTIMindtree", 
#                            "This is a test email sent from Python.",
#     ["app.py"]  # List of file paths
# )
