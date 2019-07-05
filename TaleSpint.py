#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##Noelia Navarro an approach for Talespin

import numpy as np
import pandas as pd
import copy
import random


#-----------Define actors set up--------------
#Define what we know from the actors we  create a class for each of the character

class Actor():
        def __init__(self,name,socialRelation,currentFeelingState,food,currentLocation,goal,honest):
            self.__name = name
            self.__socialRelation = socialRelation
            self.__currentFeelingState = currentFeelingState
            self.__food = food 
            self.__currentLocation = currentLocation
            self.__goal = goal
            self.__honest = honest
            self.__inMemoryGoal = [goal]##[[name,goal]]
            print("" + name + "-" + socialRelation + "-" + currentFeelingState + "-" + food + "-" + currentLocation + "-" + str(goal))

       #return properties 
        @property
        def name(self):
            return self.__name
        @property
        def socialRelation(self):
            return self.__socialRelation
        @property
        def currentFeelingState(self):
            return self.__currentFeelingState
        @property
        def food(self):
            return self.__food
        @property
        def currentLocation(self):
            return self.__currentLocation
        @property
        def goal(self):
            return self.__goal       
        @property
        def inMemoryGoal(self):
            return self.__inMemoryGoal 
        @property
        def honest(self):
            return self.__honest 

         
        #set the names   
        @name.setter
        def name(self,name):
            self.__name = name
            
        @socialRelation.setter
        def socialRelation(self,socialRelation):
            self.__socialRelation = socialRelation
            
        @currentFeelingState.setter
        def currentFeelingState(self,currentFeelingState):
            self.__currentFeelingState = currentFeelingState
            
        @food.setter
        def food(self,food):
            self.__food = food
            
        @currentLocation.setter
        def currentLocation(self,currentLocation):
            self.__currentLocation = currentLocation
            
        @goal.setter
        def goal(self,goal):
            self.__goal = goal
            
        @inMemoryGoal.setter
        def inMemoryGoal(self,inMemoryGoal):
            self.__inMemoryGoal = inMemoryGoal           

        @honest.setter
        def honest(self,honest):
            self.__honest = honest   

            

#-----------Define Program class - main execution--------------

class TaleSpin():
    def __init__(self,worldInitialStage, locations):
            self.__initialStage = worldInitialStage
            #self.__inMemoryGoal = []
            #memory to save the story

            self.__inMemory =  self.__initialStage
            self.__storyCharactersList = []
            self.__locations = locations

    #set the properties
    @property
    def initialStage(self):
        return self.__initialStage
    @property
    def inMemory(self):
        return self.__inMemory 
    @property
    def storyCharactersList(self):
        return self.__storyCharactersList
    @property
    def locations(self):
        return self.__locations
    
    
    @initialStage.setter
    def initialStage(self, initialStage):
        self.__initialStage = initialStage  
    @inMemory.setter
    def inMemory(self, inMemory):
        self.__inMemory = inMemory 
    @storyCharactersList.setter
    def storyCharactersList(self, storyCharactersList):
        self.__storyCharactersList = storyCharactersList  
    @locations.setter
    def locations(self, locations):
        self.__locations = locations
        
    #Function create story characters 
    #Defining global characters for the story and setting their properties.
    def createCharacters(self,name,socialRelation,currentFeelingState,food,currentLocation,goal,honest):
        newActor = Actor(name,socialRelation,currentFeelingState,food,currentLocation,goal,honest)
        self.__storyCharactersList.append(newActor)
        
        
    #Function init  to generate the story
    #Starts with adding the goal to the goals' stack and executing the problemSolver
    def createStory(self):
        for i in self.__storyCharactersList:
            newStory = Story(i,self.__inMemory,self.__storyCharactersList,locations)    
        #incluir el print de la historia
 
    
#-----------Class for story building for an character and a goal--------------
#inMemory is reference to the story pipe
class Story():
    def __init__(self,mainActor,inMemory,storyCharactersList,locations):
            self.__actor = mainActor
            inMemory.append(["--------Story starts--------"])
            self.__inMemory = inMemory
            self.__storyCharactersList = storyCharactersList
            self.__locations = locations
           # print(inMemory)
            self.problemSolver()
    
    @property
    def inMemory(self):
        return self.__inMemory 
    @property
    def storyCharactersList(self):
        return self.__storyCharactersList  
    
    @inMemory.setter
    def inMemory(self, inMemory):
        self.__inMemory = inMemory 
        
    @property
    def locations(self):
        return self.__locations
  
    
#-----------Main functions for plan controls--------------
#Function problemSolver       
#executes each plan until one works and the goal
#can be removed, or until none do and the character fails to get the
#goal.  If the goal is already true (and the actor knows that), then
#return success immediately.  If the actor already has the goal,
#then he's in a loop and has failed.  Otherwise, set up the goal and go."    
    def problemSolver(self):
        while  len(self.__actor.inMemoryGoal) > 0:
            print("Execution started")
            print("Main goal " + str(self.__actor.inMemoryGoal))
            self.executePlans()
            if "GOAL NOT ACHIEVED" in self.__inMemory:
                break;      
        self.__inMemory.append(["THE END"])
        print("----------Stack Memory result story -----------------")    
        print(self.__inMemory)
    

#Function executePlans       
#This function executes all plans -actions available to achieve the goal.
    def executePlans(self):
        goal = self.__actor.inMemoryGoal[0][1] 
        lent = len(self.__actor.inMemoryGoal)
        a = self.__actor.inMemoryGoal
        if goal == "thirst":
            self.sigmaThirst()
        if goal == "hungry":
            self.sigmaHunger()
        if goal == "wants to be":
            self.deltaProx()
        if goal == "wants to know about":
            self.deltaKnow()
        if goal == "tells":
            self.deltaTell()
        if goal == "asks info of":
            self.deltaAsk() 
        if goal == "rest":
            self.sigmaRest()
            

#Function assertionMechanism
#assertion controls the effects , consecuences to be apply to the  memory stack of the story state 
#if no mayor consecuence to the principal stack then applies the effects
#consequences do affect the goals stack only adds information to the story stack
    def assertionMechanism(self,consequence,effect):
        result = ""
        if (not consequence):
            if not(not effect):
                self.applyeffect(effect)
        else: 
            for i in consequence:
                self.__inMemory.append(i)
            if not(not effect):
                self.applyeffect(effect)
            
        return result


#Function that reviews current memoryGoal and removes the goal achieved
    def applyeffect(self,goalAchieved):
        response = "not goal achieved"
        goalAchieved1 = copy.deepcopy(goalAchieved)
        goalAchieved1.remove("not")
        positivegoalAchieved = goalAchieved1
        if positivegoalAchieved in self.__actor.inMemoryGoal:
            self.__actor.inMemoryGoal.remove(positivegoalAchieved)
            response =  "goal achieved"  
        return response

#Function to collapse all story and getting one string
        def utilityCollapseString(self,lista):
            result = ''
            for i in lista:
               newString = ' '.join(str(j) for j in i)
               result += (newString + ' ')
            return result
            

#-----------Main planboxes for delta plans ande sigma states --------------
#******Plans to satisfy  sigma states thirst, hunger, rest, hot ***************

#Action sigmaThirst
# To satisfy thirst, go to some water and drink it.
#preconditions: [actor, ' is in', 'river']
#postconditions:
#effects: actor drinks water, actor is not thrist
    def sigmaThirst (self):
        if len(self.__actor.inMemoryGoal) > 0:
            precondition = [self.__actor.name, 'is in', 'river']
            print("Thirst!!!!!")
            #print(goal)
    
            effect = copy.deepcopy(self.__actor.inMemoryGoal[0])
            effect.insert(0,"not")
            print(effect)

            if precondition in self.__inMemory:
               self.assertionMechanism([[self.__actor.name,"knows it is possible to drink","water"],[self.__actor.name,"drinks","water"],effect],effect)
               #print(effect1)

            else: 
                self.__actor.inMemoryGoal.insert(0,[self.__actor.name,"wants to be","river"])
                print("alternate")

#Action sigmaHunger
## To satisfy hunger, you see food, move to the food and eat it.
##preconditions: thre is food in the place the character is per example the bear can see food in the cave his in it
#no body lies to be able to eat
##postconditions:
##effects: [actor, 'can see food', food actor eats]
#           actor eats food, actor is not hungry

    def sigmaHunger (self):
        if len(self.__actor.inMemoryGoal) > 0:
            newgoal = self.__actor.inMemoryGoal[0]
            #if the food is in the same spot of the actor then the actor knows where is the food
            precondition1 = [self.__actor.food, 'is in',self.__actor.currentLocation]
            precondition2 = [self.__actor.name, 'knows', newgoal[2]]
            precondition3 =  [self.__storyCharactersList[1].name, 'lies', self.__actor.name]                               
           
            print("Hungry!!" + str(len(self.__actor.inMemoryGoal)))
            print(self.__actor.currentLocation)
    
            effect = copy.deepcopy(self.__actor.inMemoryGoal[0])
            effect.insert(0,"not")
            if precondition1 in self.__inMemory: 
                if not(precondition3 in self.__inMemory):
                #if the character sees food he likes at his location then eats it
                    self.assertionMechanism([[self.__actor.name, 'knows location of food', self.__actor.food],[self.__actor.name,"eats",self.__actor.food],effect],effect)
                else:
                    self.assertionMechanism([[self.__actor.name, 'dies'],"GOAL NOT ACHIEVED"],[])
            elif precondition2 in self.__inMemory :
                location = self.searchObject(self.__inMemory,newgoal[2])
                moveToLocation = [self.__actor.name, "wants to be", location]
                self.__actor.inMemoryGoal.insert(0,moveToLocation)

            else:
                 self.__actor.inMemoryGoal.insert(0,[self.__actor.name,"wants to know about",self.__actor.food])
                 print("alternate")
 
    
#Action sigmaRest
## To satisfy rest, must eat much.
##preconditions: there is food in the place the character is per example the bear can see food in the cave his in it
##postconditions:[actor, 'full and tired']
##effects: 
                 
    def sigmaRest (self):
        if len(self.__actor.inMemoryGoal) > 0:
            newgoal = self.__actor.inMemoryGoal[0]
            #if the food is in the same spot of the actor then the actor knows where is the food
            precondition1 = [self.__actor.name, 'wants to rest']
            newgoal = [self.__actor.name, 'hungry',self.__actor.food]

            print("Rest!!" + str(len(self.__actor.inMemoryGoal)))
            print(self.__actor.currentLocation)
    
            effect = copy.deepcopy(self.__actor.inMemoryGoal[0])
            effect.insert(0,"not")
            
            if precondition1 in self.__inMemory: 
                self.assertionMechanism([[self.__actor.name, 'resting at', self.__actor.currentLocation]],effect)           
            else:
                self.__actor.inMemoryGoal.insert(0,newgoal)
                self.assertionMechanism([precondition1],[])
    
                
          
#******Delta actions ***************
#Action deltaProx
# To move an object (including yourself) to where some other
#person or object is: get the first object (if not yourself), 
#preconditions: goal of movement  in stack
#postconditions:
#effects:actor moves to requested location, goal completed.
            
    def deltaProx(self):
        if len(self.__actor.inMemoryGoal) > 0:
             newgoal = self.__actor.inMemoryGoal[0]
             print("delta prox")
             print(newgoal)
             if not (newgoal in self.__inMemory):
                  effect = copy.deepcopy(newgoal)
                  effect.insert(0,"not")
                 # self.__actor.inMemoryGoal.insert(0,[self.__actor.name,"wants to know about",self.__actor.food])

                  moveToLocation1 = [self.__actor.name, 'moves to', newgoal[2]]                  
                  moveToLocation2 = [self.__actor.name, 'is in', newgoal[2]]
                  self.__actor.currentLocation = newgoal[2]
                  
                  self.assertionMechanism([moveToLocation1,moveToLocation2],effect) 
             
             

#  To find out something: find a friend to tell you
#precondition actor needAnswer object
#[actor wants to know  objectIs]
                  
    def deltaKnow(self):
        if len(self.__actor.inMemoryGoal) > 0:
             newgoal = self.__actor.inMemoryGoal[0]
            # if not goal inside to know
             if not (newgoal in self.__inMemory):
                  print("delta know")
                  print(newgoal)
                  effect = copy.deepcopy(newgoal)
                  effect.insert(0,"not")
                  print(len(self.__storyCharactersList))
                  if self.__actor.currentLocation == self.__storyCharactersList[1].currentLocation:
                      #to ask to somebody, it needs to be close to the other actor.
                      askActorforInformation = [self.__actor.name, 'asks info of', newgoal[2]]
                      self.__actor.inMemoryGoal.insert(0,askActorforInformation)
                      self.assertionMechanism([],[effect]) 
                  else:
                      moveToLocation1 = [self.__actor.name, "wants to be", self.__storyCharactersList[1].currentLocation]                                  
                      askActorforInformation = [self.__actor.name, 'asks info of', newgoal[2]] 
                      self.__actor.inMemoryGoal.insert(0,askActorforInformation)
                      self.__actor.inMemoryGoal.insert(0,moveToLocation1)                      
                      self.assertionMechanism([],effect) 
                    
#validates if the other actor will cooperate with the information based on the characteristics
    def deltaAsk(self):
        if len(self.__actor.inMemoryGoal) > 0:
             newgoal = self.__actor.inMemoryGoal[0]
            # if not goal inside to know
             if not (newgoal in self.__inMemory):
                  print("delta ask")
                  print(newgoal)
                  effect = copy.deepcopy(newgoal)
                  effect.insert(0,"not")
                  noMorePersecution= False
                  a = self.__actor.socialRelation
                  b = self.__storyCharactersList[1].socialRelation
                  c = self.__actor.currentFeelingState
                  #si su relacion con el actor es buena 
                  if self.__actor.socialRelation == "good" and self.__storyCharactersList[1].socialRelation == "good" and self.__actor.currentFeelingState not in ["furious","physco","deppresive"]:
                      print("Delta Ask1")

                      answer = [self.__actor.name, 'is friend of', self.__storyCharactersList[1].name]
                      tellInformation = [self.__storyCharactersList[1].name, 'tells', newgoal[2]]
                      self.__actor.inMemoryGoal.insert(0,tellInformation)
                      self.assertionMechanism([answer],effect) 

                  #if they are not friends then the second actor will move to other location
                  elif self.__actor.socialRelation == "good" and self.__actor.currentFeelingState in ["depressive","sick"]:
                      print("Delta Ask2")
                      answer = [self.__storyCharactersList[1].name, 'feels sorry for', self.__actor.name]
                      tellInformation = [self.__storyCharactersList[1].name, 'tells', newgoal[2]] 
                      #self.assertionMechanism([],[answer,effect]) 
                      self.__actor.inMemoryGoal.insert(0,tellInformation)
                      self.assertionMechanism([answer],effect) 

                      noMorePersecution= True

                  elif self.__storyCharactersList[1].socialRelation == "bad" and noMorePersecution == False:
                      print("Delta Ask3")
                      scape = random.choice(self.__locations)
                      self.__storyCharactersList[1].currentLocation =  scape
                      self.__actor.currentFeelingState = random.choice(["furious","physco","depressive","sick"])
                      answer1 = [self.__storyCharactersList[1].name, 'runaway far to', scape]
                      answer2 = [self.__actor.name, 'feeling', self.__actor.currentFeelingState]
                      moveToLocation1 = [self.__actor.name, 'wants to be', self.__storyCharactersList[1].currentLocation]
                      self.__actor.inMemoryGoal.insert(0,moveToLocation1)
                      self.assertionMechanism([answer1,answer2],[]) 
                  else:
                      self.__actor.socialRelation = "good"
                      self.assertionMechanism([[self.__actor.name, 'send a gift', self.__storyCharactersList[1].name],[self.__actor.name, 'is friend of', self.__storyCharactersList[1].name]],[]) 

                      
                         
  
#tells the  location of an object if the information is in the story and if it is honest,
#if not  information regarding the object then the actor lies and sets a ramdom location     
    def deltaTell(self):
        if len(self.__actor.inMemoryGoal) > 0:
             newgoal = self.__actor.inMemoryGoal[0]
            # if not goal inside to know
             if not (newgoal in self.__inMemory):
                  print("delta tell")
                  print(newgoal)
                  effect = copy.deepcopy(newgoal)
                  effect.insert(0,"not")        
                  answer1 = [self.__storyCharactersList[1].name, 'tells information', self.__actor.name]                               
                  answer2 = [self.__actor.name, 'knows', newgoal[2]] 
                  objectLocation=""
                  
                  
                  if self.__storyCharactersList[1].honest == True:
                          objectLocation = self.searchObject(self.__inMemory,newgoal[2])
                          
                          if not objectLocation:
                              objectLocation = random.choice(self.__locations)
                              self.__storyCharactersList[1].honest= False
                              answer3 = [newgoal[2], 'is in', objectLocation]
                              answer4 = [self.__storyCharactersList[1].name, 'lies', self.__actor.name]                               
                              self.assertionMechanism([answer1,answer2,answer3,answer4],effect)
                          else:
                            answer3 = [newgoal[2], 'is in', objectLocation]
                            self.assertionMechanism([answer1,answer2,answer3],effect)
                  elif self.__storyCharactersList[1].honest == False:
                      objectLocation = random.choice(self.__locations)
                      self.__storyCharactersList[1].honest= False
                      answer3 = [newgoal[2], 'is in', objectLocation]
                      answer4 = [self.__storyCharactersList[1].name, 'lies', self.__actor.name]                               
                      self.assertionMechanism([answer1,answer2,answer3,answer4],effect)

             else:
                      self.assertionMechanism([answer1,answer2],effect) 

#function that searches for an object in what we know of the story
    def searchObject(self,story,objectToSearch):
        result = []
        for i in story:
            if objectToSearch in i:
                if "is in" in i:
                    result = i[2]
                    
        return result

 


#Example test    
    

worldInitialStage =[['Birdy','home','tree'],
                    ['water','is in','river'],
                    ['honey', 'is in', 'tree'],
                    ['worm','is in','ground'],
                    ['Joe','is in','cave'],
                    ['fish','is in','river'],
                    ['Joe','is a','bear'],
                    ['Joe','home','cave'],
                    ['Birdy','is a','bird'],
                    #['Joe', 'is in', 'river'],
                    ['--------Story starts--------']]
                 #   ['Joe', 'is in', 'river']]
locations = ['cave', 'tree', 'elm-tree', 'ground', 'river']
story1 = TaleSpin(worldInitialStage, locations)

story1.createCharacters("Joe","good","Happy","fish","cave",["Joe","hungry","fish"],True)

story1.createCharacters("Birdy","good","Happy","worm","tree",["Birdy", "thirst","worm"],True)

#story1.createCharacters("Joe","bad","Happy","fish","cave",["Joe","thirst"],True)

story1.createStory()

   



 

    

    
    
 