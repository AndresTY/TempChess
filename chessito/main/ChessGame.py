import numpy as np
import random
"""
import tensorflow
import keras
import pytorch
import numba
import scipy
import sklearn
import tkinter
import matplotlib
import base64
import hashlib
"""


#Todo:
    # Transform when pawn reaches oposite side
#1 -- King

#3 -- Tower

#5 -- Knight
#6 -- Bishop

#8 -- Pawn
#9 -- Queen

#Winning state is determined with whoever has captured the king, no checkmates or anything.
#Opponent doesnt have to declare a mate if the king is threatened

# "-" for facing upwards.
#Signs will work mostly for direcional purposes
#Need to optimize movement calculations zzz
#Maybe some can be calculated using masks, but eh.
#Not fancy but it works?

class Player():
    def __init__(self, s=1):
        self.pieces = []
        self.s = s #Orientation sign
        self.mov_list = []
     
        
    def pieces_to_str(self):
        mov_dict ={"P":0,
                   "G":0,
                   "S":0,
                   "C":0,
                   "L":0,
                   "B":0,
                   "R":0,
                   
                   }
        
        for piece in self.pieces:
            mov_dict[self.pieces_dict[abs(piece)]]+=1
        a=""
        for i in range(1,len(mov_dict.values())):
            a+=f"{list(mov_dict.values())[i]}{list(mov_dict.keys())[i]}-"
        a = f"{'0'+str(list(mov_dict.values())[0]) if list(mov_dict.values())[0]<10 else list(mov_dict.values())[0] }{list(mov_dict.keys())[0]}-"+a
        return a
            
            
        
        
       
class Chess():
    BOARD_SIZE = 8
    def __init__(self, board_state = None, p1= None, p2 = None):
        self.p1 = p1
        self.p2 = p2
        #DICTIONARY WITH ALL MOVEMENT CHECKS. Some use functions within the class itself just to make it easier
        self.PIECES = {0: lambda pos2, pos1, s: False,
                       #IM SORRY I INVERTED POS1 AND POS2 HERE REMEMBER TO INVER THEM FOR #1 #2
                       1: lambda pos2, pos1, s : pos1 in [(pos2[0] + 1*s,pos2[1] + 1*s),(pos2[0] +1*s ,pos2[1] +0*s ),(pos2[0]+ 0*s ,pos2[1]+1*s ),(pos2[0]-1,pos2[1] -1*s),(pos2[0] -1*s ,pos2[1]+ 0*s ),(pos2[0]+ 0*s,pos2[1] -1*s),(pos2[0] -1*s ,pos2[1]+ 1*s),(pos2[0] -1*s,pos2[1] -1*s)],#FIX STARTING POS NAME
                    
                       
                        6: lambda pos1, pos2,s : pos2 in self.checkBishop(pos1,s=s),#gets a diagonal with respect with pos 1.
                       
                      
                        5: lambda pos1, pos2, s: pos2 in [(pos1[0]+2*s,pos1[1]+1),(pos1[0]-2*s,pos1[1]-1), (-pos1[0]+2*s,pos1[1]-1),(-pos1[0]-2*s,pos1[1]+1),        
                                                (pos1[0]+1,pos1[1]+2*s),(pos1[0]-1,pos1[1]+2*s), (pos1[0]-1,-pos1[1]+2*s),(pos1[0]+1,-pos1[1]+2*s) ],
                        4: lambda pos1, pos2, s: pos2 in [(pos1[0]+ 1*s, pos1[1]+1*s) , (pos1[0]+1*s, pos1[1]-1*s) , (pos1[0]+1*s, pos1[1]+0*s) , (pos1[0]-1*s, pos1[1]-1*s) , (pos1[0]-1*s, pos1[1]+1*s) ],
                       
                       8:  lambda pos1, pos2, s: pos2 in self.checkPawn(pos1,s),
                       7: lambda pos1, pos2, s: pos2 in self.checkLance(pos1, s),
                       3: lambda pos1, pos2, s: pos2 in self.checkTower(pos1, s), #Gets  a cross
                       
                       9: lambda pos1, pos2, s : pos2 in self.checkBishop(pos1, s) or pos2 in self.checkTower(pos1, s)                       }
        self.valid_moves = {0: lambda pos2, pos1, s: False,
                       #IM SORRY I INVERTED POS1 AND POS2 HERE REMEMBER TO INVER THEM FOR #1 #2
                       1: lambda pos2, pos1, s : [(pos2[0] + 1*s,pos2[1] + 1*s),(pos2[0] +1*s ,pos2[1] +0*s ),(pos2[0]+ 0*s ,pos2[1]+1*s ),(pos2[0]-1,pos2[1] -1*s),(pos2[0] -1*s ,pos2[1]+ 0*s ),(pos2[0]+ 0*s,pos2[1] -1*s),(pos2[0] -1*s ,pos2[1]+ 1*s),(pos2[0] -1*s,pos2[1] -1*s)],#FIX STARTING POS NAME
                    
                       
                        6: lambda pos1, pos2,s : self.checkBishop(pos1,s=s),#gets a diagonal with respect with pos 1.
                       
                      
                        5: lambda pos1, pos2, s: [(pos1[0]+2*s,pos1[1]+1),(pos1[0]-2*s,pos1[1]-1), (-pos1[0]+2*s,pos1[1]-1),(-pos1[0]-2*s,pos1[1]+1),        
                                                (pos1[0]+1,pos1[1]+2*s),(pos1[0]-1,pos1[1]+2*s), (pos1[0]-1,-pos1[1]+2*s),(pos1[0]+1,-pos1[1]+2*s) ],
                        4: lambda pos1, pos2, s:  [(pos1[0]+ 1*s, pos1[1]+1*s) , (pos1[0]+1*s, pos1[1]-1*s) , (pos1[0]+1*s, pos1[1]+0*s) , (pos1[0]-1*s, pos1[1]-1*s) , (pos1[0]-1*s, pos1[1]+1*s) ],
                       
                       8:  lambda pos1, pos2, s:  self.checkPawn(pos1,s),
                       7: lambda pos1, pos2, s:  self.checkLance(pos1, s),
                       3: lambda pos1, pos2, s: self.checkTower(pos1, s), #Gets  a cross
                       
                       9: lambda pos1, pos2, s :  self.checkBishop(pos1, s) + self.checkTower(pos1, s)                       }
       
        if board_state == None:
            #Default chess beggining 1state
            self.board_state = np.array([[3,5,6,9,1, 6, 5, 3],
                                         [8 , 8,8 ,8 ,8 ,8 ,8 , 8],
                                         [0 , 0, 0, 0 ,0 ,0 ,0 ,0 ],
                                         [0 ,0 ,0 ,0 , 0, 0, 0, 0],
                                         [0 ,0 ,0 ,0 ,0 , 0, 0, 0],
                                         [0,  0, 0, 0, 0, 0 ,0 ,0 ],
                                         [-8 ,-8 ,-8 ,-8 ,-8 ,-8 ,-8 ,-8 ],
                                         [-3 , -5, -6, -9, -1, -6, -5, -3]])
           
        else:
            self.board_state = board_state



    def pos_in_bounds(self,pos1):
        if pos1[0]<0 or pos1[1]<0:
            return False
        try:
            self.board_state[pos1[0]][pos1[1]]
            return True
        except:
            return False
        
    def checkPawn(self,pos1,s):
        m = []
        if not self.board_state[pos1[0]+s][pos1[1]]:
            m.append((pos1[0]+s,pos1[1]))
        
        if  self.pos_in_bounds([pos1[0]+s,pos1[1]+s])   and np.sign(self.board_state[pos1[0]+s][pos1[1]+s])!=np.sign(s) and self.board_state[pos1[0]+s][pos1[1]+s]!=0:
            m.append((pos1[0]+s,pos1[1]+s))
        if  self.pos_in_bounds([pos1[0]+s,pos1[1]-s])   and np.sign(self.board_state[pos1[0]+s][pos1[1]-s])!=np.sign(s) and self.board_state[pos1[0]+s][pos1[1]-s]!=0:
            m.append((pos1[0]+s,pos1[1]-s))
        print(m)
        return m
        
    def checkBishop(self,pos1,s):
        x= 1
        #This checks all diagonals with respect to the bishop position. If it finds an allied piece, it stops as it cant go further.
        #If an enemy piece is found, its position is added and then it stops, as it cant go further
        mov =[]
        try:
            while (self.board_state[pos1[0]+x][pos1[1]+x] ==0 or np.sign(self.board_state[pos1[0]+x][pos1[1]+x])==-s  )  and x<self.BOARD_SIZE:
                mov.append((x+pos1[0],x+pos1[1]))
                if np.sign(self.board_state[pos1[0]+x][pos1[1]+x]) ==-s:
                    break
               
                x+=1
        except:
            pass
       
   
        x=1
        try:
            while (self.board_state[pos1[0]-x][pos1[1]-x] ==0 or np.sign(self.board_state[pos1[0]-x][pos1[1]-x])==-s )  and x<self.BOARD_SIZE:
                mov.append((-x+pos1[0],-x+pos1[1]))
                if np.sign(self.board_state[pos1[0]-x][pos1[1]-x]) ==-s:
                    break
               
                x+=1
        except:
            pass
        x=1
     
        try:
            while (self.board_state[pos1[0]-x][pos1[1]+x]  ==0 or np.sign(self.board_state[pos1[0]-x][pos1[1]+x])==-s  )  and x<self.BOARD_SIZE:
                mov.append((-x+pos1[0],x+pos1[1]))
                if np.sign(self.board_state[pos1[0]-x][pos1[1]+x]) ==-s:
                    break
               
                x+=1
             
               
             
        except:
            pass
        x=1
   
        try:
            while (self.board_state[pos1[0]+x][pos1[1]-x]  ==0 or np.sign(self.board_state[pos1[0]+x][pos1[1]-x])==-s  )  and x<self.BOARD_SIZE:
                mov.append((x+pos1[0],-x+pos1[1]))
                if np.sign(self.board_state[pos1[0]+x][pos1[1]-x]) ==-s:
                    break
               
                x+=1
             
        except:
            pass
        return mov
   
       
           
   
    def checkTower(self,pos1,s):
        x=1
        mov=[]
        #todo: REMOVE TRY EXCEPT, Add a max pos limit
       
        #Similar to bishop, but instead of doing diagonals it just checks the column and row with respect on the position of the tower
        try:
            while (self.board_state[pos1[0]+x][pos1[1]] ==0 or np.sign(self.board_state[pos1[0]+x][pos1[1]]) ==-s) and x<self.BOARD_SIZE:
                mov.append((pos1[0]+x,pos1[1]))
                if np.sign(self.board_state[pos1[0]+x][pos1[1]]) ==-s:
                    break
               
                x+=1
        except:
            pass
        x=1
        try:
            while (self.board_state[pos1[0]][pos1[1]+x] ==0 or np.sign(self.board_state[pos1[0]][pos1[1]+x]) ==-s) and x<self.BOARD_SIZE:
                mov.append((pos1[0],pos1[1]+x))
                if np.sign(self.board_state[pos1[0]][pos1[1]+x]) ==-s:
                    break
                
                x+=1
        except:
            pass
        x=1
        try:
            while (self.board_state[pos1[0]-x][pos1[1]] ==0 or np.sign(self.board_state[pos1[0]-x][pos1[1]]) ==-s) and x<self.BOARD_SIZE:
                mov.append((pos1[0]-x,pos1[1]))
                if np.sign(self.board_state[pos1[0]-x][pos1[1]]) ==-s:
                    break
               
                x+=1
        except:
            pass
        x=1
        try:
            while (self.board_state[pos1[0]][pos1[1]-x] ==0 or np.sign(self.board_state[pos1[0]][pos1[1]-x]) ==-s) and x<self.BOARD_SIZE:
                mov.append((pos1[0],pos1[1]-x))
                if np.sign(self.board_state[pos1[0]][pos1[1]-x]) ==-s:
                    break
               
                x+=1
            return mov
        except:
            pass
   
   
    def move(self, p, pos1, pos2):
       
        
        if pos2[0] >self.BOARD_SIZE-1 or pos2[1] >self.BOARD_SIZE-1 or pos2[0] <0 or pos2[1] <0: #Checks if pos is out of bounds.
            
            return 0
       
        #Check if piece belongs to player
        if (p==self.p1) and (self.board_state[pos1[0],pos1[1]]<0):
            print("Not your piece")
            return 0
        if (p==self.p2) and self.board_state[pos1[0],pos1[1]]>0 :
            print("Not your piece")
            return 0
        

           
        #Replaces the pos2 with the new piece, and pos1 with a blank space
        try: #REMOVE THIS TRY
            print(self.PIECES[np.abs(self.board_state[pos1[0],pos1[1]])](pos1,pos2,p.s))
            if self.PIECES[np.abs(self.board_state[pos1[0],pos1[1]])](pos1,pos2,p.s) and np.sign(self.board_state[pos1[0],pos1[1]]) != np.sign(self.board_state[pos2[0],pos2[1]]):
                
                if self.board_state[pos2[0],pos2[1]]:
                    p.pieces.append(-self.board_state[pos2[0],pos2[1]])
                self.board_state[pos2[0],pos2[1]] = self.board_state[pos1[0],pos1[1]]
                self.board_state[pos1[0],pos1[1]] = 0
                
                return True
                #print("OK")
               
               
            else:
                
                print("IBREAKHERE",pos1,pos2, self.valid_moves[np.abs(self.board_state[pos1[0],pos1[1]])](pos1,pos2,p.s))
                #print("Not a valid move!")
                return 0
           
        except:
            return 0
   
     

   
    def play_moves(self, moves):
        winner = False
        turns = [self.p1,self.p2]
        x=0
        current = turns[x]
        players = ["PLAYER 1", "PLAYER 2"]
        
        
        #valid = 0
        for m in moves:
            
            pos1 = tuple(m[0])
            pos2 = tuple(m[1])
         
            if not self.move(current, pos1, pos2 ):
                
                return False

                   
            if 1 in self.p1.pieces or -1 in self.p2.pieces:
                winner = 1
                return True
            
               
            x+=1
            current = turns[x%2]
        return self.board_state
