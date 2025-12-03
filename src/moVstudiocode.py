"""
hello.py
====================================
This code gives out movie reccomendations

| Author: Katherine
| Date: 2025 Novermber 30
"""

from pdb import set_trace
from pythonds.graphs import PriorityQueue, Graph, Vertex
from https://grouplens.org/datasets/movielens/100k/ import ml-100k as moviesinfo 

import sys

def prim(G,start):
    pq = PriorityQueue()
    for v in G:
        v.setDistance(sys.maxsize)
        v.setPred(None)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(),v) for v in G])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
          newCost = currentVert.getWeight(nextVert)
          if nextVert in pq and newCost<nextVert.getDistance():
              nextVert.setPred(currentVert)
              nextVert.setDistance(newCost)
              pq.decreaseKey(nextVert,newCost)
    

def ratings(movieratings):
    #defines how the movies are rated and weighted
    dostuff = 1
    for i in movieratings


if __name__=="__main__":
    choice = input("What movie do you like")
    prim(choice)

    print("Here is a list of reccomended movies based on the movie you liked")
    print(f'->{choice.prim()}', end ='->')