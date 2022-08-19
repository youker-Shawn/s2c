from django.contrib import admin

from accounts.models import MyUser

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'invite', 'invitedby','invitedbycode']
    
    # 自定义显示 邀请人的邀请码 字段
    def invitedbycode(self, obj):
        code = ''
        try:
            code = MyUser.objects.get(pk=obj.invitedby).invite
        except Exception as e:
            pass
        return code
        
    invitedbycode.short_description = "invited by code"

admin.site.register(MyUser, UserAdmin)