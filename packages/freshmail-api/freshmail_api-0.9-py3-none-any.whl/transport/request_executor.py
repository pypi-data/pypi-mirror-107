import platform

import requests

from exceptions import RequestException, ServerException, ClientException


class RequestExecutor:
    def __init__(self, logger):
        self.__scheme = "https"
        self.__host = "api.freshmail.com"
        self.__version = "v3"
        self.logger = logger

    def set_logger(self, logger):
        self.logger = logger

    def post(self, uri, message, bearer_token=None, proxies=None):
        headers = self.__prepare_headers(bearer_token)
        data = message.__prepare_data()
        url = self.__scheme + "://" + self.__host + "/" + self.__version + "/" + uri
        if self.logger:
            self.logger.debug(
                "Sending requests with given parameters: URL: {}, DATA: {}, HEADERS: {}, PROXIES: {}".format(url, data,
                                                                                                             headers,
                                                                                                             proxies))
        try:
            response = requests.post(url=url, data=data, headers=headers, proxies=proxies)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)

        if self.logger:
            self.logger.debug(
                "Got response: STATUS CODE: {}, JSON: {}, HEADERS: {}".format(response.status_code, response.json(),
                                                                              response.headers))

        if 400 <= response.status_code < 500:
            raise ClientException(response.json())
        if 500 <= response.status_code < 600:
            raise ServerException(response.json())

        return Response(response)

    def __prepare_headers(self, bearer_token):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.__prepare_user_agent()
        }

        if bearer_token:
            headers['Authorization'] = 'Bearer ' + bearer_token
        return headers

    def __prepare_user_agent(self):
        format_str = "freshmail/python-api-client:{python_api_client_version};requests:{requests_version};python:{python_version}"
        versions = {
            "python_api_client_version": "0.1",
            "requests_version": requests.__version__,
            "python_version": platform.python_version()
        }
        return format_str.format(**versions)


class Response:
    def __init__(self, response):
        self.__raw_response = response

    def is_success(self):
        """
        :rtype: bool
        :return: Boolean value if request succeeded
        """
        if self.__raw_response.status_code != 201:
            return False
        return True

    def get_data(self):
        """
        Returns dict from json returned by request
        :return: dict
        """
        return self.__raw_response.json()

    def get_requests_response(self):
        """
        Returns raw Response object from requests library
        :return: requests.Response
        """
        return self.__raw_response
