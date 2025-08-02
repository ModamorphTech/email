from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://modamorph-tech-website.vercel.app/",
    "https://modamorph-tech-website.vercel.app",
    "modamorph-tech-website.vercel.app/"
    "modamorph-tech-website.vercel.app"
    "https://modamorph-tech-website-modamorphtechs-projects.vercel.app/"
    "https://modamorph-tech-website-modamorphtechs-projects.vercel.app"# Allow your React app's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

class EmailRequest(BaseModel):
    sender_email: EmailStr
    sender_password: str
    recipient_email: EmailStr
    subject: str
    body: str

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Create the MIME message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email. Error: {e}")

@app.post("/send-email")
def send_email_api(request: EmailRequest):
    result = send_email(
        request.sender_email,
        request.sender_password,
        request.recipient_email,
        request.subject,
        request.body
    )
    return {"message": "✅ Email sent successfully!"}


