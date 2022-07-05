from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from dotenv import dotenv_values
from typing import List
from pydantic import BaseModel, EmailStr
import jwt
from models.user_model import User

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT="2500",
    MAIL_SERVER="localhost",
    # MAIL_TLS="True",
    # MAIL_SSL=True,
    # USE_CREDENTIALS=True
)

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

async def send_mail(email, instance: User):
    token_data = {
        "uuid": instance.uuid
    }

    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm=["HS256"])

    template = f""""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <div style="display:flex; align-items: center; justify-content: center; flex-direction: column">
            <h3>
                Account verification
            </h3>
            <br/>

            <p>
            Thanks for choosing Ultimate School, please click on the button below to verify your account.
            </p>
            
            <a href="http://localhost:5301/verification/?token={token}" style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; color: blue; background-color: "transparent"; border: "1px solid blue">
                Verify your email
            </a>

            <p>
            Please ignore this email if you did not register to Ultimate School.
            </p>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject= "School App Account Verification",
        recipients=email, #List of emails
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)