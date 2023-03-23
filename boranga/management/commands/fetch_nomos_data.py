
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import Taxonomy, TaxonVernacular, TaxonomyRank, Kingdom, ClassificationSystem, InformalGroup


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
        #logger.info('username: {} Password: {}'.format(username, passwd))

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
                taxon_url='https://wagyl.bio.wa.gov.au/api/v1/taxon_names?range=[0,500]'
                taxon_res=requests.get(taxon_url, headers={'Authorization': token})
                tres=taxon_res.json()
                #logger.info('Taxon data:{} '.format(tres))
                try:
                    for t in tres:
                        author = t['author'] if 'author' in t else ''
                        notes = t['notes'] if 'notes' in t else ''

                        # kingdom
                        kingdom_fk = Kingdom.objects.get(kingdom_id = t['kingdom_id'])

                        # Taxon rank from the hierarchy
                        taxon_rank_id = t['rank_id']
                        taxon_rank_fk = TaxonomyRank.objects.get(taxon_rank_id = taxon_rank_id)

                        # Taxon's family_nid(taxon_name_id) ref from the rank hierarchy
                        family_nid = t['family_nid'] if 'family_nid' in t else None
                        family_fk = None
                        # to check if family exists else retrieve it from other api taxon_names/{taxon_name_id}
                        if family_nid:
                            try:
                                family_fk = Taxonomy.objects.get(taxon_name_id=family_nid)

                            except Taxonomy.DoesNotExist:
                                #  create taxon for the family_nid(taxon_name_id) in the hierarchy
                                family_url='https://wagyl.bio.wa.gov.au/api/v1/taxon_names/{}'.format(family_nid)
                                family_res=requests.get(family_url, headers={'Authorization': token})
                                fres=family_res.json()
                                try:
                                    family_author = fres['author'] if 'author' in fres else ''
                                    family_notes = fres['notes'] if 'notes' in fres else ''

                                    # kingdom
                                    family_kingdom_fk = Kingdom.objects.get(kingdom_id = fres['kingdom_id'])

                                    # Taxon rank from the hierarchy
                                    family_taxon_rank_id = fres['rank_id']
                                    family_taxon_rank_fk = TaxonomyRank.objects.get(taxon_rank_id = family_taxon_rank_id)

                                    family_obj, created=Taxonomy.objects.update_or_create(taxon_name_id=fres['taxon_name_id'], defaults={'scientific_name' : fres['canonical_name'],
                                                                                                        'kingdom_id' : fres['kingdom_id'],
                                                                                                        'kingdom_fk' : family_kingdom_fk,
                                                                                                        'kingdom_name' : fres['kingdom']['kingdom_name'],
                                                                                                        'name_authority' : family_author,
                                                                                                        'name_comments' : family_notes,
                                                                                                        'name_currency' : fres['is_current'],
                                                                                                        'taxon_rank_id' : family_taxon_rank_id,
                                                                                                        'taxonomy_rank_fk' : family_taxon_rank_fk,
                                                                                                        'path' : fres['path'],
                                                                                                        })
                                    family_fk = family_obj
                                except Exception as e:
                                    err_msg = 'Create family taxon:'
                                    logger.error('{}\n{}'.format(err_msg, str(e)))
                                    errors.append(err_msg)
                                
                        
                        obj, created=Taxonomy.objects.update_or_create(taxon_name_id=t['taxon_name_id'], defaults={'scientific_name' : t['canonical_name'],
                                                                                                            'kingdom_id' : t['kingdom_id'],
                                                                                                            'kingdom_fk' : kingdom_fk,
                                                                                                            'kingdom_name' : t['kingdom']['kingdom_name'],
                                                                                                            'name_authority' : author,
                                                                                                            'name_comments' : notes,
                                                                                                            'name_currency' : t['is_current'],
                                                                                                            'taxon_rank_id' : taxon_rank_id,
                                                                                                            'taxonomy_rank_fk' : taxon_rank_fk,
                                                                                                            'family_nid' : family_nid,
                                                                                                            'family_fk' : family_fk,
                                                                                                            'path' : t['path'],
                                                                                                            })
                        #logger.info('Taxon {}'.format(obj.scientific_name))
                        updates.append(obj.id)
                        
                        # check if tha taxon has classification_systems_ids and then create the informal group records for taxon which will be the "phylo group for a taxon"
                        if obj:
                            if t["classification_system_ids"]:
                                informal_grp_url='https://wagyl.bio.wa.gov.au/api/v1/informal_groups?filter={}{}{}'.format('{"taxon_name_id":',obj.taxon_name_id,'}')
                                informal_grp_res=requests.get(informal_grp_url, headers={'Authorization': token})
                                gres=informal_grp_res.json()
                                try:
                                    for g in gres:
                                        # classification system id
                                        classification_system_id = g['classification_system_id']
                                        classification_system_fk = ClassificationSystem.objects.get(classification_system_id=classification_system_id)

                                        obj, created=InformalGroup.objects.update_or_create(informal_group_id=g['informal_group_id'],
                                                                                        defaults={
                                                                                            'classification_system_id': classification_system_id,
                                                                                            'classification_system_fk': classification_system_fk,
                                                                                            'taxon_name_id': g['taxon_name_id'],
                                                                                            'taxonomy': obj,
                                                                                        })
                                except Exception as e:
                                    err_msg = 'Create informal group:'
                                    logger.error('{}\n{}'.format(err_msg, str(e)))
                                    errors.append(err_msg)

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




