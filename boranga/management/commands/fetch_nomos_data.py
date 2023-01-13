
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import Taxonomy, TaxonVernacular


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch nomos data'

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
        logger.info('username: {} Password: {}'.format(username, passwd))

        try:
            res=requests.post(my_url, data=data1[0])
            if res.status_code==200:
                r=res.json()
                r['access_token']
                token='{} {}'.format(r['token_type'], r['access_token'])
                logger.info('Access token {}'.format(token))
                #token example
                # users_url='https://wagyl.bio.wa.gov.au/api/v1/users?range=%5B0%2C20%5D'
                # token='{} {}'.format(r['token_type'], r['access_token'])
                # user_res=requests.get(users_url, headers={'Authorization': token})
                # if user_res.status_code==200:
                #     users=user_res.json()
                #     #logger.info('Users response {}'.format(users))
                # else:
                #     err_msg = 'Users API failed with status code {}'.format(res.status_code)
                #     logger.error('{}\n{}'.format(err_msg, str(e)))
                #     errors.append(err_msg)

                taxon_url='https://wagyl.bio.wa.gov.au/api/v1/taxon_names?range=%5B0%2C5%5D'
                taxon_res=requests.get(taxon_url, headers={'Authorization': token})
                tres=taxon_res.json()
                logger.info('Taxon data:{} '.format(tres))
                try:
                    for t in tres:
                        obj, created=Taxonomy.objects.update_or_create(taxon_name_id=t['taxon_name_id'], defaults={'scientific_name' : t['scientific_name']})
                        logger.info('Taxon {}'.format(obj.scientific_name))
                        
                        # if created:
                        #     #spc, spc_created= Species.objects.update_or_create(taxonomy_id=obj.id)
                        #     tax_ver, tax_ver_created=TaxonVernacular.objects.update_or_create(taxonomy_id=obj.id, defaults={'taxon_name_id' : obj.taxon_name_id})
                        #     logger.info('TaxonVernacular {}'.format(tax_ver))
                except Exception as e:
                    err_msg = 'Create taxon:'
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




