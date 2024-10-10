from django.db import models


class PlayerScore(models.Model):
    name = models.CharField(max_length=100)
    time = models.IntegerField()
    level = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        default="easy",
    )

    def __str__(self):
        return f"{self.name} - {self.time} seconds - {self.level} level"


class Leaderboard(models.Model):
    player_name = models.CharField(max_length=100)
    score = models.IntegerField()
    time = models.IntegerField()  # time in seconds

    def __str__(self):
        return f"{self.player_name}: {self.score} points"
