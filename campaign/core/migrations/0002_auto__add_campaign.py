# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Campaign'
        db.create_table(u'core_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('full_description', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('script', self.gf('django.db.models.fields.TextField')()),
            ('chamber', self.gf('django.db.models.fields.CharField')(default='both', max_length=1)),
        ))
        db.send_create_signal(u'core', ['Campaign'])


    def backwards(self, orm):
        # Deleting model 'Campaign'
        db.delete_table(u'core_campaign')


    models = {
        u'core.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'chamber': ('django.db.models.fields.CharField', [], {'default': "'both'", 'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'full_description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']