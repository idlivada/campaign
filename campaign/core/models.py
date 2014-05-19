import urlparse
import urllib

from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from docutils.core import publish_parts
import campaign.secret

class Campaign(models.Model):
    CHAMBER_HOUSE = 'house'
    CHAMBER_SENATE = 'senate'
    CHAMBER_BOTH = 'both'
    CHAMBER_CHOICES = (
        (CHAMBER_HOUSE, 'House'),
        (CHAMBER_SENATE, 'Senate'),
        (CHAMBER_BOTH, 'Both'),
        )
    chamber = models.CharField(max_length=6, 
                               choices=CHAMBER_CHOICES, 
                               default=CHAMBER_BOTH)
 
    title = models.CharField(max_length=50, help_text="Descriptive title. Example: Stop Flawed Anti-India & Anti-Hindu H.Res 417. Max length: 50 chars.")
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(max_length=500, 
                                   help_text="Short description of this campaign used on the homepage. Max length: 500 chars.")
    full_description = models.TextField(help_text="Full description of this campaign. This can be long and detailed. You can use rst formatting: http://docutils.sourceforge.net/docs/user/rst/quickref.html")
    script = models.TextField(help_text="Script that callers should read out. You can use the following template variables CONGNAME for the Congressperson's name (example: Senator Elizabeth Warren), and YOURNAME for the caller's name (example: Mihir Meghani)")
    tweet_text = models.CharField(max_length=120, help_text="Tweet text. URL & Congressperson handle will automatically be added.  Max length: 120 chars. Example: Vote no to flawed Anti-Hindu H.Res 417.")
    short_url = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('core.views.single_campaign', args=[self.slug])
    
    def get_formatted_full_description(self):
        return publish_parts(self.full_description, writer_name='html')['body']

    def get_formatted_script(self):
        return self.script.replace('CONGNAME', '<span class="cong-name"></span>').\
            replace('YOURNAME', '<span class="your-name"></span>')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        
            url = urlparse.urljoin(campaign.secret.BASE_URL, self.get_absolute_url())
            params = urllib.urlencode({'format':'simple', 'url': url})
            u = urllib.urlopen('http://is.gd/create.php?%s' % params)
            self.short_url = u.read()
            u.close()

        super(Campaign, self).save(*args, **kwargs)

class Member(models.Model):
    firstname = models.CharField(max_length=35)
    lastname = models.CharField(max_length=35)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    
    
