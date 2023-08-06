import logging
from typing import Optional, List

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)


class SegmentEndpoints(APIOperations):

    def segment_list(self, project_id: str) -> Optional[List[dict]]:
        '''
        This call return segments from project

        :param project_id: ID from projects' list
        :type project_id: str
        :return: segment list
        :rtype: Optional[List[dict]]
        '''
        endpoint = '/api/segment/list'
        args_dict = {
            'project_id': project_id
        }
        return super().make_get_request(endpoint, params=args_dict)
        
    