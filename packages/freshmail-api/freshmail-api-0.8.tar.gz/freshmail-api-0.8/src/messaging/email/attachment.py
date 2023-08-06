import base64
import os


class Base64Attachment:
    def __init__(self,
                 name=None,
                 content=None):
        """
        :param name: Name of attachment file
        :type name: str
        :param content: Base64 encoded content of file
        :type content: bytes or str
        """
        self.name = name
        self.content = content

    @property
    def name(self):
        """
        :return: Name of attachment file
        """
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def content(self):
        """
        :return: Base64 encoded content of file
        """
        return self.__content

    @content.setter
    def content(self, content):
        if isinstance(content, bytes):
            content = content.decode()
        self.__content = content

    def __repr__(self):
        return {
            "name": self.__name,
            "content": self.__content
        }


class LocalFileAttachment:
    def __init__(self,
                 filepath,
                 name=None):
        """
        :param filepath: Path to file
        :param name: Name of file
        """
        head, tail = os.path.split(filepath)
        self.__filepath = filepath
        if not name:
            self.name = tail
        else:
            self.name = name
        self.content = self.__prepare_content()

    @property
    def name(self):
        """
        :return: Name of file
        """
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def content(self):
        """
        :return: Base64 encoded content of file
        :type: str
        """
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    def __repr__(self):
        return {
            "name": self.__name,
            "content": self.__content
        }

    def __prepare_content(self):
        with open(self.__filepath, "rb") as f:
            f_content = f.read()
            return base64.b64encode(f_content).decode()
