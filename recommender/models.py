from django.db import models

class Mood(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name.title()


class Movie(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rating = models.FloatField()
    release_year = models.IntegerField()
    url = models.URLField()
    poster = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Music(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube = models.URLField()

    def __str__(self):
        return self.title

