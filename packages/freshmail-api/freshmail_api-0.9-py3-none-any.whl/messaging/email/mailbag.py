import json
from typing import List

from exceptions import *
from messaging.email.attachment import Base64Attachment, LocalFileAttachment


class MailBag:

    def __init__(self,
                 tos=None,
                 from_=None,
                 subject=None,
                 contents=None,
                 headers=None,
                 attachments=None,
                 template_hash=None):
        """
        The main object that handles all the data needed for a proper sending.
        :param tos: Data of every recipient
        :type tos: List[dict]
        :param from_: Data of the sending account
        :type from_: dict
        :param subject: Subject of email
        :type subject: str
        :param contents: HTML and/or text content of the email
        :type contents: dict
        :param headers: Custom email headers
        :type headers: dict
        :param attachments: Email attachments list
        :type attachments: List[Base64Attachment or LocalFileAttachment]
        :param template_hash: Hash of email template
        :type template_hash: str
        """
        if tos is not None:
            self.tos = tos
        if from_ is not None:
            self.from_ = from_
        if subject is not None:
            self.subject = subject
        if contents is not None:
            self.contents = contents
        if template_hash is not None:
            self.template_hash = template_hash

        self.attachments = attachments
        self.headers = headers

    @property
    def tos(self):
        """
        :rtype: dict
        :return: Data of every recipient
        """
        return self.__tos

    @tos.setter
    def tos(self, recipients):
        if not all(isinstance(recipient, dict) for recipient in recipients):
            raise WrongEmailRecipientTypeException
        if not all("email" in recipient.keys() for recipient in recipients):
            raise MissingRecipientEmailException
        self.__tos = recipients

    @property
    def from_(self):
        """
        :rtype: dict
        :return: Data of the sending account
        """
        return self.__from

    @from_.setter
    def from_(self, from_):
        if not isinstance(from_, dict):
            raise WrongFromTypeException
        self.__from = from_

    @property
    def subject(self):
        """
        :rtype: str
        :return: Subject of email
        """
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject

    @property
    def contents(self):
        """
        :rtype: dict
        :return: HTML and/or text content of the email
        """
        return self.__contents

    @contents.setter
    def contents(self, contents):
        if contents:
            if not isinstance(contents, dict):
                raise WrongContentTypeException
            if "html" not in contents.keys() and "text" not in contents.keys():
                raise MissingContentKeys("Available keys in contents dictionary: [html, text]")
        self.__contents = []
        types = {
            "html": "text/html",
            "text": "text/plain"
        }
        for key in contents.keys():
            self.__contents.append({
                "type": types[key],
                "body": contents[key]
            })

    @property
    def headers(self):
        """
        :rtype: dict
        :return: Custom email headers
        """
        return self.__headers

    @headers.setter
    def headers(self, headers):
        if headers:
            if not isinstance(headers, dict):
                raise WrongHeaderTypeException
        self.__headers = headers

    @property
    def attachments(self):
        """
        :rtype: List[Base64Attachment or LocalFileAttachment]
        :return: Email attachments list
        """
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        if attachments:
            if not all((isinstance(attachment, Base64Attachment) or isinstance(attachment, LocalFileAttachment)) for
                       attachment in attachments):
                raise WrongAttachmentTypeException
        self.__attachments = attachments

    @property
    def template_hash(self):
        """
        :rtype: str
        :return: Hash of email template
        """
        return self.__template_hash

    @template_hash.setter
    def template_hash(self, template_hash: str):
        if template_hash:
            template_hash = template_hash.strip()
        self.__template_hash = template_hash

    def __prepare_data(self):
        data = json.dumps(self.__repr__(), default=lambda o: o.__repr__())
        return data

    def __repr__(self):
        if not hasattr(self, 'tos') or not hasattr(self, 'from_') or not hasattr(self, 'subject'):
            raise MissingContentAttribute(
                "Missing attribute. All of this attributes are required: [recipients, from_, subject]")
        tmp = {
            "recipients": self.__tos,
            "from": self.__from,
            "subject": self.__subject
        }

        if hasattr(self, 'template_hash') and hasattr(self, 'contents'):
            raise MultipleContentAttribute(
                "You can't set both of given attributes simultaneously: [template_hash, contents]")

        if hasattr(self, 'template_hash'):
            tmp['templateHash'] = self.__template_hash
        else:
            if not hasattr(self, 'contents'):
                raise MissingContentAttribute(
                    "Missing attribute. There has to be set one of these: [template_hash, contents]")
            tmp['contents'] = self.__contents

        if self.__headers:
            tmp['headers'] = {}
            for key, value in self.__headers.items():
                tmp['headers'][key] = value

        if self.__attachments:
            tmp['attachments'] = self.__attachments

        return tmp
