import re
import json
import sunlight
import twilio
import twilio.rest

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import campaign.secret as secret
import campaign.settings as settings
from campaign.core.models import Campaign

def home(request):
    context = {'campaigns' : Campaign.objects.all()}
    return render(request, 'home.jinja', context)

def locator(request):
    zipcode = request.GET.get('zipcode')
    chamber = request.GET.get('chamber')
    
    if not zipcode or not re.search(r'^(\d{5}(\-\d{4})?)$', zipcode):
        return HttpResponse('Invalid zipcode', status=422)
    
    if chamber and (not chamber == 'senate' and not chamber == 'house'):
        return HttpResponse('Invalid chamber', status=422)

    data = sunlight.congress.locate_legislators_by_zip(zipcode)
    
    if not data:
        return HttpResponse('Could not find legislator', status=422)

    if chamber:
        data = [x for x in data if x['chamber'] == chamber]
    else:
        data = list(data)

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
    
    if settings.DEBUG:
        context['cong_phone'] = secret.debug_phone
    else:
        context['cong_phone'] = cong_data['phone']

    return render(request, 'twiml/dial_callback.jinja', context, content_type="text/xml")
    
def single_campaign(request, slug):
    try:
        context = {'campaign' : Campaign.objects.get(slug=slug)}
    except Campaign.DoesNotExist:
        raise Http404
    return render(request, 'single.jinja', context)
