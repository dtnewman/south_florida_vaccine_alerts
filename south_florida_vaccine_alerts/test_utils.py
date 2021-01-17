# -*- coding: utf-8 -*-
"""Helper utilities for testing."""

from flask_testing import TestCase

from south_florida_vaccine_alerts import settings
from south_florida_vaccine_alerts.app import create_app
from south_florida_vaccine_alerts.database import db_session, init_db, drop_db

APP = None


class BaseTestCase(TestCase):

    def create_app(self):
        global APP
        if APP is None:
            APP = create_app(config_object=settings.Test)
        return APP

    def setUp(self):
        self.app = self.create_app()
        self.session = db_session
        init_db()

    def tearDown(self):
        self.session.close()
        drop_db()
        self.session.remove()
