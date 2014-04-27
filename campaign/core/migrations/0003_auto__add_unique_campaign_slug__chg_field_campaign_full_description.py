# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Campaign', fields ['slug']
        db.create_unique(u'core_campaign', ['slug'])


        # Changing field 'Campaign.full_description'
        db.alter_column(u'core_campaign', 'full_description', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Removing unique constraint on 'Campaign', fields ['slug']
        db.delete_unique(u'core_campaign', ['slug'])


        # Changing field 'Campaign.full_description'
        db.alter_column(u'core_campaign', 'full_description', self.gf('django.db.models.fields.TextField')(max_length=500))

    models = {
        u'core.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'chamber': ('django.db.models.fields.CharField', [], {'default': "'both'", 'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'full_description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']