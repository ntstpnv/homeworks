from random import randint, sample

from django.db import models, transaction
from faker import Faker


class Student(models.Model):
    name = models.CharField(max_length=64, unique=True)

    courses = models.ManyToManyField("Course", "students", through="StudentCourse")

    class Meta:
        ordering = ["name"]


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)

    lecturers = models.ManyToManyField("Lecturer", "courses", through="CourseLecturer")

    class Meta:
        ordering = ["name"]


class Lecturer(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]


class StudentCourse(models.Model):
    student = models.ForeignKey("Student", models.CASCADE)
    course = models.ForeignKey("Course", models.CASCADE)

    class Meta:
        unique_together = ["student", "course"]


class CourseLecturer(models.Model):
    course = models.ForeignKey("Course", models.CASCADE)
    lecturer = models.ForeignKey("Lecturer", models.CASCADE)

    class Meta:
        unique_together = ["course", "lecturer"]


class Article(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField(unique=True)
    published_at = models.DateTimeField()

    tags = models.ManyToManyField("Tag", "articles", through="ArticleTag")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_at"]


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ArticleTag(models.Model):
    article = models.ForeignKey("Article", models.CASCADE, "article_ids")
    tag = models.ForeignKey("Tag", models.CASCADE, "tag_ids")

    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_main", "tag__name"]
        unique_together = ["article", "tag"]


class DBManager:
    def __init__(self):
        self.fake = Faker("ru_RU")
        self.students = [Student(name=self.fake.name()) for _ in range(16)]
        self.courses = [Course(name=self.fake.bs()) for _ in range(4)]
        self.lecturers = [Lecturer(name=self.fake.name()) for _ in range(8)]

    def generate(self) -> None:
        with transaction.atomic():
            Student.objects.all().delete()
            Course.objects.all().delete()
            Lecturer.objects.all().delete()

            Student.objects.bulk_create(self.students)
            Course.objects.bulk_create(self.courses)
            Lecturer.objects.bulk_create(self.lecturers)

            [
                student.courses.add(*sample(self.courses, randint(1, 4)))
                for student in self.students
            ]
            [
                course.lecturers.add(*self.lecturers[i * 2 : (i + 1) * 2])
                for i, course in enumerate(self.courses)
            ]

    @staticmethod
    def get_courses():
        return Course.objects.prefetch_related("lecturers", "students")

    @staticmethod
    def get_articles():
        return Article.objects.prefetch_related("article_ids__tag")
