
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import InformalGroup, ClassificationSystem, Taxonomy


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch Informal Group data'

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
        #logger.info('username: {} Password: {}'.format(username, passwd))

        try:
            res=requests.post(my_url, data=data1[0])
            if res.status_code==200:
                r=res.json()
                r['access_token']
                token='{} {}'.format(r['token_type'], r['access_token'])
                logger.info('Access token {}'.format(token))
                
                informal_grp_url='https://wagyl.bio.wa.gov.au/api/v1/informal_groups'
                informal_grp_res=requests.get(informal_grp_url, headers={'Authorization': token})
                gres=informal_grp_res.json()
                try:
                    for g in gres:
                        # classification system id
                        classification_system_id = g['classification_system_id']
                        classification_system_fk = ClassificationSystem.objects.get(classification_system_id=classification_system_id)

                        # taxon name id
                        taxon_name_id = g['taxon_name_id']
                        # taxon_name_fk = Taxonomy.objects.get(taxon_name_id=taxon_name_id)
                        
                        obj, created=InformalGroup.objects.update_or_create(informal_group_id=g['informal_group_id'], 
                                                                        defaults={
                                                                            'classification_system_id': classification_system_id,
                                                                            'classification_system_fk': classification_system_fk,
                                                                            'taxon_name_id': taxon_name_id,
                                                                            # 'taxonomy': taxon_name_fk,
                                                                        })
                        
                        updates.append(obj.id)
                        
                except Exception as e:
                    err_msg = 'Create informal group:'
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
        err_str = '<strong style="color: red;">Errors: {}</strong>'.format(len(errors)) if len(errors)>0 else '<strong style="color: green;">Errors: 0</strong>'
        msg = '<p>{} completed. Errors: {}. IDs updated: {}.</p>'.format(cmd_name, err_str, updates)
        logger.info(msg)
        print(msg) # will redirect to cron_tasks.log file, by the parent script




