from prefect import flow
from prefect_email import EmailServerCredentials, email_send_message

@flow(retries=2, retry_delay_seconds=3)
def send_email(targeted_email: str):
    email_credentials_block = EmailServerCredentials.load("my-email-creds")

    subject = email_send_message(
        email_server_credentials=email_credentials_block,
        subject="Example Flow Notification",
        msg="This proves email_send_message works!",
        email_to=f"{targeted_email}",
    )
    return subject

if __name__ == "__main__":
    email=""
    send_email(email)