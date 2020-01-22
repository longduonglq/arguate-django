from django.contrib import admin
from bgapp.bgModels import *

class CustomModelMixin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelMixin, self).__init__(model, admin_site)

admin.site.register(User, CustomModelMixin)
admin.site.register(UserOpinion, CustomModelMixin)
admin.site.register(SessionInfo, CustomModelMixin)

admin.site.register(Conversation, CustomModelMixin)
admin.site.register(Message, CustomModelMixin)

admin.site.register(Feedback, CustomModelMixin)

admin.site.register(Topic, CustomModelMixin)
admin.site.register(ProCamp, CustomModelMixin)
admin.site.register(ConCamp, CustomModelMixin)


