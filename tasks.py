# -*- coding: utf-8 -*-
import logging
import time
from json.decoder import JSONDecodeError
from smtplib import SMTPDataError, SMTPRecipientsRefused, SMTPServerDisconnected

import requests
from flask_mailman import EmailMessage
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from app import create_app

app = create_app()
app.app_context().push()


logger = logging.getLogger("[QUEUE]")


def background_task(
    channel_url, text, subscribers, subject, mfrom, send_uid, attachments=[]
):
    logger.info(
        f'Start send "{subject}" to {len(subscribers)} recipients through channel "{channel_url}".'
    )
    max_retries = 3  # Numero massimo di tentativi
    for i, mto in enumerate(subscribers):
        attempt = 0  # Contatore dei tentativi
        error_msg = ""
        while attempt < max_retries:
            try:
                attempt += 1
                with app.mail.get_connection() as conn:
                    msg = EmailMessage(
                        from_email=mfrom,
                        to=[mto],
                        body=text,
                        subject=subject,
                        connection=conn,
                    )
                    msg.content_subtype = "html"
                    for attachment in attachments:
                        msg.attach(
                            filename=attachment.get("filename", ""),
                            content=attachment.get("data", ""),
                            mimetype=attachment.get("content_type", ""),
                        )
                    try:
                        msg.send()
                    except SMTPRecipientsRefused:
                        logger.info("[SKIP] - {}: invalid address.".format(mto))
                    if (i + 1) % 1000 == 0:
                        logger.info(
                            "- Sending status: {}/{}".format(i + 1, len(subscribers))
                        )
                break
            except (SMTPServerDisconnected, SMTPDataError) as e:
                logger.error(f"Message not sent to {mto} for problems with smtp:")
                logger.exception(e)
                logger.error(
                    f"waiting 5 seconds before retry. Remaining attempts: {max_retries - attempt}\n"
                )
                error_msg = str(e)
                time.sleep(5)
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Message not sent to {mto}:")
                logger.exception(e)
                logger.error(
                    f"waiting 5 seconds before retry. Remaining attempts: {max_retries - attempt}\n"
                )
                time.sleep(5)
        else:
            logger.error("Message not sent: no more attempts. Stop sending messages.")
            logger.error("Following addresses didn't received the message:")
            for mto in subscribers[i:]:
                logger.error(f"- {mto}")
            error_msg = f"{error_msg}. Sent {i} messages. Not sent {len(subscribers) - i}. See logs for more details."
            send_complete(
                channel_url=channel_url,
                send_uid=send_uid,
                error=True,
                error_message=error_msg,
            )
            return
    send_complete(channel_url=channel_url, send_uid=send_uid)
    logger.info("Task complete.")


def send_complete(channel_url, send_uid, error=False, error_message=None):
    if not send_uid:
        return
    url = "{}/@send-complete".format(channel_url)
    data = {"send_uid": send_uid, "error": error, "error_message": error_message}

    max_retries = 3  # Numero massimo di tentativi
    attempt = 0  # Contatore dei tentativi
    while attempt < max_retries:
        attempt += 1
        try:
            res = requests.post(
                url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                json=data,
            )
            res.raise_for_status()
            break
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            logger.exception(e)
            logger.error(
                f"Waiting 10 seconds before retry. Remaining attempts: {max_retries - attempt}\n"
            )
            time.sleep(5)
    else:
        logger.error(
            'Unable to update status to remote: received "{code}" instead a "204".'.format(  # noqa
                code=res.status_code
            )
        )
        logger.error("Called url: {}.".format(url))
        logger.error("Parameters: {}.".format(data))
        try:
            logger.error("Error: {}.".format(res.json()))
        except JSONDecodeError:
            logger.error("Error: {}.".format(res.text))
    if res.status_code != 204:
        logger.error(
            'Unable to update status to remote: received "{code}" instead a "204".'.format(  # noqa
                code=res.status_code
            )
        )
        logger.error("Called url: {}.".format(url))
        logger.error("Parameters: {}.".format(data))
        try:
            logger.error("Error: {}.".format(res.json()))
        except JSONDecodeError:
            logger.error("Error: {}.".format(res.text))


def custom_failure_handler(job, exc_type, exc_value, traceback):
    """
    Error handler for RQ jobs. It is called by the RQ worker.
    It is used to call send_complete() with the error information.
    Basically when Task exceeded maximum timeout value
    """
    channel_url = job.kwargs.get("channel_url")
    send_uid = job.kwargs.get("send_uid")

    error_message = f"{exc_type.__name__}: {exc_value}"
    send_complete(
        channel_url=channel_url,
        send_uid=send_uid,
        error_message=error_message,
        error=True,
    )
    return True
