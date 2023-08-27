from django.contrib import admin

from .models import Chat, Message

class MessageInLine(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("title", "job", "completed")
    inlines = (MessageInLine,)