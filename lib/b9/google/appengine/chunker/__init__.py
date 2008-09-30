import datetime
import logging
import types
import os
import re

from google.appengine.ext import webapp
from google.appengine.ext import db
#from google.appengine.api import datastore_types

from django.utils import simplejson

def status_ok(handler, entity):
    handler.response.set_status(200)
    _set_entity(handler, entity)

def status_created(handler, entity):
    handler.response.set_status(201)
    _set_entity(handler, entity)

def status_accepted(handler, entity):
    handler.response.set_status(202)
    _set_entity(handler, entity)

def status_not_found(handler, message):
    handler.error(404)
    logging.debug("Status Not Found: %s" % (message,))
    _set_entity(handler, { "error": message })

def status_bad_request(handler, message):
    handler.error(400)
    logging.debug("Status Bad Request: %s" % (message,))
    _set_entity(handler, { "error": message })

def _set_entity(handler, entity):
    if entity is None:
        entity = {}
#   handler.response.headers["Content-Type"] = "application/json"
    handler.response.headers["Content-Type"] = "text/plain"
    handler.response.out.write(simplejson.dumps(entity))

def empty(value):
    return not(bool(value) or value is 0)

def default(value, default=''):
    return value if not empty(value) else default

class ChunkMessage(db.Model):
    length = db.IntegerProperty(required = True)
    cdtime = db.DateTimeProperty(auto_now_add = True)

class Chunk(db.Model):
    message=db.ReferenceProperty(ChunkMessage, required = True)
    rank=db.IntegerProperty(required = True)
    payload=db.TextProperty(required = True)
    cdtime = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp.RequestHandler):

    def assemble_message(self, query):
        message = ""
        for chunk in query:
            message += chunk.payload
        return message;

    def on_complete(self, message, chunk_message):
        ""

    def cleanup(self, chunk_message):
            query = db.GqlQuery("""\
    SELECT * FROM Chunk WHERE message = :1 ORDER BY rank
    """, chunk_message)
            for chunk in query:
                db.delete(chunk)
            db.delete(chunk_message)
        
    def prepare_response(self, response, chunk_message, chunk, message):
        ""

    def new_message(self, length):
        chunk_message = ChunkMessage(
            length = length
        )
        chunk_message.put()
        return chunk_message

    def get_message(self, key):
        return ChunkMessage.get_by_id(key)

    def new_chunk(self, chunk_message, rank, payload):
        chunk = Chunk(
            message = chunk_message,
            rank = rank,
            payload = payload,
        )
        chunk.put()
        return chunk


    def get(self):

        message_length = self.request.get("ml", None)
        message_key = self.request.get("mk", None)

        chunk_rank = self.request.get("cr", None)
        chunk_payload = self.request.get("cp", None)

        new_message = empty( message_key )
        chunking = True
        chunk_message = None
        chunk = None

        if new_message:
            message_length = long(message_length)
            if message_length > 1:
                chunk_message = self.new_message(message_length)
                chunk_rank = 0
            else:
                chunking = False
        else:
            chunk_message = self.get_message(long(message_key))

        if chunking:
            chunk = self.new_chunk(chunk_message, int(chunk_rank), chunk_payload)

            query = db.GqlQuery("""\
    SELECT * FROM Chunk WHERE message = :1 ORDER BY rank
    """, chunk_message)

            message = None
            if query.count() == chunk_message.length:
                message = self.assemble_message(query)
        else:
            message = chunk_payload
            
        response = {}
        if chunk_message:
            response["mk"] = chunk_message.key().id()
        if chunk:
            response["ck"] = chunk.key().id()
        if not message is None:
            response["complete"] = True
            self.on_complete(message, chunk_message)

        self.prepare_response(response, chunk_message, chunk, message)

        if not message is None and not chunk_message is None:
            self.cleanup(chunk_message)

        self.respond(response)

    def respond(self, response):
        callback = self.request.get("cb")
        output = simplejson.dumps(response);
        if not empty(callback):
            output = callback + "(" + output + ")"
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(output);
