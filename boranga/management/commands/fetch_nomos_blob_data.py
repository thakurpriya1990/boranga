
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import requests
from boranga.components.species_and_communities.models import(
    Taxonomy,
    TaxonVernacular,
    TaxonomyRank,
    Kingdom,
    ClassificationSystem,
    InformalGroup,
)


import itertools

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch Taxonomy data'

    def handle(self, *args, **options):
        #logger.info('Running command {}')
        
        logger.info('Running command {}'.format(__name__))

        errors = []
        updates = []
        
        my_url = settings.NOMOS_BLOB_URL
        
        try:
            taxon_res=requests.get(my_url)
            if taxon_res.status_code==200:
                taxon=taxon_res.json()
                try:
                    for t in taxon:
                        kingdom_id = t['kingdom_id'] if 'kingdom_id' in t else None
                        kingdom_fk = None
                        if kingdom_id:
                            try:
                                kingdom_obj, created=Kingdom.objects.update_or_create(kingdom_id=kingdom_id,
                                                                                        defaults={
                                                                                        'kingdom_name' : t['kingdom_name']
                                                                                        })
                                kingdom_fk = kingdom_obj
                            except Exception as e:
                                err_msg = 'Create kingdom:'
                                logger.error('{}\n{}'.format(err_msg, str(e)))
                                errors.append(err_msg)
                        
                        rank_id = t['rank_id'] if 'rank_id' in t else None
                        taxon_rank_fk = None
                        if rank_id and kingdom_id:
                            try:
                                rank_obj, created=TaxonomyRank.objects.update_or_create(taxon_rank_id=rank_id,
                                                                                        defaults={
                                                                                            'kingdom_id': kingdom_id,
                                                                                            'kingdom_fk': kingdom_fk,
                                                                                            'rank_name' : t['rank_name']
                                                                                        })
                                taxon_rank_fk = rank_obj
                            except Exception as e:
                                err_msg = 'Create rank:'
                                logger.error('{}\n{}'.format(err_msg, str(e)))
                                errors.append(err_msg)

                        taxon_obj, created=Taxonomy.objects.update_or_create(taxon_name_id=t["taxon_name_id"], defaults={"scientific_name" : t["canonical_name"],
                                                                                                            "kingdom_id" : t["kingdom_id"],
                                                                                                            "kingdom_fk" : kingdom_fk,
                                                                                                            "kingdom_name" : t["kingdom_name"],
                                                                                                            "name_authority" : t["author"],
                                                                                                            "name_comments" : t["notes"],
                                                                                                            "name_currency" : t["is_current"],
                                                                                                            'taxon_rank_id' : t["rank_id"],
                                                                                                            'taxonomy_rank_fk' : taxon_rank_fk,
                                                                                                            })
                        updates.append(taxon_obj.id)

                        # import ipdb; ipdb.set_trace()
                        # check if the taxon has vernaculars and then create the TaxonVernacular records for taxon which will be the "common names"
                        if taxon_obj:
                            vernaculars = t["vernaculars"] if "vernaculars" in t else ""
                            if vernaculars != None:
                                try:
                                    #A taxon can have more than one vernaculars(common names)
                                    for v in vernaculars:
                                        obj, created=TaxonVernacular.objects.update_or_create(vernacular_id=v["id"],
                                                                                            defaults={
                                                                                                "vernacular_name" : v["name"],
                                                                                                "taxonomy": taxon_obj,
                                                                                                "taxon_name_id" : taxon_obj.taxon_name_id,
                                                                                            })

                                except Exception as e:
                                    err_msg = "Create Taxon Vernacular:"
                                    logger.error('{}\n{}'.format(err_msg, str(e)))
                                    errors.append(err_msg)
                
                except Exception as e:
                    err_msg = 'Create Taxon:'
                    logger.error('{}\n{}'.format(err_msg, str(e)))
                    errors.append(err_msg)

            else:
                err_msg = 'Login failed with status code {}'.format(taxon_res.status_code)
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
