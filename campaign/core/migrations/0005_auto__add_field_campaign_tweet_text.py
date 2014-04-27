# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Campaign.tweet_text'
        db.add_column(u'core_campaign', 'tweet_text',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=120),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Campaign.tweet_text'
        db.delete_column(u'core_campaign', 'tweet_text')


    models = {
        u'core.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'chamber': ('django.db.models.fields.CharField', [], {'default': "'both'", 'max_length': '6'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'full_description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tweet_text': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['core']