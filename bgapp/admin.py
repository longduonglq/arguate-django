from django.contrib import admin
from bgapp.bgModels import *

class CustomModelMixin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_display.append('pk')
        super(CustomModelMixin, self).__init__(model, admin_site)

class UserMixin(admin.ModelAdmin):
    list_display = ['isOnline', 'isBanned', 'isLooking', 'user_ID', 'topics_display']
    def user_ID(self, obj):
        return str(obj.userID)
    user_ID.short_description = 'UserID'

    def topics_display(self, obj):
        return ', '.join([
            userOp.topic.content for userOp in obj.opinions.filter(isDeleted=False).all()
        ])
    topics_display.short_description = 'Topics'

class UserOpinionMixin(admin.ModelAdmin):
    list_display = ['isDeleted', 'position', 'topic_content', 'user_userID']
    def topic_content(self, obj):
        return obj.topic.content
    topic_content.short_description = 'Topic Content'
    topic_content.admin_order_field = 'topic__content'

    def user_userID(self, obj):
        return obj.user.userID
    user_userID.short_description = 'UserID'
    user_userID.admin_order_field = 'user__userID'

class ConversationMixin(admin.ModelAdmin):
    list_display = ['timeStart', 'timeEnd', 'isEnded', 'users_list', 'topic_content']
    def users_list(self, obj):
        return ', '.join([
            str(user.userID)[:7] for user in obj.users.all()
        ])
    users_list.short_description = 'Users'

    def topic_content(self, obj):
        return obj.topic.content
    topic_content.short_description = 'Topic'

class CampMixin(admin.ModelAdmin):
    list_display = ['topic_content', 'pk']
    def topic_content(self, obj):
        return obj.topic.content
    topic_content.short_description = 'Topic'


admin.site.register(User, UserMixin)
admin.site.register(UserOpinion, UserOpinionMixin)
admin.site.register(SessionInfo, CustomModelMixin)

admin.site.register(Conversation, ConversationMixin)
admin.site.register(Message, CustomModelMixin)

admin.site.register(Feedback, CustomModelMixin)

admin.site.register(Topic, CustomModelMixin)
admin.site.register(ProCamp, CampMixin)
admin.site.register(ConCamp, CampMixin)


