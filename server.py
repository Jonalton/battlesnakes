import os
import random

import cherrypy

from copy import deepcopy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "jonalton",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        #data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        #data = cherrypy.request.json

        food = self.getFood()
        body = self.getBody()
        head = self.getHead()

        #self.movement(head,body,food)
        
        # Choose a random direction to move in
        
        move = self.movement(head,body,food)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    
    def getHead(self):
      data = cherrypy.request.json
      temp = data.get("you").get("head")
      head = [temp["x"],temp["y"]]
      return head

    def getFood(self):
      data = cherrypy.request.json
      temp = data.get("board").get("food")
      food = []
      for i in temp:
        tList = []
        tList.append(i["x"])
        tList.append(i["y"])
        food.append(tList)
      return food

    def getBody(self):
      data = cherrypy.request.json
      temp = data.get("you").get("body")
      body = []
      for i in temp:
        tList = []
        tList.append(i["x"])
        tList.append(i["y"])
        body.append(tList)
      return body

    def getHeight(self):  
      data = cherrypy.request.json
      height = data.get("board").get("height")
      return height

    def getWidth(self):  
      data = cherrypy.request.json
      width = data.get("board").get("width")
      return width

    def movement(self,head,body,food):
      possible_moves = ["up", "down", "left", "right"]
      move = self.moveToFood(head,food,possible_moves)
      move = self.avoidBodyCollision(head,body,move,possible_moves)
      print("MOVE: ",move)
      move = self.avoidBorder(head,move,possible_moves)
      print("borderMOVE: ",move)
      possible_moves = self.checkAvailableMoves(head,body,possible_moves)
      move = self.confirmMove(move,possible_moves)
      print("possiblemoves",possible_moves)
      print("FINALMOVE: ",move)
      return move

    def confirmMove(self,move,possible_moves):
      #print("poss",possible_moves)
      for i in range(0,len(possible_moves)):
        if (move == possible_moves[i]):
          print("checkmove",move)
          return move
      return possible_moves[0]


    def avoidBodyCollision(self,head,body,move,possible_moves):
      print("FIRST MOVE: ",move)
      print("HEAD: ",head)
      #print("BODY: ", body)
      #for i in range(1,len(body)):
      #print("i: ",i)
      print("BODY: ", body[1])
      move = self.avoidNeck(head,body,move,possible_moves)
      print("MOVENECK",move)
      move = self.avoidTail(head,body,move,possible_moves)
      print("MOVETAIL",move)
        
      return move

    def avoidNeck(self,head,body,move,possible_moves):
      if move == "right" and ((body[1][0]-(1)) == head[0]):   
        print("rightcon")
        return possible_moves[0]
      elif move == "left" and ((body[1][0]+(1)) == head[0]):
        print("leftcon")
        return possible_moves[1]
      elif move == "up" and ((body[1][1]-(1)) == head[1]):
        print("upcon")
        return possible_moves[3]
      elif move == "down" and ((body[1][1]+(1)) == head[1]):
        print("downcon")
        return possible_moves[2]
      return move

    def avoidTail(self,head,body,move,possible_moves):
      for i in range(2,len(body)):
        if move == "right" and (body[i][0] == head[0]+1) and (body[i][1] == head[1]):
          print("Trightcon body: ",body[i][0])
          return possible_moves[1]
        elif move == "left" and (body[i][0] == head[0]-1) and (body[i][1] == head[1]):
          print("Tleftcon body: ",body[i][0])
          return possible_moves[0]
        elif move == "up" and (body[i][1] == head[1]+1) and (body[i][0] == head[0]):
          print("Tupcon body: ",body[i][1])
          return possible_moves[2]
        elif move == "down" and (body[i][1] == head[1]-1) and (body[i][0] == head[0]):
          print("Tdowncon body:",body[i][1])
          return possible_moves[3]
      return move       

    def checkAvailableMoves(self,head,body,possible_moves):
      possible_moves = ["up", "down", "left", "right"]
      #print("POSS_MOVES",possible_moves)
      for i in range(1,len(body)):
        #CHECK IF UP IS FREE
        if body[i][1] == head[1]+1 and body[i][0] == head[0] and ("up" in possible_moves):
          possible_moves.remove("up")
          print("UP BLOCKED")
        elif body[i][1] == head[1]-1 and body[i][0] == head[0] and ("down" in possible_moves):
          possible_moves.remove("down")
          print("DOWN BLOCKED")
        elif body[i][0] == head[0]+1 and body[i][1] == head[1] and ("right" in possible_moves):
          possible_moves.remove("right")
          print("RIGHT BLOCKED")
        elif body[i][0] == head[0]-1 and body[i][1] == head[1] and ("left" in possible_moves):
          possible_moves.remove("left")
          print("LEFT BLOCKED")
      possible_moves = self.checkBorder(head,possible_moves)
      return possible_moves

    def checkBorder(self,head,possible_moves):
      height = self.getHeight()
      width = self.getWidth()
      if width+1 == head[0]+1 and ("right" in possible_moves):
        possible_moves.remove("right")
      elif -1 == head[0]-1 and ("left" in possible_moves):
        possible_moves.remove("left")
      elif height+1 == head[1]+1 and ("up" in possible_moves):
        possible_moves.remove("up")
      elif -1 == head[1]-1 and ("down" in possible_moves):
        possible_moves.remove("down")
      return possible_moves



    def avoidBorder(self,head,move,possible_moves):
      height = self.getHeight()
      width = self.getWidth()
      if move == "right" and ((width+1) == (head[0]+1)):
        return possible_moves[1]
      elif move == "left" and (-1 == (head[0]-1)):
        return possible_moves[0]
      elif move == "up" and ((height+1) == (head[1]+1)):
        return possible_moves[2]
      elif move == "down" and (-1 == (head[1]-1)):
        return possible_moves[3]
      return move
    

    def moveToFood(self,head,food,possible_moves):
      #print("HEAD",head)
      diff = self.calcFoodDist(head,food)
      #print("FOOD",food)
      #print("DIFF",diff)
      tempdiff = deepcopy(diff)
      index = self.getFoodIndex(tempdiff)
      #print("DIFF",diff)
      #print("GOTO",food[index])
      #print("DIFFINDEX",diff[index])
      move = self.getFoodMove(diff,index,possible_moves)
      return move
      
      
    def getFoodMove(self,diff,index,possible_moves):
      if (diff[index][0] == 0 and diff[index][1] < 0):
        #print("MOVE DOWN")
        return possible_moves[1]
      elif (diff[index][0] == 0 and diff[index][1] > 0):
        #print("MOVE UP")
        return possible_moves[0]
      elif (diff[index][0] < 0 and diff[index][1] == 0):
        #print("MOVE LEFT")
        return possible_moves[2]
      elif (diff[index][0] > 0 and diff[index][1] == 0):
        #print("MOVE RIGHT")
        return possible_moves[3]
      elif (diff[index][0] < 0 and diff[index][1] < 0):
        #print("MOVE LEFT OR DOWN")  
        return possible_moves[1]  
      elif (diff[index][0] > 0 and diff[index][1] < 0):
        #print("MOVE RIGHT OR DOWN")
        return possible_moves[3]
      elif (diff[index][0] < 0 and diff[index][1] > 0):
        #print("MOVE LEFT OR UP")
        return possible_moves[2]
      elif (diff[index][0] > 0 and diff[index][1] > 0):
        #print("MOVE RIGHT OR UP")
        return possible_moves[0]

    def getFoodIndex(self,tempdiff):
      for i in range(0,(len(tempdiff))):
        for j in (0,1):
          if tempdiff[i][j] < 0:
            tempdiff[i][j] = tempdiff[i][j] * -1
      sum = []
      for i in range(0,(len(tempdiff))):
        print(tempdiff[i])
        sum.append(tempdiff[i][0]+tempdiff[i][1])
      return sum.index(min(sum))


    def calcFoodDist(self,head,food):
      diff = [] 
      for i in food:
        tList = []
        tList.append(i[0]-head[0])
        tList.append(i[1]-head[1])
        diff.append(tList)
      return diff


    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
