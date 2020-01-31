from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from django.core import exceptions
from django.db import models, utils

from datetime import timedelta
from django.utils import timezone
import uuid
import logging
import json

from bgapp.bgModels import *
from .consumer_utils import *
from .error_msgs import *
from .tasks import *
from .stats import online_user_Num, new_users_Num, \
                    active_convo_Num, new_convo_Num, \
                    topics_created, active_topics_num, \
                    opinions_registered, active_opinion_num, \
                    start_chat_Wait, conversation_duration, session_duration, \
                    found_fail
from .ChannelMap import *

log = logging.getLogger('batground')
log.setLevel(logging.DEBUG)

class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.user_db_ref = None
        self.user_id = None
        self.contact_db = None
        self.session_info_db = None
        self.cur_conversation_db = None

    def inform_client_of_error(self, **kwargs):
        if 'log_msg' in kwargs:
            logging.warning(kwargs['log_msg'])

        json_content = {
            'cmd': kwargs['type'],
        }
        if 'data' in kwargs:
            json_content['data'] = kwargs['data']
        self.send_json(content=json_content)

    def user_id(self, data):
        self.user_id = data['id']
        try:
            self.user_db_ref = User.objects.get(
                userID=data['id']
            )
        except exceptions.ObjectDoesNotExist:
            self.user_db_ref = User.objects.create(userID=self.user_id)
            new_users_Num.inc()
        except Exception as e:
            return None

        if self.user_db_ref.isBanned:
            self.disconnect(0)

        self.user_db_ref.isOnline = True
        self.user_db_ref.isActive = True
        self.user_db_ref.channelID = self.channel_name # map channel name with user
        self.user_db_ref.save()

        self.session_info_db = SessionInfo.objects.create(
            ip=self.scope['client'][0],
            timeEnd=timezone.now(),
            user=self.user_db_ref
        )

        # register user into all camp before connect
        for opinion in self.user_db_ref.opinions.filter(isDeleted=False):
            opinion.topic.camp(opinion.position).users.add(self.user_db_ref)
            opinion.topic.users.add(self.user_db_ref)

        # stats logging
        online_user_Num.inc()

        self.send_json(content={
            'cmd': 'user_id_confirmed'
        })

    def connect(self):
        self.accept()

    def disconnect(self, code):
        online_user_Num.dec()
        self.user_db_ref.channelID = None
        self.user_db_ref.save() # unmap user to channel name
        # unregister user from all camp and topic before disconnect
        for opinion in self.user_db_ref.opinions.filter(isDeleted=False):
            opinion.topic.camp(opinion.position).users.remove(self.user_db_ref)
            opinion.topic.users.remove(self.user_db_ref)

        if self.session_info_db is not None:
            # in case a brief connection was made. client didn't send user_id
            # so no session object created
            self.session_info_db.timeEnd = timezone.now()
            self.session_info_db.save()

            # stats
            session_length = getMinutes(self.session_info_db.timeEnd - self.session_info_db.timeStart)
            if session_length > 0:
                session_duration.observe(
                    session_length
                )

        self.user_db_ref.isOnline = False
        self.user_db_ref.isLooking = False
        self.user_db_ref.save()

        if self.cur_conversation_db is not None:
            self.cur_conversation_db.timeEnd = timezone.now()
            self.cur_conversation_db.isEnded = True
            self.cur_conversation_db.save()

        if self.contact_db is not None \
                and checkUserIdInMap(self.contact_db):
            async_to_sync(self.channel_layer.send)(
                getChannelID(self.contact_db),
                {
                    'type': 'receive_end_chat',
                    'cmd': 'receive_end_chat',
                }
            )

    def receive_json(self, data, **kwargs):
        log.debug('-*-*-receive json: {}'.format(data))
        cmd = data['cmd']
        if cmd in self.cmd_handlers:
            # try append cmd to activity history
            if self.user_db_ref is not None:
                try:
                    self.user_db_ref.activity += json.dumps(data) + '\n'
                    self.user_db_ref.save()
                except utils.DataError:
                    self.user_db_ref.activity = json.dumps(data)
                    self.user_db_ref.save()

            self.cmd_handlers[cmd](self, data)

    def receive_start_chat(self, data):
        self.contact_db = User.objects.get(userID__exact=data['contact_id'])
        self.cur_conversation_db = Conversation.objects.get(conversation_id=data['conversation_id'])

        self.user_db_ref.isLooking = False
        self.user_db_ref.save()

        self.send_json(content={
            'cmd': 'start_chat_success',
            'contact_id': data['contact_id'],
            'conversation_id': data['conversation_id'],
            'topic': data['topic'],
            'opinion': data['opinion']
        })

    def send_feedback(self, data):
        """
            data keys: cmd, email, feedback
        :param data:
        :return:
        """
        Feedback.objects.create(
            user=self.user_db_ref,
            email=data['email'],
            feedback=data['feedback']
        )

    def start_chat(self, data):
        """
            data key: cmd

            1. send msg contains contact_id, conversation_id to opponent
            2. send conversation_id to this user
                { 'cmd': 'start_chat_success', 'conversation_id': ... }
        """
        opinion_list = self.user_db_ref.opinions
        if opinion_list.filter(isDeleted=False).count() == 0:
            self.inform_client_of_error(
                type='start_chat_err.could_not_start'
            )
            return None

        self.user_db_ref.isLooking = True
        self.user_db_ref.save()

        opponent, opinion = get_opponent(opinion_list)

        if opponent == 'NOT_FOUND':
            self.inform_client_of_error(
                type='start_chat_err.no_opponents'
            )
            found_fail.labels(status='fail').inc()
        else:
            try:
                self.cur_conversation_db = Conversation.objects.create(
                    timeEnd=timezone.now(),
                    topic=opinion.topic
                )
                self.cur_conversation_db.users.add(self.user_db_ref, opponent)

                self.contact_db = opponent

                self.user_db_ref.isLooking = False
                self.user_db_ref.save()

                async_to_sync(self.channel_layer.send)(
                    getChannelID(self.contact_db),
                    {
                        'type': 'receive_start_chat',
                        'cmd': 'receive_start_chat',
                        'contact_id': self.user_id,
                        'conversation_id': str(self.cur_conversation_db.conversation_id),
                        'topic': opinion.topic.content,
                        'opinion': opinion.position # this is ur opinion
                    }
                )

                self.send_json(content={
                    'cmd': 'start_chat_success',
                    'contact_id': str(self.contact_db.userID),
                    'conversation_id': str(self.cur_conversation_db.conversation_id),
                    'topic': opinion.topic.content,
                    'opinion': not opinion.position # this is the other opinion
                })

                active_convo_Num.inc()
                new_convo_Num.inc()
                found_fail.labels(status='found').inc()
            except Exception as e:
                self.user_db_ref.isLooking = False
                self.user_db_ref.save()
                self.inform_client_of_error(
                    log_msg='unexpected error [{}, type: {}] in start chat'.format(str(e),
                                                                                str(type(e))),
                    type='start_chat_err.could_not_start'
                )

    def receive_end_chat(self, data):
        self.send_json(content={
            'cmd': 'receive_end_chat',
        })

        self.contact_db = None
        self.cur_conversation_db = None

        self.user_db_ref.isLooking = False
        self.user_db_ref.save()

    def end_chat(self, data):
        """
            data keys: cmd
        """
        if self.cur_conversation_db is not None:
            self.cur_conversation_db.timeEnd = timezone.now()
            self.cur_conversation_db.isEnded = True
            self.cur_conversation_db.save()

            # stat collection
            active_convo_Num.dec()
            dur = getMinutes(self.cur_conversation_db.timeEnd - self.cur_conversation_db.timeStart)
            if dur > 0:
                conversation_duration.observe(dur)

            if checkUserIdInMap(self.contact_db):
                async_to_sync(self.channel_layer.send)(
                    getChannelID(self.contact_db),
                    {
                        'type': 'receive_end_chat',
                        'cmd': 'receive_end_chat',
                    }
                )

        self.contact_db = None
        self.cur_conversation_db = None

        self.user_db_ref.isLooking = False
        self.user_db_ref.save()

    def receive_typing_status(self, data):
        self.send_json(content=data)

    def typing_status(self, data):
        async_to_sync(self.channel_layer.send)(
            getChannelID(self.contact_db),
            {
                'type': 'receive_typing_status',
                'cmd': 'receive_typing_status',
                'isTyping': data['isTyping']
            }
        )

    def receive_msg_from(self, data):
        """
            data keys: msg
        :param data:
        :return:
        """
        self.send_json(content={
            'cmd': 'receive_msg_from',
            'msg': data['msg']
        })

    def send_msg_to(self, data):
        """
            data keys: cmd, msg
        """
        msg = data['msg']
        passed, reason = msg_security_check(msg)
        if not passed:
            self.inform_client_of_error(
                type='send_msg_to_error',
                data=reason
            )
            return None

        Message.objects.create(
            content=msg,
            conversation=self.cur_conversation_db,
            sender=self.user_db_ref,
            receiver=self.contact_db
        )

        async_to_sync(self.channel_layer.send)(
            getChannelID(self.contact_db),
            {
                'type': 'receive_msg_from',
                'msg': msg
            }
        )

    def report_user(self, data):
        """
            data keys: cmd, complaint_code, complaint, conversation_id
        :param data:
        :return:
        """
        accused = Conversation.objects.get(conversation_id=data['conversation_id']).\
            users.exclude(userID=self.user_id).first()

        UserComplaint.objects.create(
            conversation=data['conversation_id'],
            filedBy=self.user_db_ref,
            accused=accused,
            complaintCode=data['complaint_code'],
            complaint=data['complaint']
        )

    def register_opinion(self, data):
        """
            1. create UserOpinion object
            2. register user to ProCamp or ConCamp object

            data keys: cmd, topic, position
        """
        try:
            topic_db = Topic.objects.get(content__iexact=data['topic'].strip())
        except exceptions.ObjectDoesNotExist:
            # new topic, trying to create in db
            passed, reason = topic_security_check(data['topic'])
            if not passed:
                self.inform_client_of_error(
                    type='register_opinion_err.reason',
                    data=reason
                )
                return None

            topic_db = Topic.objects.create(
                userStarted=self.user_db_ref,
                content=data['topic'],
            )

            topics_created.inc()
            active_topics_num.inc()

        except Exception as e:
            self.inform_client_of_error(
                log_msg=str(e),
                type='register_opinion_err',
            )
            return None

        if self.user_db_ref.opinions.filter(isDeleted=False, topic=topic_db).count() > 0:
            return None

        UserOpinion.objects.create(
            timeEnd=timezone.now(),
            position=data['position'],
            topic=topic_db,
            user=self.user_db_ref
        )

        topic_db.camp(data['position']).users.add(self.user_db_ref)
        topic_db.camp(data['position']).save()

        opinions_registered.inc()
        active_opinion_num.inc()
        # what topics is an online user currently engage in
        self.user_db_ref.topics.add(topic_db)

        topic_db.save()

    def change_opinion(self, data):
        """
            1. change UserOpinion object
            2. change user Camp

            data keys: cmd, topic
        """
        try:
            user_opinion = self.user_db_ref.opinions.filter(
                topic__content__iexact=data['topic'],
                isDeleted=False
            ).order_by('-timeStart')[0]
        except Exception as e:
            self.inform_client_of_error(
                log_msg=str(e),
                type='change_opinion_err',
            )
            return None

        # change camp
        try:
            topic_db = Topic.objects.get(content__iexact=data['topic'])
            topic_db.camp(user_opinion.position).users.remove(self.user_db_ref)
            topic_db.camp(user_opinion.position).save()

            topic_db.camp(not user_opinion.position).users.add(self.user_db_ref)
            topic_db.camp(not user_opinion.position).save()
        except Exception as e:
            self.inform_client_of_error(
                log_msg=str(e),
                type='change_opinion_err'
            )
            return None

        user_opinion.position = not user_opinion.position
        user_opinion.save()

    def unregister_opinion(self, data):
        """
            1. mark UserOpinion object as deleted
            2. unregister user from ___Camp

            data keys: cmd, topic
        """
        try:
            user_opinion = self.user_db_ref.opinions.filter(
                topic__content__iexact=data['topic'],
                isDeleted=False
            ).order_by('-timeStart')[0]
        except Exception as e:
            self.inform_client_of_error(
                log_msg=str(e),
                type='unregister_opinion_err: {}'.format(e),
            )
            return None
        user_opinion.isDeleted = True
        user_opinion.timeEnd = timezone.now()
        user_opinion.save()

        active_opinion_num.dec()
        # unregister user from Camp
        topic_db = None
        try:
            topic_db = Topic.objects.get(content__iexact=data['topic'])
            topic_db.camp(user_opinion).users.remove(self.user_db_ref)
            topic_db.camp(user_opinion).save()
        except Exception as e:
            self.inform_client_of_error(
                log_msg=str(e),
                type='unregister_opinion_err: {}'.format(e)
            )

        if topic_db is not None:
            self.user_db_ref.topics.remove(topic_db)

    def start_chat_wait_time(self, data):
        start_chat_Wait.observe(data['time'])

    cmd_handlers = {
        'user_id': user_id,
        'send_feedback': send_feedback,
        'start_chat': start_chat,
        'end_chat': end_chat,
        'send_msg_to': send_msg_to,
        'report_user': report_user,

        'typing_status': typing_status,

        'register_opinion': register_opinion,
        'change_opinion': change_opinion,
        'unregister_opinion': unregister_opinion,

        'start_chat_wait_time': start_chat_wait_time
    }

