#!/usr/bin/python3
# -*- coding: utf-8 -*-
from graph_gen import tagMap, tagDets
import math

class PathPlanning(object):

    def __init__(self):
        pass

    def getNode(self, pointer, ctc, goalId, active):
        goalCoord = tagDets[goalId]
        currCoord = tagDets[pointer]
        ctg = math.sqrt(math.pow(goalCoord[0]-currCoord[0],2) + math.pow(goalCoord[1]-currCoord[1],2))
        cth = active[1] + ctc  # new cth je cht parent noda + cost to child
        f = cth + ctg
        node = [pointer, cth, f]
        return node

    def findPath(self, startId, goalId):
        openList = []
        closedList = []
        parentId = []
        path = []
        invalidTurns = []
        cth = 0   
        node = self.getNode(startId, cth, goalId, [0,0])
        node.append(parentId)
        active = node   

        stop = False
        while not stop:
            noDupes = []
            for i in range(len(openList)):
                noDupes.append(openList[i][0])
            numChild = int(len(tagMap[active[0]])/2)
            parentId = active[0]
            pointer = 0
            if numChild > 0:
                for child in range(numChild):
                    childNode = tagMap[active[0]][pointer]
                    if childNode == 0:
                        invalidTurns.append([active[0],pointer])
                    else:
                        cth = tagMap[active[0]][pointer+1]
                        node = self.getNode(childNode, cth, goalId, active)
                        node.append(parentId)
                        if node[0] in noDupes:
                            idx = noDupes.index(node[0])
                            oldF = openList[idx][2]
                            if oldF > node[2]:
                                openList.pop(idx)
                                openList.append(node) 
                        else:
                            openList.append(node) 
                        openList.sort(key=lambda k:k[2])
                    pointer = pointer + 2
            closedList.append(active)
            if not openList:
                stop = True
                print("no route")
                return
            else:
                active = openList.pop(0)
            if active[0] == goalId:
                stop = True
                closedList.append(active)
                closed = closedList[::-1]
                path.append(closed[0][0])
                naslednji = closed[0][3]
                for i in range(len(closedList)):
                    if naslednji == closed[i][0]:
                        if closed[i][0] == startId:
                            path.append(closed[i][0])
                        else:
                            path.append(closed[i][0])
                            naslednji = closed[i][3]

                path = path[::-1]
                return path
        return path

    def generateActions(self, path):
        actions = []
        offRoad = []
        #TODO Convert path to actions here ...
        #action = ('left', 20, 0.202)
        #actions.append(action)
        for i in range(len(path)-1):
            nextIndex = tagMap[path[i]].index(path[i+1])
            if nextIndex == 0:
                direction = 'levo'
            elif nextIndex == 2:
                direction = 'desno'
            else:
                direction = 'Jesus take the wheel'
                goalCoord = tagDets[path[i+1]]
                currCoord = tagDets[path[i]]
                deltaX = goalCoord[0]-currCoord[0]
                deltaY = goalCoord[1]-currCoord[1]
                randomVariableName = [i, (deltaX, deltaY)]
                offRoad.append(randomVariableName)
                print(offRoad)


            nextId = path[i+1]
            distance = tagMap[path[i]][nextIndex+1]
            action = [direction, nextId, distance]
            actions.append(action)
        return actions

if __name__ == '__main__':
  pp = PathPlanning()
  path = pp.findPath(2, 105)
  print(path)
  actions = pp.generateActions(path)
  print(actions)
