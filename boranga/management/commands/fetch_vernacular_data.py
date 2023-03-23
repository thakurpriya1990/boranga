
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import Taxonomy, TaxonVernacular


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch Vernacular data'

    def handle(self, *args, **options):
        #logger.info('Running command {}')
        
        logger.info('Running command {}'.format(__name__))

        errors = []
        updates = []
        
        my_url='{}/token'.format(settings.NOMOS_URL)
        
        username= settings.NOMOS_USERNAME
        passwd= settings.NOMOS_PASSWORD

        data1=[{'grant_type': 'password',
        'scope': 'READER',
        'username': username,
        'password': passwd }]
        
        try:
            res=requests.post(my_url, data=data1[0])
            if res.status_code==200:
                r=res.json()
                r['access_token']
                token='{} {}'.format(r['token_type'], r['access_token'])
    
                vern_url='{}/v1/vernaculars'.format(settings.NOMOS_URL)
                vern_res=requests.get(vern_url, headers={'Authorization': token})
                vres=vern_res.json()
                #logger.info('Taxon data:{} '.format(vres))
                try:
                    for t in vres:
                        taxon, taxon_created= Taxonomy.objects.get_or_create(taxon_name_id=t['taxon_name_id'])
                        obj, created=TaxonVernacular.objects.update_or_create(vernacular_id=t['vernacular_id'], defaults={'vernacular_name' : t['vernacular_name'], 'taxonomy': taxon, 'taxon_name_id' : taxon.taxon_name_id })
                        #logger.info('Vernacular {}'.format(obj.vernacular_name))
                        updates.append(obj.id)
                        
                        
                except Exception as e:
                    err_msg = 'Create Vernacular:'
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




