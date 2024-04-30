import logging

from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from boranga.components.main.decorators import basic_exception_handler

logger = logging.getLogger("boranga")


@basic_exception_handler
def retrieve_email_user(email_user_id):
    try:
        email_user = EmailUser.objects.get(id=email_user_id)
    except EmailUser.DoesNotExist:
        logger.error(f"EmailUser with id {email_user_id} does not exist")
        return None
    return email_user
