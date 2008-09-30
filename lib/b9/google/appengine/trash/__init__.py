import logging
import re
import hashlib
import datetime

from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.ext import webapp
from django.utils import simplejson

class Trash(db.Model):
    reference_key = db.StringProperty(None, required = True) # TODO This should be a KeyProperty
    reference_kind = db.StringProperty(required = True)
    freshness = db.DateTimeProperty(auto_now_add = True, required = True)
    expiring = db.DateTimeProperty()

    def reference(self):
        return db.Key(self.reference_key)

    @staticmethod
    def throw_away(model, expiring = None):
        trash = Trash.get_or_insert(
            key_name = str(model.key()),
            reference_kind = model.key().kind(),
            reference_key = str(model.key()),
            expiring = expiring,
        )
        logging.info(trash.reference_kind)
        trash.put()
        return trash
