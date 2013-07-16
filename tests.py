from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
UserModel = get_user_model()

from django_dynamic_fixture import G

from binder.test_utils import AptivateEnhancedTestCase

class LogframeTest(AptivateEnhancedTestCase):
    pass
