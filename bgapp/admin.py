from django.contrib import admin
from bgapp.bgModels import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['userID']

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'get_topic_content']

    def get_topic_content(self, obj):
        return obj.topic.content
    get_topic_content.short_description = 'Content'
    get_topic_content.admin_order_field = 'topic__content'

class TopicAdmin(admin.ModelAdmin):
    list_display = ['content']

admin.site.register(User, UserAdmin)
admin.site.register(UserOpinion)
admin.site.register(SessionInfo)

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message)

admin.site.register(Feedback)

admin.site.register(Topic, TopicAdmin)
admin.site.register(ProCamp)
admin.site.register(ConCamp)


