
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import Taxonomy, CrossReference


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch Cross Reference data'

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
                #logger.info('Access token {}'.format(token))
                #token example
                # users_url='https://wagyl.bio.wa.gov.au/api/v1/users?range=%5B0%2C20%5D'
                # token='{} {}'.format(r['token_type'], r['access_token'])
                

                cross_url='https://wagyl.bio.wa.gov.au/api/v1/cross_references'
                cross_res=requests.get(cross_url, headers={'Authorization': token})
                cres=cross_res.json()
                #logger.info('Croos Reference data:{} '.format(cres))
                try:
                    for c in cres:
                        old_name_id = c['old_name_id'] if 'old_name_id' in c else None
                        old_taxon, taxon_created= Taxonomy.objects.get_or_create(taxon_name_id=old_name_id)

                        new_name_id = c['new_name_id'] if 'new_name_id' in c else None
                        new_taxon  = None
                        if new_name_id:
                            new_taxon, taxon_created= Taxonomy.objects.get_or_create(taxon_name_id=new_name_id)

                        obj, created=CrossReference.objects.update_or_create(cross_reference_id=c['cross_reference_id'],
                                                                        defaults={
                                                                            'cross_reference_type' : c['cross_reference_type'],
                                                                            'old_name_id': old_name_id,
                                                                            'new_name_id': new_name_id,
                                                                            'old_taxonomy': old_taxon,
                                                                            'new_taxonomy': new_taxon,
                                                                        })
                        #logger.info('Cross Reference {}'.format(obj.cross_reference_id))
                        updates.append(obj.id)
                        
                        
                except Exception as e:
                    err_msg = 'Create Cross Reference:'
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




