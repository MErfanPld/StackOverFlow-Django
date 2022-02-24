from django.contrib import admin
from .models import Question, Answer, Category, Vote, Sliders


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'slug', 'created']
    search_fields = ('slug', 'body')
    prepopulated_fields = {"slug": ('body',)}
    raw_id_fields = ('user',)


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_reply', 'created']
    raw_id_fields = ('user', 'question')


admin.site.register(Answer, AnswerAdmin)


class CatAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'position']


admin.site.register(Category, CatAdmin)

admin.site.register(Vote)


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']


admin.site.register(Sliders, SliderAdmin)
