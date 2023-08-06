import logging

import dmsales

logger = logging.getLogger(__name__)

def person_generator(dmsales_api: dmsales.DMSalesAPI, segment_id: int):
    '''
    Generator which generates all persons from specific segment

    :param dmsales_api: DMSalesAPI client object
    :type dmsales_api: dmsales.DMSalesAPI
    :param segment_id: segment id from persons will be downloaded
    :type segment_id: int
    :yield: yields one person object
    :rtype: None
    '''
    logger.debug(f'Getting persons list from segment {segment_id}')
    page = 1
    while True:
        leads_result = dmsales_api.persons_list(page=page, limit=100, segment_id=segment_id) # 10000 max limit on page
        
        logger.debug(f'Got persons_list result {leads_result}')
        if not leads_result or not isinstance(leads_result, dict):
            if 'maximum limit' in leads_result:
                logger.debug(f'Api returned max limit communicate: {leads_result}')
            return
        else:
            if len(leads_result['data']) == 0:
                logger.debug(f'No more leads from segment {segment_id}')
                return
            else:
                logger.debug(f'Downloaded persons list from segment {segment_id}')
                page += 1
                for lead in leads_result['data']:
                    yield lead