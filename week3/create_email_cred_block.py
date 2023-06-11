from prefect_email import EmailServerCredentials, email_send_message
from prefect.blocks.system import Secret


def create_email_creds_block():
    email = Secret.load("my-email")
    pw = Secret.load("my-email-pw")

    email_server_creds_obj = EmailServerCredentials(
        username=email.get(),
        password=pw.get(),
    )

    email_server_creds_obj.save(name="my-email-creds", overwrite=True)


if __name__ == "__main__":
    create_email_creds_block()
