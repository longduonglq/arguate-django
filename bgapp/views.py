from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bgapp.bgModels import *
from django.core import exceptions
from .view_utils import *
from statsd.defaults.django import statsd
from django.shortcuts import render

import logging
log = logging.getLogger('batground')

@csrf_exempt
@statsd.timer('getTopics_Time')
def get_topics(request):
    req = json.loads(request.body.decode('utf-8'))
    try:
        user_db = User.objects.get(userID__exact=req['user_id'])
    except exceptions.ObjectDoesNotExist:
        return JsonResponse({'topics': []})

    if not req['input']:
        topic_suggestions = get_popular_topics()
    else:
        kws = req['input'].strip().split(' ')
        q_obj = models.Q(content__icontains=kws[0])
        for kw in kws[1:]:
            q_obj = q_obj | models.Q(content__icontains=kw)

        topic_suggestions = Topic.objects.filter(q_obj)[:options_per_page]

    json_content = {
        'topics': [], # [ ['topic', pro, con], ... ]
    }

    for topic in topic_suggestions:
        json_content['topics'].append(
            [topic.content, topic.pro_camp.user_count, topic.con_camp.user_count]
        )

    #log.debug(json_content['topics'])
    response = JsonResponse(json_content)
    return response


@csrf_exempt
@statsd.timer('getUserTopics_Time')
def get_user_topics(request):
    req = json.loads(request.body.decode('utf-8'))
    try:
        user_db = User.objects.get(userID__exact=req['user_id'])
    except exceptions.ObjectDoesNotExist:
        return JsonResponse({'topics': []})

    user_opinions = user_db.opinions.filter(isDeleted=False)
    json_content = {
        'topics': [] # [ [topics, position], ... ]
    }
    for opinion in user_opinions:
        json_content['topics'].append(
            [opinion.topic.content, opinion.position]
        )

    response = JsonResponse(json_content)
    return response

@csrf_exempt
def itsme(request):
    return HttpResponse('long duong')
