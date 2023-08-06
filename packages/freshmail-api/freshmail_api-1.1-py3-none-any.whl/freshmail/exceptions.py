class ApiUsageException(Exception):
    pass


class MissingBearerTokenException(ApiUsageException):
    pass


class MessageNotSupportedException(ApiUsageException):
    pass


class WrongEmailRecipientTypeException(ApiUsageException):
    pass


class WrongContentTypeException(ApiUsageException):
    pass


class MissingContentKeys(ApiUsageException):
    pass


class WrongHeaderTypeException(ApiUsageException):
    pass


class WrongFromTypeException(ApiUsageException):
    pass


class WrongAttachmentTypeException(ApiUsageException):
    pass


class MissingRecipientEmailException(ApiUsageException):
    pass


class MissingContentAttribute(ApiUsageException):
    pass


class MultipleContentAttribute(ApiUsageException):
    pass


class RequestException(Exception):
    pass


class ServerException(Exception):
    pass


class ClientException(Exception):
    pass
