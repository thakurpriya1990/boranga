import logging
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields.jsonb import JSONField
from boranga import exceptions
from boranga.components.main.models import (
    CommunicationsLogEntry, 
    UserAction,
    Document,
    RevisionedMixin,
)


from boranga.ledger_api_utils import retrieve_email_user
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup
import json
from django.db import models,transaction
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from boranga.settings import (
    GROUP_NAME_ASSESSOR,
    GROUP_NAME_APPROVER,
    GROUP_NAME_EDITOR,
)
from boranga.components.main.utils import get_department_user
from boranga.components.main.related_item import RelatedItem

logger = logging.getLogger(__name__)

private_storage = FileSystemStorage(location=settings.BASE_DIR+"/private-media/", base_url='/private-media/')

class Meeting(models.Model):
    """
    A change in conservation status for a species is executed during Committee Meetings. 
    It is necessary to capture these changes and the meetings that caused the change. 

    Has a:
    - Contact
    """
    MEETING = 'meeting'
    COMMITTEE_MEETING = 'committee_meeting'

    MEETING_TYPE_CHOICES = (
        (MEETING, 'meeting'),
        (COMMITTEE_MEETING, 'Committee Meeting'),
        
    )
    
    meeting_type = models.CharField('Meeting Type', max_length=30, choices=MEETING_TYPE_CHOICES,
                                     default=MEETING_TYPE_CHOICES[0][0])
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
                                
    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.title)