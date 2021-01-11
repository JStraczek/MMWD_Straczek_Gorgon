# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:38:00 2021

@author: Jasiek
"""


import random
import sys
import numpy as np
#from enum import Enum
import math

inf = sys.maxsize

class Order():
    A = (0, 'A')
    a = (1, 'a')
    B = (2, 'B')
    b = (3, 'b')
    C = (4, 'C')
    c = (5, 'c')
    
class Solver1:
    
    T0 = 30 # initial temperature
    Tmin = 10 # minimal temperature
    k = 2 # number of iteration per era
    alpha = 0.5 # cooling coefficient
    
    max_prohibited_solutions=300
    
    backpack_volume=3 # backpack volume
    
    c_orders = [Order.A, Order.B] #points of collect
    d_orders = [Order.a, Order.b] #points of deliver
    
    Xa = [Order.A, Order.a, Order.B, Order.b] # initial solution(route)

    cost_matrix = np.array(
               [[inf, 10, 5, 15],
                [inf, inf, 5, 5],
                [5, 5, inf, 10],
                [15, 5, inf, inf]]) #bardziej wlasciwa nazwa to time matrix
    
    penalties_matrix= np.array(
                   [[0, 10, 10],
                    [10, 20, 5],
                    [20, 30, 0],
                    [30, 40, -10],
                    [40, 50, -25],
                    [50, inf, -inf]], dtype=object) #bardziej wlasciwa nazwa to cost matrix
    
    def create_init_solution(self):
        c_order=self.c_orders
        d_order=self.d_orders
        start_point=random.randint(0, len(c_order)-1)
        x_init=[c_order[start_point]]
        backpack=[d_order[start_point]]
        c_order.remove(c_order[start_point])
        while len(c_order)!=0 or len(d_order)!=0:
            if len(backpack)<self.backpack_volume:
                if random.randint(0,1)==0: #tutaj dodamy do sciezki restauracje
                    if len(c_order)!=0:
                        next_point=0
                        if len(c_order)>1:
                            next_point=random.randint(0, len(c_order)-1)
                        print('next',next_point)
                        x_init.append(c_order[next_point])
                        backpack.append(d_order[next_point])
                        c_order.remove(c_order[next_point])
                elif len(backpack)>0: #tutaj dodamy do sciezki klienta
                    next_point=0
                    if len(backpack)>1:
                        next_point=random.randint(0, len(backpack)-1)
                    x_init.append(backpack[next_point])
                    backpack.remove(backpack[next_point])
            else:#musimy dodac do sciezki klienta bo plecak jest pelny
                next_point=random.randint(0, len(backpack)-1)
                x_init.append(backpack[next_point])
                backpack.remove(backpack[next_point])
        print(x_init)
        return x_init
    
    def check_solution(self, trace):
        total_time=self.calculate_total_time(trace)
        if total_time>50:
            return False #prohibited_soultion
        return True
    
    def calculate_total_time(self, trace):
        time=0
        prev_point=trace[0]
        for point in trace[1:]:
            time+=self.cost_matrix[prev_point[0],point[0]]
            prev_point=point
        return time
    
    def cost_function(self, route):
        cost = 0
        time = 0
        prev_point=route[0]
        for point in route[1:]:
            time+=self.cost_matrix[prev_point[0],point[0]]
            if point[0]%2==0:
                print("odebrano zamowienie",point)
            else:
                print("dostarczono zamowienie",point)
                for case in self.penalties_matrix:
                    if case[0] < time <= case[1]:
                        cost+= case[2] * (1)
        print(cost)
        return cost
    
    def calculate_order_cost(self, order, Xa): # returns order realisation cost based on solution Xa
        cost = 0
        for i in range(1, len(Xa)):
            cost += self.calculate_traverse_cost(Xa[i-1], Xa[i])
            print('cost',cost)
            if Xa[i][1] == order[1].lower():
                break
        return cost    
    
    def simulated_annealing(self):
        T = self.T0
        
        #x_init=self.Xa #TODO switch lines
        x_init=self.create_init_solution()#self.c_orders,self.d_orders)
        limiter=0
        while not self.check_solution(x_init): #uncomment after finisishing create ini solution
            x_init=self.create_init_solution(self.c_orders,self.d_orders)
            if limiter==self.max_prohibited_solutions:
                print("program nie moze osiagnac dopuszczolnego rozwiazana")
            else:
                limiter+=1
        
        x_star = x_init
        while T > self.Tmin:
            for it in range(self.k):
                x_n=x_star
                while not self.check_solution(x_n):
                    #x_n=zmiana w rozwiazaniu
                    limiter=0
                    if limiter==self.max_prohibited_solutions:
                        print("program nie moze osiagnac dopuszczolnego rozwiazana")
                    else:
                        limiter+=1
                        
                delta = self.cost_function(x_n) - self.cost_function(x_star)
                
                if delta > 0:
                    x_star=x_n
                else:       
                    r = random.random()
                    if r < math.exp(-delta/T):
                        x_star = x_n
            T *= self.alpha
        
            
#Xa = [Order.A, Order.a, Order.B, Order.b] # initial solution(route)
solver = Solver1()
solver.simulated_annealing()
