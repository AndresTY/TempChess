from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import TemplateView
import main.ChessGame
import json
from django.urls import reverse
from django.http import HttpResponse
from Games.models import GameSession, Team
from django.http import JsonResponse
import numpy as np
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
"""
def home(request):
    games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
 
    context = {"games": games}
    return render(request, 'main/lobby_game.html',context)


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
"""
class PlayGame(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "about.html"
    def get(self, request, format=None, *args, **kwargs):
        data = {"ena":2}
        return Response(data)
"""

def game(request):
    
    if request.method =="GET":
       
        if request.GET.get("create",None):
            context = {}
            return render(request, 'main/create_game.html',context)

        elif request.GET.get("id"):
            gamesess = GameSession.objects.get(gameid=request.GET.get("id"))
            gameid = request.GET.get("id")

            context = {"gameid":gameid, "update":True }
            return render(request, 'main/board.html',context)
        else: #request.GET.get("join",None):

            games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
           
            context = {"games": games}
            return render(request, 'main/lobby_game.html',context)
    elif request.method == "POST":
     
        if request.POST.get("create",None)=="true":
            team1 = Team(player1 = request.user)
            team2 = Team()
            team1.save()
            team2.save()
            gamesess = GameSession(team1 = team1, team2= team2, name = request.POST.get("name","My Game!"), isPrivate = request.POST.get("isPrivate",False)=="on" )
            gamesess.save()
            
        elif request.POST.get("join",None):
        
            gamesess = GameSession.objects.get(gameid=request.POST.get("id"))
            print("AAAAAAAAAAAwebos", request.POST.get('team1',False))
            if request.POST.get("team1",False):
                currentteam = 0
            else:
                currentteam=1
            if gamesess:
                teams = [gamesess.team1, gamesess.team2]
                people = [gamesess.team1.player1, gamesess.team2.player1,
                        gamesess.team1.player2, gamesess.team2.player2, 
                        gamesess.team1.player3, gamesess.team2.player3,
                        gamesess.team1.player4, gamesess.team2.player4,
                        gamesess.team1.player5, gamesess.team2.player5,]
                current = teams[currentteam]
                if not request.user in people:
                        
                    
                    if not current.player1:
                        current.player1 = request.user
                    elif not current.player2:
                        current.player2 = request.user
                    elif not current.player3:
                        current.player3 = request.user
                    elif not current.player4:
                        current.player4 = request.user
                    elif not current.player5:
                        current.player5 = request.user
                    else:
                        "talleno"
                else:
                    "yasta"
                
                
                

                    
                current.save()
                gamesess.save()
                
                return redirect(reverse('main-game')+f"?id={gamesess.gameid}")
        games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
        
        context = {"games": games}
      
        return render(request, 'main/lobby_game.html', context)

def play(request): #cambiar get por post
    if request.is_ajax and request.method =="GET":
     
        gameid = request.GET.get("id")
        user = request.user

        gamesess = GameSession.objects.get(gameid=request.GET.get("id"))

        if gamesess:
            prevmovs = json.loads(gamesess.moves)
         
            
            current_mov =  len(prevmovs)%2 #leer json
            flag = False
            current_user_play = None
            if current_mov==0:

                
                if user == gamesess.player1:
                    flag = True
                current_user_play = gamesess.player1.username
               
            else:
                if user == gamesess.player2:
                    flag = True
                current_user_play = gamesess.player2.username
                
            if flag and request.GET.get("pos1") and request.GET.get("pos2"):

                pos1,pos2 = [int(x) for x in request.GET.get("pos1")],[int(x) for x in request.GET.get("pos2")]
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs+[(pos1,pos2)])
                if board is True:
                    gamesess.moves = json.dumps(prevmovs+[(pos1,pos2)])
                    if  not gamesess.winner_player:
                        
                            
                        gamesess.winner_player = gamesess.player1 if (len(prevmovs)+1)%2  else gamesess.player2
                        if gamesess.player1 != gamesess.player2:
                            gamesess.winner_player.win_ctd +=1
                            gamesess.winner_player.save()
                    
                    gamesess.isFinished = True
                    gamesess.save()
                    
                    return JsonResponse({"board":shogi.board_state.tolist(),"current_player":gamesess.winner_player.username+" is the winner"})
                
                elif board is False:
                    board = shogi.play_moves(prevmovs)
                else:
                

                    gamesess.moves = json.dumps(prevmovs+[(pos1,pos2)])
                    gamesess.save()
                    print(board)
            else:
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs)

                if board is True:
                    
                    gamesess.isFinished = True
                    if  not gamesess.winner_player:
                        gamesess.winner_player = gamesess.player1 if len(prevmovs)%2  else gamesess.player2
                   
                   
                        if gamesess.player1 != gamesess.player2:
                            gamesess.winner_player.win_ctd +=1
                            gamesess.winner_player.save()                   
                    gamesess.save()
                    return JsonResponse({"board":shogi.board_state.tolist(),"current_player":gamesess.winner_player.username+" is the winner"})
                
                gamesess.moves = json.dumps(prevmovs)
                gamesess.save()
        context = {"board":board.tolist(), "current_player":current_user_play, "current_turn":current_mov}
        return JsonResponse(context)


    elif request.method == "GET":

        context = {
        
        }
    
        return render(request, 'main/lobby_game.html', context)