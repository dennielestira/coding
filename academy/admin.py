from django.contrib import admin

from .models import LearningPath, Lesson, QuizQuestion


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "lesson_count")
    search_fields = ("title", "category")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "path", "difficulty", "activity_type")
    search_fields = ("title", "path__title")


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order", "question")
    search_fields = ("question", "lesson__title")
