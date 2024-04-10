import smtplib
from openai import OpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Project_Aria import settings

# ------------------------------------------Emails file is opened here ------------------------------------

# open the latest_emails file read it into the email_body var
with open("latest_emails.txt", "r") as file:
    email_body = file.read()


# -------------------------------------------AI call is made here------------------------------------------

openai_api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)
try:
    # Example conversation with the chat model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Your name is Aria you are a helpful assistant/Planner for ADHD and neorudivergent people, you extract the important dates from the text and output an adhd friendly schedule in an eamil format, you can use emojis to make it fun and engaging.",
            },
            {"role": "user", "content": email_body},
        ],
    )

    # Accessing the first choice's message content directly
    assistant_response = response.choices[0].message.content
except Exception as e:
    print("Failed to query OpenAI API:", str(e))


# --------------------------------------------email is send in this aria-----------------------------------

# login credentials for aria main email
email_address = "aria1995parisa@gmail.com"
email_password = "gfwy rbsc pxgb pqsh"  # Use app password for 2FA accounts
# Recipeient email address and other stuff
recipient_email = "Rafi.zabi456@gmail.com"
subject = "Test Email from Aria Server"
body = assistant_response

# Create a MIME message
msg = MIMEMultipart()
msg["From"] = email_address
msg["To"] = recipient_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain", "utf-8"))  # Specify the UTF-8 encoding for the body

# SMTP server setup
smtp_server = "smtp.gmail.com"
port = 587  # For starttls

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Secure the connection
    server.login(email_address, email_password)
    server.send_message(msg)  # Send the MIME message
    print("Email sent successfully!")
    print("AI Respone:" + assistant_response)
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()
