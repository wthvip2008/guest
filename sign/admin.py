from django.contrib import admin
from sign.models import Event
from sign.models import Guest


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_time', 'id']
    search_fields = ['name']  # 搜索功能
    list_filter = ['status']  # 过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email',
                    'sign', 'create_time', 'event_id']
    list_display_links = ('realname', 'phone')  # 显示链接
    search_fields = ['realname', 'phone']  # 搜索功能
    list_filter = ['event_id']  # 过滤器


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)

# from datetime import datetime
# el = Event(id = 2, name="红米发布会",limit=2000, status=True, address='北京', start_time=datetime(2016,8,10,14,0,0))
# el.save()
#
# Event.objects.create(id=3, name='红米max发布会',limit=2000, status=True, address='北京会展中心', start_time=datetime(2016,10,10,14,0,0))
# el = Event.objects.get('红米max发布会')