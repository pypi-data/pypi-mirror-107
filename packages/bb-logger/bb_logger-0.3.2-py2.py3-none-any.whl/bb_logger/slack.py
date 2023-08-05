import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from .constant import LOG_LEVEL
from datetime import datetime


def build_message(event) -> dict:
    """build slack message layout blocks and text fallback

    Returns:
        dict: [description]
    """
    # info
    level = event['level']
    message = event['message']
    main_message = message[:100]
    event_time = datetime.now()

    # slack elements
    # fall back text
    if not level:
        level = LOG_LEVEL.unkown.value
    text = ' - '.join(
        [level, event_time.strftime('%H:%M:%S %Y-%m-%d'), main_message])

    # block
    header_image_alt, header_image_url = {
        LOG_LEVEL.info.value: ("info", "https://image.flaticon.com/icons/png/512/3160/3160580.png"),
        LOG_LEVEL.warn.value: ("warn", "https://img.icons8.com/color/344/fa314a/error--v1.png"),
        LOG_LEVEL.warning.value: ("warn", "https://img.icons8.com/color/344/fa314a/error--v1.png"),
        LOG_LEVEL.error.value: ("error", "https://img.icons8.com/fluent/344/fa314a/break.png"),
        LOG_LEVEL.critical.value: ("critical", "https://img.icons8.com/nolan/344/fa314a/skull.png"),
        LOG_LEVEL.unkown.value: ("unkown", "https://img.icons8.com/ios/344/question-shield.png"),
    }.get(level)
    header = {"type": "context",
              "elements": [{"type": "image",
                            "image_url": header_image_url,
                            "alt_text": header_image_alt},
                           ]}
    message = {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": message,
                "emoji": False
            }
        ]
    }
    blocks = [
        header,
        {
            "type": "divider"
        },
        message,
    ]
    color = {
        LOG_LEVEL.info.value: '#43aa8b',
        LOG_LEVEL.warn.value: '#f9c74f',
        LOG_LEVEL.warning.value: '#f9c74f',
        LOG_LEVEL.error.value: '#f3722c',
        LOG_LEVEL.critical.value: '#f94144',
        LOG_LEVEL.unkown.value: '#577590'
    }.get(level, '#f94144')
    attachments = [
        {'color': color,
         'blocks': blocks}
    ]

    return text, attachments


def push_noti(event: dict, slack_info: dict) -> None:
    """receive event from lambda, buils message and send
        """

    client = WebClient(token=slack_info["slack_token"])
    channel_id = slack_info['slack_channel']
    text, attachments = build_message(event)
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=text,
            attachments=attachments
        )
        logging.info(result)

    except SlackApiError as e:
        logging.error(f"Error posting message: {e}")
