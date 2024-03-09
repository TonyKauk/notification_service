from django.contrib import admin
from django.contrib.auth.models import Group, User

from api.models import Client, Filter, Mailing, Message, Tag

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Client)
admin.site.register(Filter)
admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(Tag)
