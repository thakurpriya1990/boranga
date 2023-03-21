
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import Kingdom, TaxonomyRank


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch Taxon Rank data'

    def handle(self, *args, **options):
        #logger.info('Running command {}')
        
        logger.info('Running command {}'.format(__name__))

        errors = []
        updates = []
        
        my_url='https://wagyl.bio.wa.gov.au/api/token'
        
        username= settings.NOMOS_USERNAME
        passwd= settings.NOMOS_PASSWORD

        data1=[{'grant_type': 'password',
        'scope': 'READER',
        'username': username,
        'password': passwd }]
        # logger.info('username: {} Password: {}'.format(username, passwd))

        try:
            res=requests.post(my_url, data=data1[0])
            if res.status_code==200:
                r=res.json()
                r['access_token']
                token='{} {}'.format(r['token_type'], r['access_token'])
                
                rank_url='https://wagyl.bio.wa.gov.au/api/v1/taxon_ranks'
                rank_res=requests.get(rank_url, headers={'Authorization': token})
                rank_res=rank_res.json()
                #logger.info('Croos Reference data:{} '.format(cres))
                try:
                    for r in rank_res:
                        # kingdom
                        kingdom_id = r['kingdom_id']
                        kingdom_fk = Kingdom.objects.get(kingdom_id = kingdom_id)

                        obj, created=TaxonomyRank.objects.update_or_create(taxon_rank_id=r['taxon_rank_id'],
                                                                        defaults={
                                                                            'kingdom_id': kingdom_id,
                                                                            'kingdom_fk': kingdom_fk,
                                                                            'rank_name': r['rank_name'],
                                                                        })
                        #logger.info('Cross Reference {}'.format(obj.cross_reference_id))
                        updates.append(obj.id)
                        
                        
                except Exception as e:
                    err_msg = 'Create Taxon Rank:'
                    logger.error('{}\n{}'.format(err_msg, str(e)))
                    errors.append(err_msg)

            else:
                err_msg = 'Login failed with status code {}'.format(res.status_code)
                #logger.error('{}\n{}'.format(err_msg, str(e)))
                logger.error('{}'.format(err_msg))
                errors.append(err_msg)
        except Exception as e:
            err_msg = 'Error at the end'
            logger.error('{}\n{}'.format(err_msg, str(e)))
            errors.append(err_msg)


        cmd_name = __name__.split('.')[-1].replace('_', ' ').upper()
        err_str = 'Errors: {}'.format(len(errors)) if len(errors)>0 else 'Errors: 0'
        msg = '{} completed. Errors: {}. IDs updated: {}.'.format(cmd_name, err_str, updates)
        logger.info(msg)
        print(msg) # will redirect to cron_tasks.log file, by the parent script




