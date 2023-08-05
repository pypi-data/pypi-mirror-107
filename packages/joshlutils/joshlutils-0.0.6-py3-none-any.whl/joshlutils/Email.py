# Login to email
import keyring

# Send Mail
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fetch Mail
import imap_tools.message
from imap_tools import MailBox, A, AND


class _Constants:
    def __init__(self):
        pass

    username = "raspberryp915@gmail.com"
    password = keyring.get_password("gmail", username)


class _CustomError(Exception):
    pass


class SendMail:
    def __init__(self, recipient: list = None, cc_recipient: list = None,
                 bcc_recipient: list = None, subject: str = "", plain_or_html: str = "plain",
                 message: str = ""):
        """
        Send an email from my gmail account (raspberryp915@gmail.com).
        The message will appear to be from "Josh's Python Email"

        Simple example implementation:
            x = Email.Send(recipient=["joshloecker@gmail.com"], subject="This is a second-file subject", message="This is the body of my message")

        :param recipient: A list of recipients
        :param cc_recipient: A list of CC recipients
        :param bcc_recipient: A list of BCC recipients
        :param subject: The subject of the message
        :param plain_or_html: Plain-text or HTML-text
        :param message: The body of the message
        """
        if not self._IsPlainOrHTMLText(plain_or_html):
            raise _CustomError("The parameter 'plain_or_html' must contain either 'plain' or 'html' as its parameter.")

        port = 465

        self.message = MIMEMultipart()
        self.message["Subject"] = subject
        self.message["From"] = f"Josh's Python Email <{_Constants.username}>"

        if recipient is not None:
            self.message["To"] = ", ".join(recipient)
        if cc_recipient is not None:
            self.message["Cc"] = ", ".join(cc_recipient)
        if bcc_recipient is not None:
            self.message["Bcc"] = ", ".join(bcc_recipient)

        self.message.attach(MIMEText(message, plain_or_html))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(_Constants.username, _Constants.password)
            server.sendmail(_Constants.username, recipient, self.message.as_string())

    @staticmethod
    def _IsPlainOrHTMLText(body: str) -> bool:
        """
        Test if the email type contains "plain" text or "html" text
        :param body: String. Should be 'plain' or 'html'
        :return:
        """
        if body not in ["plain", "html"]:
            return False
        else:
            return True


class FetchMail:
    def __init__(self, folder: str = "Inbox"):
        """
        Fetch mail from the Raspberry Pi gmail inbox
        :param folder: The folder to get mail from, defaults to 'Inbox'
        """
        self.mailbox = MailBox("imap.gmail.com")
        self.mailbox.login(username=_Constants.username, password=_Constants.password, initial_folder=folder)

    def UnreadMail(self) -> list[imap_tools.message.MailMessage]:
        """
        Get all unread mail from the `folder` mailbox
        :return: A list of type imap_tools.message.MailMessage
        """
        return [msg for msg in self.mailbox.fetch(A(seen=False), mark_seen=False)]

    def ReadMail(self) -> list[imap_tools.message.MailMessage]:
        """
        Get all read mail from the `folder` mailbox
        :return: A list of type imap_tools.message.MailMessage
        """
        return [msg for msg in self.mailbox.fetch(A(seen=True), mark_seen=False)]

    def AllMail(self) -> list[imap_tools.message.MailMessage]:
        """
        Get all mail from the Raspberry Pi mailbox.
        Return as a list of imap_tools.message.MailMessage's
        :return:
        """
        return [msg for msg in self.mailbox.fetch(mark_seen=False)]

    def MarkMessageFlags(self, uids: list[int], flag: str, value: bool):
        """
        Set the flags for messages
        The uid's list contains a list of messages to set flags for

        Valid flags can be found at: https://pypi.org/project/imap-tools/#id6

        :param uids: A list of mail uid's
        :param flag: The flag to set
        :param value: Set value as True or False
        :return:
        """
        self.mailbox.flag(uids, flag, value)
