# Login to email
import keyring

# Send Mail
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Fetch Mail
import imap_tools.message
from imap_tools import MailBox, A, AND, H

# Mail Flags
import datetime

class _Constants:
    def __init__(self):
        pass

    username: str = "raspberryp915@gmail.com"
    password: str = keyring.get_password("gmail", username)


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

        port: int = 465

        self.message: MIMEMultipart = MIMEMultipart()
        self.message["Subject"]: str = subject
        self.message["From"]: str = f"Josh's Python Email <{_Constants.username}>"

        if recipient is not None:
            self.message["To"]: str = ", ".join(recipient)
        if cc_recipient is not None:
            self.message["Cc"]: str = ", ".join(cc_recipient)
        if bcc_recipient is not None:
            self.message["Bcc"]: str = ", ".join(bcc_recipient)

        self.message.attach(MIMEText(message, plain_or_html))

        context: ssl.SSLContext = ssl.create_default_context()
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
        self.mailbox: MailBox = MailBox("imap.gmail.com")
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


class MarkMailFlags:
    def __init__(self, folder: str = "Inbox"):
        """
        Mark flags in email as read, unread, etc.
        :param folder: The folder to get mail from, defaults to 'Inbox'
        """
        self.mailbox: MailBox = MailBox("imap.gmail.com")
        self.mailbox.login(username=_Constants.username, password=_Constants.password, initial_folder=folder)

    def MarkRead(self, uids: list[int]) -> None:
        """
        Mark mail as "Read"

        :param uids: A list of mail uid's
        :return: None
        """
        self.mailbox.flag(uids, "seen", True)

    def MarkUnread(self, uids: list[int]) -> None:
        """
        Mark mail as "Unread".

        :param uids: A list of mail uid's
        :return: None
        """
        self.mailbox.flag(uids, "seen", False)

    def MarkOtherFlag(self, uids: list[int], flag, value) -> None:
        """
        Valid flags can be found at: https://pypi.org/project/imap-tools/#id6

        :return: None
        """
        flag_values: dict = {
            "answered": bool,
            "seen": bool,
            "flagged": bool,
            "draft": bool,
            "deleted": bool,
            "keyword": [str, list[str]],
            "no_keyword": [str, list[str]],
            "from_": [str, list[str]],
            "to": [str, list[str]],
            "subject": [str, list[str]],
            "body": [str, list[str]],
            "text": [str, list[str]],
            "bcc": [str, list[str]],
            "cc": [str, list[str]],
            "date": [datetime.date, list[datetime.date]],
            "date_gte": [datetime.date, list[datetime.date]],
            "date_lt": [datetime.date, list[datetime.date]],
            "sent_date": [datetime.date, list[datetime.date]],
            "sent_date_gte": [datetime.date, list[datetime.date]],
            "sent_date_lt": [datetime.date, list[datetime.date]],
            "size_gt": int,
            "size_lt": int,
            "new": True,
            "old": True,
            "recent": True,
            "all": True,
            "header": H,
            "gmail_label": [str, list[str]]
        }

        if flag not in flag_values.keys():
            message: str = f"Invalid flag.\nYou passed in '{flag}'.\nValid flags are: {flag_values.keys()}"
            raise _CustomError(message)
        else:
            if not isinstance(flag_values[flag], value):
                message: str = f"Invalid flag value.\nYou passed in '{value}'\n. Valid values for this flag are: {flag_values[flag]}"
                raise _CustomError(message)

        self.mailbox.flag(uids, flag, value)
