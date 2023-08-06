import logging

import requests.exceptions

from . import exceptions

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10
class APIOperations:
    '''
    Handling requests
    '''
    
    def make_get_request(self, endpoint: str, **kwargs):
        '''
        Sends GET request to given endpoint and handle errors

        :param endpoint: only endpoint e.g. /api/persons/list
        :type endpoint: str
        :raises exceptions.DMSalesAPIConnectionError: when there was a problem with api connection (timeouts) 
        :raises Exception: unknown error
        :return: json response from api
        :rtype: dict
        '''
        try:
            logger.debug(f'Trying to make GET request to endpoint {endpoint} with query kwargs {kwargs}')
            if 'timeout' in kwargs:
                response = self.session.get(self.api_host + endpoint, **kwargs)
            else:
                response = self.session.get(self.api_host + endpoint, timeout=DEFAULT_TIMEOUT, **kwargs)
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:
            logger.exception('DMSales API connection timeout')
            raise exceptions.DMSalesAPIConnectionError(DEFAULT_TIMEOUT)
        except Exception as e:
            raise e
        else:
            logger.debug(f'DMSales API returned response {response}')
            return response.json()

    def make_post_request(self, endpoint: str, **kwargs):
        '''
        Sends POST request to given endpoint and handle errors

        :param endpoint: only endpoint e.g. /api/persons/list
        :type endpoint: str
        :raises exceptions.DMSalesAPIConnectionError: when there was a problem with api connection (timeouts) 
        :raises Exception: unknown error
        :return: json response from api
        :rtype: dict
        '''
        try:
            logger.debug(f'Trying to make POST request to endpoint {endpoint} with kwargs {kwargs}')
            if 'timeout' in kwargs:
                response = self.session.post(self.api_host + endpoint, **kwargs)
            else:
                response = self.session.post(self.api_host + endpoint, timeout=DEFAULT_TIMEOUT, **kwargs)
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:
            raise exceptions.DMSalesAPIConnectionError(DEFAULT_TIMEOUT)
        except Exception as e:
            raise e
        else:
            logger.debug(f'DMSales API returned response {response}')
            logger.debug(f'Response message: {response.text}')
            return response.json()

    def make_put_request(self, endpoint: str, **kwargs):
        '''
        Sends PUT request to given endpoint and handle errors

        :param endpoint: only endpoint e.g. /api/persons/list
        :type endpoint: str
        :raises exceptions.DMSalesAPIConnectionError: when there was a problem with api connection (timeouts) 
        :raises Exception: unknown error
        :return: json response from api
        :rtype: dict
        '''
        try:
            logger.debug(f'Trying to make PUT request to endpoint {endpoint} with kwargs {kwargs}')
            if 'timeout' in kwargs:
                response = self.session.put(self.api_host + endpoint, **kwargs)
            else:
                response = self.session.put(self.api_host + endpoint, timeout=DEFAULT_TIMEOUT, **kwargs)
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:
            raise exceptions.DMSalesAPIConnectionError(DEFAULT_TIMEOUT)
        except Exception as e:
            raise e
        else:
            logger.debug(f'DMSales API returned response {response}')
            logger.debug(f'Response message: {response.text}')
            return response.json()
