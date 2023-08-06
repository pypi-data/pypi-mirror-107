import os
import sys
from logging import warn

from dotenv import load_dotenv
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

load_dotenv()

API_ID = 5690708
API_HASH = 'ee6da7fc5772ca692faa783a1c600791'

def login():

    print(
      "\n Hi this is the registration process of "
    )

    print(
        "\nYou are now going to login, and the auth string will be sent securely to your telegram account. \nYou need to copy that for registration on the Redirector Bot.\n\n"
    )
    print(
        "The auth string will be saved in you Telgram's Saved Messages.\n"
    )
    print(
        "Make sure to provide your phone number for registration and not a bot token for registration"
    )

    input("\nPress [ENTER] to proceed ...\n")

    with TelegramClient(StringSession(), API_ID, API_HASH).start() as client:
        session_string = client.session.save()
        message = f"Your session string is: \n\n`{session_string}`\n\nKeep this secret!"

        me = client.get_me()
        print(f"\n\n{me.username}\n\n")
        if me.bot:
            print(
                "This is a bot account, please provide\
                  valid mobile number to register with Redirector Bot"
            )
            sys.exit(1)
        else:
            client.send_message("me", message)
            print("Open your saved messages in telegram to see your session string!")

        Info = """
        \n\n
        - Open Your Saved Messages.

        - Copy the String & Send it to the Redirector Bot to enable your registration.

        - Make sure that this is your auth ket and should not be shared expect with the Redirector Bot.

        """

        print(Info)

    return session_string

login()