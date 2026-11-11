from django.db import models


class LearningPath(models.Model):
    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("it_support", "IT Support"),
        ("hardware", "Computer Hardware"),
        ("networking", "Networking"),
        ("security", "Cybersecurity"),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default="programming")
    description = models.TextField()
    icon = models.CharField(max_length=40, default="bi-code-slash")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "title"]

    def __str__(self):
        return self.title

    @property
    def lesson_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    ACTIVITY_CHOICES = [
        ("code", "Code Challenge"),
        ("support", "Support Scenario"),
        ("concept", "Concept Lesson"),
    ]

    path = models.ForeignKey(LearningPath, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    introduction = models.TextField()
    explanation = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default="code")
    activity_prompt = models.TextField(blank=True)
    activity_choices = models.JSONField(default=list, blank=True)
    starter_code = models.TextField(blank=True)
    expected_keywords = models.JSONField(default=list, blank=True)
    hint = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    difficulty = models.CharField(max_length=30, default="Beginner")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["path__category", "order", "title"]

    def __str__(self):
        return f"{self.path.title}: {self.title}"


class QuizQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="quiz_questions", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_index = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
