from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bgapp.bgModels import *
from django.core import exceptions
from .view_utils import *
from django.shortcuts import render
from .stats import get_topics_Latency, get_user_topics_Latency

import logging
log = logging.getLogger('batground')

@csrf_exempt
@get_topics_Latency.time()
def get_topics(request):
    req = json.loads(request.body.decode('utf-8'))
    try:
        user_db = User.objects.get(userID__exact=req['user_id'])
    except exceptions.ObjectDoesNotExist:
        return JsonResponse({'topics': []})

    if not req['input']:
        topic_suggestions = get_popular_topics()
    else:
        topic_suggestions = get_topic_suggestions(req['input'].strip())[:options_per_page]

    json_content = {
        'topics': [], # [ ['topic', pro, con], ... ]
    }

    for topic in topic_suggestions:
        json_content['topics'].append(
            [topic.content,
             topic.camp(True).users
                 .exclude(userID=user_db.userID)
                 .exclude(isOnline=False)
                 .count(),
             topic.camp(False).users
                 .exclude(userID=user_db.userID)
                 .exclude(isOnline=False)
                 .count()
             ]
        )

    response = JsonResponse(json_content)
    return response


@csrf_exempt
@get_user_topics_Latency.time()
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
    return HttpResponse('Hi, long duong')
