Python API Client for Freshmail API V3

[Official API V3 Documentation](https://freshmail.pl/dokumentacja-rest-api-v3/docs/messaging/emails/)

This API V3 client covers only sending transactional emails by FreshMail Application. Additional features will be added in future.

# Requirements

* Python 3.5+

# Installation

``` bash
pip install freshmail
```

# Usage

## Send transactional email

```python
from messaging.email.mailbag import MailBag
from sender.sender import FreshmailSender
from transport.api.email import EmailApiTransport

token = "MY_APP_TOKEN"
transport = EmailApiTransport(bearer_token = token)
sender = FreshmailSender(transport=transport)

message = MailBag()

message.from_ = {
    "email": "from@address.com",
    "name": "Office"
}
message.subject = "That's my awesome first mail!"
message.contents = {
    "html": "<html><body><strong>Look!</strong> its working!</body></html>"
}
message.tos = [
    {
        "email": "recipient email address"
    }
]

response = sender.send(message=message)
```

## Handle with response object

```python
if response.is_success():
    response_data = response.get_data()
```

## Handle with raw [Requests Response](https://requests.readthedocs.io/en/latest/api/#requests.Response)

```python
response.get_requests_response();
```

## Send personalized email 

```python
from freshmail_api.messaging.email.mailbag import MailBag
from freshmail_api.sender.sender import FreshmailSender
from freshmail_api.transport.api.email import EmailApiTransport

token = "MY_APP_TOKEN"
transport = EmailApiTransport(bearer_token = token)
sender = FreshmailSender(transport=transport)

message = MailBag()

message.from_ = {
    "email": "from@address.com",
    "name": "Office"
}
message.subject = "Hello $$first_name$$! I've got promotion code for You!"
message.contents = {
    "html": "<html><body>Your code is <strong>$$code$$</strong></body></html>"
}
message.tos = [
    {
        "email": "recipient email address",
        "personalization": {
            "first_name": "Joshua",
            "code": "CODE1234"
        }
    }
]

response = sender.send(message=message)
```

## Send multiply emails 

You can send multiple emails by one request. It's much faster than sending one email by one request.
In one request You can send up to 100 emails.

```python
from freshmail_api.messaging.email.mailbag import MailBag
from freshmail_api.sender.sender import FreshmailSender
from freshmail_api.transport.api.email import EmailApiTransport

token = "MY_APP_TOKEN"
transport = EmailApiTransport(bearer_token = token)
sender = FreshmailSender(transport=transport)

message = MailBag()

message.from_ = {
    "email": "from@address.com",
    "name": "Office"
}
message.subject = "Hello $$first_name$$! I've got promotion code for You!"
message.contents = {
    "html": "<html><body>Your code is <strong>$$code$$</strong></body></html>"
}
message.tos = [
    {
        "email": "recipient email address",
        "personalization": {
            "first_name": "Joshua",
            "code": "10percentDISCOUNT"
        }
    },
    {
        "email": "second recipient email address",
        "personalization": {
            "first_name": "Donald",
            "code": "25percentDISCOUNT"
        }
    },
    {
        "email": "third recipient email address",
        "personalization": {
            "first_name": "Abbie",
            "code": "FREEshippingDISCOUNT"
        }
    }
]

response = sender.send(message=message)
```

## Send email from template

You can use FreshMail Templates mechanism to optimize requests to API. Additionally You can modify content of Your emails in FreshMail, not modifying the code of Your application.
```python
from freshmail_api.messaging.email.mailbag import MailBag
from freshmail_api.sender.sender import FreshmailSender
from freshmail_api.transport.api.email import EmailApiTransport

token = "MY_APP_TOKEN"
transport = EmailApiTransport(bearer_token = token)
sender = FreshmailSender(transport=transport)

message = MailBag()

message.from_ = {
    "email": "from@address.com",
    "name": "Support"
}
message.subject = "Hello, that's my email genereted by template!"
message.template_hash = "TEMPLATE_HASH"
message.tos = [
    {
        "email": "recipient email address"
    }
]

response = sender.send(message=message)
```

## Send email with attachments

You can sent emails with attachments. You can upload up to 10 files. Weight of all attachments in email can't exceed 10Mb.
```python
from freshmail_api.messaging.email.attachment import Base64Attachment, LocalFileAttachment
from freshmail_api.messaging.email.mailbag import MailBag
from freshmail_api.sender.sender import FreshmailSender
from freshmail_api.transport.api.email import EmailApiTransport

from base64 import b64encode

token = "MY_APP_TOKEN"
transport = EmailApiTransport(bearer_token = token)
sender = FreshmailSender(transport=transport)

# attachment from hard drive
local_file_attachment = LocalFileAttachment(
    filepath="/my/local/path/file.extension",
    name="optional file name"
)

# attachment from base64 
base64_attachment = Base64Attachment(
    name="base64text.txt",
    content=b64encode("example content".encode())
)

message = MailBag()

message.from_ = {
    "email": "from@address.com",
    "name": "Support"
}
message.subject = "Hello, thats mail with attachments!!"
message.contents = {
    "html": "<html><body><strong>Attachments</strong> in mail</body></html>"
}
message.tos = [
    {
        "email": "recipient email address"
    }
]

message.attachments = [
    local_file_attachment,
    base64_attachment
]

response = sender.send(message=message)
```

# Error handling
API throws exceptions for errors that occurred during requests and errors occurred before sending requests.

- If request is not sent to server because of wrong API usage, an exception that extends `freshmail.exceptions.ApiUsageException` is thrown. This kind of exception means, for example, wrong parameters pass to some methods or passing both content and template in transactional mail, which means request won't be accepted, so API does not make any request.  
- If request is sent and some network issue occurred (DNS error, connection timeout, firewall blocking requests), a `freshmail.exceptions.RequestException` is thrown.
- If request is sent, a response is received but some server error occurred (500 level http code), a `freshmail.exceptions.ServerException` is thrown.
- If request is sent, a response is received but some client error occurred (400 level http code), a `freshmail.exceptions.ClientException` is thrown.

```python
from freshmail_api.exceptions import ClientException

try:
    response = sender.send(message=message)
except ClientException as e:
    handle_exception(e)
```

Set logger to level DEBUG to log request data and request response.

# Proxy setup
If You need to configure proxy You can use a dictionary and pass it as an argument to Transport object.

```python
from freshmail_api.transport.api.email import EmailApiTransport

token = 'MY_APP_TOKEN'
proxies = {
    "http": "http://10.10.10.10:8000",
    "https": "http://10.10.10.10:8000"
}
transport = EmailApiTransport(bearer_token=token, proxies=proxies)
```  


# Logging and debugging

If You need to log or debug Your requests You can pass logging.Logger object.

## Example logger usage

```python
import logging
from logging.handlers import SysLogHandler
from freshmail_api.transport.api.email import EmailApiTransport

def setup_logger(logger, level=logging.INFO, path="stdout"):
    logger.setLevel(logging.DEBUG)

    if path == 'syslog':
        ch = SysLogHandler(address='/dev/log')
    elif path == 'stdout':
        ch = logging.StreamHandler()
    else:
        ch = logging.StreamHandler()

    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s:%(lineno)d %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

bearer_token = "MY_APP_TOKEN"
logger = logging.getLogger("freshmail_api_client")
setup_logger(logger, level=logging.DEBUG)

transport = EmailApiTransport(bearer_token=bearer_token, logger=logger)
```  
