from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
import uuid

class Team(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1', null = True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2', null = True, blank=True)
    player3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player3', null = True, blank=True)
    player4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player4', null = True, blank=True)
    player5 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player5', null = True, blank=True)


class GameSession(models.Model):
    #players = models.ManyToManyField(Profile)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1', null = True, blank=True)
    team2 = models.ForeignKey(Team,  on_delete=models.SET_NULL, related_name='team2', null = True, blank=True)
    winner_team = models.ForeignKey(Team,  on_delete=models.SET_NULL, related_name='winner_team', null = True, blank=True)
    moves = models.TextField(default = "[]",null=True)
    name = models.TextField(default="My Game!")
    gameid = models.UUIDField(default = uuid.uuid4)
    isFinished = models.BooleanField(default=False)
    isPrivate = models.BooleanField(default=False)
