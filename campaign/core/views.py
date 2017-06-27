import re
import json
import sunlight
import twilio
import twilio.rest
import urllib
import csv

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

import campaign.secret as secret
import campaign.settings as settings
from campaign.core.models import Campaign, Member

sunlight.config.API_KEY = secret.sunlight_api_key

def home(request):
    context = {'campaigns' : Campaign.objects.all().order_by('-id'),
               'org_name' : secret.ORGANIZATION_NAME,
               'org_url' : secret.ORGANIZATION_URL}
    return render(request, 'home.jinja', context)

def locator(request):
    chamber = request.GET.get('chamber')    
    zipcode = request.GET.get('zipcode')
    
    if not zipcode or not re.search(r'^(\d{5}(\-\d{4})?)$', zipcode):
        return HttpResponse('Invalid zipcode', status=422)
    
    if chamber and (not chamber == 'senate' and not chamber == 'house'):
        return HttpResponse('Invalid chamber', status=422)

    params = [request.GET.get(p) for p in ['street','city','state','zipcode']]
    lat_lon = geocode(*params)
    data = sunlight.congress.locate_legislators_by_lat_lon(*lat_lon)
    
    if not data:
        return HttpResponse('Could not find legislator', status=422)

    email = request.GET.get('email').lower()
    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        member = Member(email=email)
    member.firstname = request.GET.get('fname')
    member.lastname = request.GET.get('lname')
    member.phone = re.sub("[^0-9]","",request.GET.get('phone'))
    member.street = request.GET.get('street')
    member.city = request.GET.get('city')
    member.state = request.GET.get('state')
    member.zipcode = request.GET.get('zipcode')
    member.save()

    if chamber:
        data = [x for x in data if x['chamber'] == chamber]
    else:
        data = list(data)

    subject = "New Call Campaign Member: %s %s" % (member.firstname, member.lastname)
    message = '\n'.join(["%s: %s"% (k , v) for k, v in request.GET.iteritems()])
    send_mail(subject, message, secret.ORGANIZATION_FROM_EMAIL, 
              [secret.ORGANIZATION_NOTIFICATION_EMAIL], fail_silently=True)

    return HttpResponse(json.dumps(data), content_type="application/json")

def call(request):
    phone = request.GET.get('phone')
    cong_id = request.GET.get('cong_id') #bioguide_id
    
    if not phone or not re.search(r'^(\d{10})$', phone):
        return HttpResponse('Invalid phone number', status=422)

    cong_data = sunlight.congress.legislator(cong_id)
    if not cong_data:
        return HttpResponse('Invalid congress identifier', status=422)
    
    client = twilio.rest.TwilioRestClient(secret.tw_sid, secret.tw_token)
    client.calls.create(to="+1{%s}" % phone, 
                        from_=secret.tw_caller_id,
                        url=secret.BASE_URL + "dial-callback/?cong_id=%s" % cong_id)

    return HttpResponse()

@csrf_exempt
def dial_callback(request):
    cong_id = request.GET.get('cong_id')
    
    cong_data = sunlight.congress.legislator(cong_id)
    if not cong_data:
        return HttpResponse('Invalid congress identifier', status=422)

    title = cong_data['chamber'] == 'senate' and 'Senator' or 'Representative'

    context = {}
    context['cong_name'] = '%s %s %s' % (title, cong_data['first_name'], cong_data['last_name'])
    context['org_name'] = secret.ORGANIZATION_NAME
    
    if settings.DEBUG:
        context['cong_phone'] = secret.debug_phone
    else:
        context['cong_phone'] = cong_data['phone']

    return render(request, 'twiml/dial_callback.jinja', context, content_type="text/xml")
    
def single_campaign(request, slug):
    try:
        context = {'campaign' : Campaign.objects.get(slug=slug),
                   'org_name' : secret.ORGANIZATION_NAME,
                   'org_url' : secret.ORGANIZATION_URL}
    except Campaign.DoesNotExist:
        raise Http404
    return render(request, 'single.jinja', context)


def geocode(street, city, state, zipcode):
    endpoint = 'http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'
    params = urllib.urlencode({'apiKey' : secret.tamu_api_key,
                               'version' : '4.01',
                               'censusYear' : '2010',
                               'streetAddress' : street,
                               'city' : city,
                               'state' : state,
                               'zip' : zipcode})
    r = urllib.urlopen(endpoint+params)
    for row in csv.reader(r):
        pass
    r.close()

    return row[3], row[4]

