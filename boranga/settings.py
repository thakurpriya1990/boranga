import hashlib
import logging
import os
import sys

import confy
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(BASE_DIR + "/.env"):
    confy.read_environment_file(BASE_DIR + "/.env")
os.environ.setdefault("BASE_DIR", BASE_DIR)

from ledger_api_client.settings_base import *  # noqa: F403

ROOT_URLCONF = "boranga.urls"
SITE_ID = 1
DEPT_DOMAINS = env("DEPT_DOMAINS", ["dpaw.wa.gov.au", "dbca.wa.gov.au"])
SYSTEM_MAINTENANCE_WARNING = env("SYSTEM_MAINTENANCE_WARNING", 24)  # hours
DISABLE_EMAIL = env("DISABLE_EMAIL", False)
SHOW_TESTS_URL = env("SHOW_TESTS_URL", False)
SHOW_DEBUG_TOOLBAR = env("SHOW_DEBUG_TOOLBAR", False)
BUILD_TAG = env(
    "BUILD_TAG", hashlib.md5(os.urandom(32)).hexdigest()
)  # URL of the Dev app.js served by webpack & express
TIME_ZONE = "Australia/Perth"

SILENCE_SYSTEM_CHECKS = env("SILENCE_SYSTEM_CHECKS", False)
if SILENCE_SYSTEM_CHECKS:
    SILENCED_SYSTEM_CHECKS = ["fields.W903", "fields.W904", "debug_toolbar.W004"]

TEMPLATE_TITLE = "Boranga System"
LEDGER_TEMPLATE = "bootstrap5"
EMAIL_DELIVERY = env("EMAIL_DELIVERY", "off")
EMAIL_INSTANCE = env("EMAIL_INSTANCE", "DEV")

GROUP_NAME_DJANGO_ADMIN = "Django Admin"
GROUP_NAME_BORANGA_ADMIN = "Boranga Admin"
GROUP_NAME_ASSESSOR = "ProposalAssessorGroup"
GROUP_NAME_APPROVER = "ProposalApproverGroup"
GROUP_NAME_EDITOR = "ConservationStatusEditorGroup"
GROUP_NAME_REFERRAL = "ProposalReferralGroup"
GROUP_NAME_SPECIES_COMMUNITIES_PROCESSOR = "SpeciesCommunitiesProcessorGroup"

GROUP_NAME_CHOICES = (
    (GROUP_NAME_DJANGO_ADMIN, "Django Admin"),
    (GROUP_NAME_BORANGA_ADMIN, "Boranga Admin"),
    (GROUP_NAME_ASSESSOR, "Proposal Assessor Group"),
    (GROUP_NAME_APPROVER, "Proposal Approver Group"),
    (GROUP_NAME_EDITOR, "Conservation Status Editor Group'"),
    (GROUP_NAME_REFERRAL, "Proposal Referral Group"),
    (GROUP_NAME_SPECIES_COMMUNITIES_PROCESSOR, "Species Communities Processor Group"),
)

if env("CONSOLE_EMAIL_BACKEND", False):
    #    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = "wagov_utils.components.utils.email_backend.EmailBackend"


if SHOW_DEBUG_TOOLBAR:
    #    def get_ip():
    #        import subprocess
    #        route = subprocess.Popen(('ip', 'route'), stdout=subprocess.PIPE)
    #        network = subprocess.check_output(
    #            ('grep', '-Po', 'src \K[\d.]+\.'), stdin=route.stdout
    #        ).decode().rstrip()
    #        route.wait()
    #        network_gateway = network + '1'
    #        return network_gateway

    def show_toolbar(request):
        return True

    MIDDLEWARE_CLASSES += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += ("debug_toolbar",)
    # INTERNAL_IPS = ('127.0.0.1', 'localhost', get_ip())
    INTERNAL_IPS = ("127.0.0.1", "localhost")

    # this dict removes check to dtermine if toolbar should display --> works for rks docker container
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "INTERCEPT_REDIRECTS": False,
    }

STATIC_URL = "/static/"


INSTALLED_APPS += [
    # 'reversion_compare',
    "webtemplate_dbca",
    "boranga",
    "boranga.components.main",
    "boranga.components.organisations",
    "boranga.components.species_and_communities",
    "boranga.components.conservation_status",
    "boranga.components.users",
    "boranga.components.proposals",
    "boranga.components.approvals",
    "boranga.components.compliances",
    "boranga.components.meetings",
    "boranga.components.conservation_plan",
    "boranga.components.occurrence",
    "taggit",
    "rest_framework",
    "rest_framework_datatables",
    "rest_framework_gis",
    "reset_migrations",
    "ckeditor",
    "multiselectfield",
    "import_export",
    "ledger_api_client",
    "appmonitor_client",
    "reversion",
    "reversion_compare",
]

ADD_REVERSION_ADMIN = True

# maximum number of days allowed for a booking
WSGI_APPLICATION = "boranga.wsgi.application"

"""REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'boranga.perms.OfficerPermission',
    )
}"""

# REST_FRAMEWORK = {
#    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#        'PAGE_SIZE': 5
# }

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ),
    # 'DEFAULT_FILTER_BACKENDS': (
    #    'rest_framework_datatables.filters.DatatablesFilterBackend',
    # ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    # 'PAGE_SIZE': 1,
}


MIDDLEWARE_CLASSES += [
    # 'boranga.middleware.BookingTimerMiddleware',
    # 'boranga.middleware.FirstTimeNagScreenMiddleware',
    # 'boranga.middleware.RevisionOverrideMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
MIDDLEWARE = MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES = None

TEMPLATES[0]["DIRS"].append(os.path.join(BASE_DIR, "boranga", "templates"))
TEMPLATES[0]["DIRS"].append(
    os.path.join(BASE_DIR, "boranga", "components", "organisations", "templates")
)
TEMPLATES[0]["DIRS"].append(
    os.path.join(BASE_DIR, "boranga", "components", "emails", "templates")
)

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "boranga.context_processors.config"
)

del BOOTSTRAP3["css_url"]
# BOOTSTRAP3 = {
#    'jquery_url': '//static.dpaw.wa.gov.au/static/libs/jquery/2.2.1/jquery.min.js',
#    'base_url': '//static.dpaw.wa.gov.au/static/libs/twitter-bootstrap/3.3.6/',
#    'css_url': None,
#    'theme_url': None,
#    'javascript_url': None,
#    'javascript_in_head': False,
#    'include_jquery': False,
#    'required_css_class': 'required-form-field',
#    'set_placeholder': False,
# }
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "boranga", "cache"),
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS.append(os.path.join(os.path.join(BASE_DIR, "boranga", "static")))
DEV_STATIC = env("DEV_STATIC", False)
DEV_STATIC_URL = env("DEV_STATIC_URL")
if DEV_STATIC and not DEV_STATIC_URL:
    raise ImproperlyConfigured("If running in DEV_STATIC, DEV_STATIC_URL has to be set")
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Department details
SYSTEM_NAME = "Boranga System"
SYSTEM_NAME_SHORT = env("SYSTEM_NAME_SHORT", "BGA")
SITE_PREFIX = env("SITE_PREFIX")
SITE_DOMAIN = env("SITE_DOMAIN")
SUPPORT_EMAIL = env("SUPPORT_EMAIL", "bio@" + SITE_DOMAIN).lower()
DEP_URL = env("DEP_URL", "www." + SITE_DOMAIN)
DEP_PHONE = env("DEP_PHONE", "(08) 9219 9978")
DEP_PHONE_SUPPORT = env("DEP_PHONE_SUPPORT", "(08) 9219 9000")
DEP_FAX = env("DEP_FAX", "(08) 9423 8242")
DEP_POSTAL = env(
    "DEP_POSTAL", "Locked Bag 104, Bentley Delivery Centre, Western Australia 6983"
)
DEP_NAME = env("DEP_NAME", "Department of Biodiversity, Conservation and Attractions")
DEP_NAME_SHORT = env("DEP_NAME_SHORT", "DBCA")
BRANCH_NAME = env("BRANCH_NAME", "Tourism and Concessions Branch")
DEP_ADDRESS = env("DEP_ADDRESS", "17 Dick Perry Avenue, Kensington WA 6151")
SITE_URL = env("SITE_URL", "https://" + SITE_PREFIX + "." + SITE_DOMAIN)
PUBLIC_URL = env("PUBLIC_URL", SITE_URL)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "no-reply@" + SITE_DOMAIN).lower()
MEDIA_APP_DIR = env("MEDIA_APP_DIR", "boranga")
ADMIN_GROUP = env("ADMIN_GROUP", "Boranga Admin")
DJANGO_ADMIN_GROUP = env("DJANGO_ADMIN_GROUP", "Django Admin")
CRON_RUN_AT_TIMES = env("CRON_RUN_AT_TIMES", "04:05")
CRON_EMAIL = env("CRON_EMAIL", "cron@" + SITE_DOMAIN).lower()
# for ORACLE Job Notification - override settings_base.py
EMAIL_FROM = DEFAULT_FROM_EMAIL
OTHER_PAYMENT_ALLOWED = env("OTHER_PAYMENT_ALLOWED", False)  # Cash/Cheque

OSCAR_BASKET_COOKIE_OPEN = "boranga_basket"
PAYMENT_SYSTEM_ID = env("PAYMENT_SYSTEM_ID", "S677")
PAYMENT_SYSTEM_PREFIX = env(
    "PAYMENT_SYSTEM_PREFIX", PAYMENT_SYSTEM_ID.replace("S", "0")
)  # '0557'
os.environ["LEDGER_PRODUCT_CUSTOM_FIELDS"] = (
    "('ledger_description','quantity','price_incl_tax','price_excl_tax','oracle_code')"
)
CRON_NOTIFICATION_EMAIL = ""
if NOTIFICATION_EMAIL:
    CRON_NOTIFICATION_EMAIL = env("CRON_NOTIFICATION_EMAIL", NOTIFICATION_EMAIL).lower()

if not VALID_SYSTEMS:
    VALID_SYSTEMS = [PAYMENT_SYSTEM_ID]

CRON_CLASSES = [
    "boranga.cron.OracleIntegrationCronJob",
    "appmonitor_client.cron.CronJobAppMonitorClient",
]


BASE_URL = env("BASE_URL")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        # 'width': 300,
        "width": "100%",
    },
    "awesome_ckeditor": {
        "toolbar": "Basic",
    },
}

# Additional logging for boranga
LOGGING["handlers"]["payment_checkout"] = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": os.path.join(BASE_DIR, "logs", "boranga_payment_checkout.log"),
    "formatter": "verbose",
    "maxBytes": 5242880,
}
LOGGING["loggers"]["payment_checkout"] = {
    "handlers": ["payment_checkout"],
    "level": "INFO",
}

LOGGING["loggers"]["boranga"] = {"handlers": ["file"], "level": "INFO"}
if DEBUG:
    LOGGING["loggers"]["boranga"] = {"handlers": ["console"], "level": "DEBUG"}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DEV_APP_BUILD_URL = env(
    "DEV_APP_BUILD_URL"
)  # URL of the Dev app.js served by webpack & express


# Use git commit hash for purging cache in browser for deployment changes
GIT_COMMIT_HASH = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%H"
).read()  # noqa: S605
GIT_COMMIT_DATE = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%cd"
).read()  # noqa: S605
if len(GIT_COMMIT_HASH) == 0:
    GIT_COMMIT_HASH = os.popen("cat /app/git_hash").read()
    if len(GIT_COMMIT_HASH) == 0:
        logger.error("No git hash available to tag urls for pinned caching")

APPLICATION_VERSION = env("APPLICATION_VERSION", "1.0.0") + "-" + GIT_COMMIT_HASH[:7]

RUNNING_DEVSERVER = len(sys.argv) > 1 and sys.argv[1] == "runserver"

# Sentry settings
SENTRY_DSN = env("SENTRY_DSN", default=None)
SENTRY_SAMPLE_RATE = env("SENTRY_SAMPLE_RATE", default=1.0)  # Error sampling rate
SENTRY_TRANSACTION_SAMPLE_RATE = env(
    "SENTRY_TRANSACTION_SAMPLE_RATE", default=0.0
)  # Transaction sampling
if not RUNNING_DEVSERVER and SENTRY_DSN and EMAIL_INSTANCE:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        sample_rate=SENTRY_SAMPLE_RATE,
        traces_sample_rate=SENTRY_TRANSACTION_SAMPLE_RATE,
        environment=EMAIL_INSTANCE.lower(),
        release=APPLICATION_VERSION,
    )

# LEDGER_UI_ACCOUNTS_MANAGEMENT = [
#            {'first_name': {'options' : {'view': True, 'edit': True}}},
#            {'last_name': {'options' : {'view': True, 'edit': True}}},
#            {'residential_address': {'options' : {'view': True, 'edit': True}}},
#            {'phone_number' : {'options' : {'view': True, 'edit': True}}},
#            {'mobile_number' : {'options' : {'view': True, 'edit': True}}},
# ]

# NOMOS login details
NOMOS_URL = env("NOMOS_URL")
NOMOS_USERNAME = env("NOMOS_USERNAME")
NOMOS_PASSWORD = env("NOMOS_PASSWORD")
KMI_SERVER_URL = env("KMI_SERVER_URL", "https://kmi.dbca.wa.gov.au")

# ---------- Identifier fields for logging ----------

""" Fields that the logging functions will check for on the instance
    and use to identify the instance in the logs. """
ACTION_LOGGING_IDENTIFIER_FIELDS = [
    "lodgement_number",
    "occurrence_number",
    "occurrence_report_number",
    "id",
]

# ---------- User Log Actions ----------

ACTION_VIEW = "View {} {}"
ACTION_CREATE = "Create {} {}"
ACTION_UPDATE = "Update {} {}"
ACTION_DESTROY = "Destroy {} {}"

# ---------- Cache keys ----------

CACHE_KEY_EPSG_CODES = "epsg-codes-{auth_name}-{pj_type}"
