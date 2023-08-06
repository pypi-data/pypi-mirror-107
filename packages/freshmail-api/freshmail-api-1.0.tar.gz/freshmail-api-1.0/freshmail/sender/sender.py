from exceptions import MessageNotSupportedException


class FreshmailSender:

    def __init__(self, transport):
        """
        :param transport: Transport object which knows how to handle messages and how to send them
        """
        self.transport = transport

    def send(self, message):
        """
        :param message: The main message object which contains all data required to sending
        :return: Response from transport's request executor
        """
        if self.__transport.is_supported(message):
            return self.__transport.send(message)
        else:
            raise MessageNotSupportedException

    @property
    def transport(self):
        """
        :return: Transport object which knows how to handle messages and how to send them
        """
        return self.__transport

    @transport.setter
    def transport(self, value):
        self.__transport = value
