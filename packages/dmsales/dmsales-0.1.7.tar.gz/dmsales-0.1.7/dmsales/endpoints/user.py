import logging
from typing import Optional

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)

class UserEndpoints(APIOperations):
    
    def me(self) -> Optional[dict]:
        '''
        Returns user information

        :return: json response from api
        :rtype: Optional[dict]
        '''
        return super().make_get_request(endpoint='/api/user/me')

    def my_points(self) -> Optional[dict]:
        '''
        Returns user points

        :return: json response from api
        :rtype: Optional[dict]
        '''
        return super().make_get_request(endpoint='/api/user/wallet/points')
