# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:33:08 2020

@author: karth
"""

from ortools.linear_solver import pywraplp
import pandas as pd
# A. Loading the input data
flight_sched = pd.read_excel("Assignment_DA_2_b_data.xlsx", sheet_name = "Flight schedule", index_col=0 , dtype = 'str')
taxi_distance = pd.read_excel("Assignment_DA_2_b_data.xlsx", sheet_name = "Taxi distances", index_col=0)
term_cap = pd.read_excel("Assignment_DA_2_b_data.xlsx", sheet_name = "Terminal capacity", index_col=0)
flights = list(flight_sched.index)
print(len(flights))
runways = list(taxi_distance.index)
print(runways)
terminals = list(taxi_distance.columns)
print(terminals)
arrival_timeslots = set(flight_sched['Arrival'].to_list())
departure_timeslots = set(flight_sched['Departure'].to_list())
all_timeslots = arrival_timeslots.union(departure_timeslots)

# B. Creating the decision variables  

solver = pywraplp.Solver('part2',
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
# Arrival Runway allocation and Departure runway allocation

arrival_allocation = {}
departure_allocation = {}
for flight in flights:
    for runway in runways:
        arrival_allocation[(flight, runway)] = solver.IntVar(0, 1, "Arrival"+flight+"_"+runway)
        departure_allocation[(flight, runway)] = solver.IntVar(0, 1,  "Departure"+flight+"_"+runway)
     

# Terminal allocation 
terminal_allocation = {}
for terminal in terminals:
    for flight in flights:
        terminal_allocation[(terminal, flight)] = solver.IntVar(0, 1, terminal+"_"+flight)

# C. Auxilary Variable for taxi movements
runway_terminal = {}
terminal_runway = {}

for flight in flights:
    for runway in runways: 
        for terminal in terminals:
        
            runway_terminal[(flight,runway,terminal)] = solver.IntVar(0, 1, "arrival"+flight+"_"+runway+"_"+terminal)
            terminal_runway[(flight,runway,terminal)] = solver.IntVar(0, 1, "departure"+flight+"_"+runway+"_"+terminal)
# Auxilary variable for flight_time

arrival_time = {}
departure_time = {}

for time in all_timeslots:
    for flight in flights:
        
        if flight_sched.loc[flight]['Arrival'] == time:
            arrival_time[(time, flight)] = 1
        else:
            arrival_time[(time, flight)] = 0
            
        if flight_sched.loc[flight]['Departure'] == time:
            departure_time[(time, flight)] = 1
        else:
            departure_time[(time, flight)] = 0 
        
    
## D. every flight has exactly two taxi movements

for flight in flights:
    solver.Add(solver.Sum(runway_terminal[(flight,runway,terminal)] for runway in runways for terminal in terminals) ==1)
    solver.Add(solver.Sum(terminal_runway[(flight,runway,terminal)] for runway in runways for terminal in terminals) ==1)
    
# E. taxi movements of a flight are to and from the allocated terminal

for flight in flights:
    
    for terminal in terminals:
        # flight A terminal A = 0 ==> 0
        c = solver.Constraint(0,0)
        c.SetCoefficient(terminal_allocation[(terminal, flight)] , -1)
        for runway in runways:
            c.SetCoefficient(runway_terminal[(flight, runway, terminal)], 1)
for flight in flights:
    
    for terminal in terminals:
        c = solver.Constraint(0, 0)
        c.SetCoefficient(terminal_allocation[(terminal, flight)] , 1)
        for runway in runways:
            c.SetCoefficient(terminal_runway[(flight, runway, terminal)], -1)


# F. taxi movements of a flight include the allocated arrival and departure runways

for flight in flights:
    for runway in runways:
        c = solver.Constraint(0,0)
        c.SetCoefficient(arrival_allocation[(flight, runway)], -1)
        for terminal in terminals:
            c.SetCoefficient(runway_terminal[(flight,runway,terminal)], 1)

            
for flight in flights:
    for runway in runways:
        c = solver.Constraint(0,0)
        c.SetCoefficient(departure_allocation[(flight, runway)], -1)
        for terminal in terminals:
            c.SetCoefficient(terminal_runway[(flight,runway,terminal)],1)


# G. each flight has exactly one allocated arrival runway and exactly one allocated departure runway
for flight in flights:
    solver.Add(sum(arrival_allocation[(flight,runway)] for runway in runways) == 1)
    solver.Add(sum(departure_allocation[(flight,runway)] for runway in runways) == 1)

# H. each flight is allocated to exactly one terminal
    
    solver.Add(sum(terminal_allocation[(terminal, flight)] for terminal in terminals) == 1)
   

## I. no runway is used by more than one flight during each timeslot

for runway in runways:
    for time in all_timeslots:
        c = solver.Constraint(0,1)
        for flight in flights:
            c.SetCoefficient(arrival_allocation[(flight,runway)] , arrival_time[(time, flight)])
            c.SetCoefficient(departure_allocation[(flight,runway)] , departure_time[(time, flight)])

### constraints that ensure terminal capacities are not exceeded

for terminal in terminals:
    for time in all_timeslots:
        c = solver.Constraint(0, int(term_cap.loc[terminal]['Gates']))
        for flight in flights:
            if flight_sched.loc[flight]['Departure'] > time and flight_sched.loc[flight]['Arrival'] <= time:
                c.SetCoefficient(terminal_allocation[(terminal, flight)] , 1)
            else:
                c.SetCoefficient(terminal_allocation[(terminal, flight)] , 0)
    
# Solve the objective function 
                    
total_taxi = solver.Objective()
for flight in flights:
    for runway in runways:
        for terminal in terminals:
            total_taxi.SetCoefficient( runway_terminal[(flight,runway,terminal)]  , int(taxi_distance.loc[runway][terminal]))
            total_taxi.SetCoefficient( terminal_runway[(flight,runway,terminal)]  , int(taxi_distance.loc[runway][terminal]))

total_taxi.SetMinimization()
status = solver.Solve()
            
if status == pywraplp.Solver.OPTIMAL:
    print("Optimal Solution Found")
    print(" Optimal Taxi Distance: ",solver.Objective().Value())
    print("\nAllocation Details for Flights")
    for flight in flights:
        print("\n",flight)
        for terminal in terminals:
            if terminal_allocation[(terminal, flight)].solution_value() >0:
                print("    Allocated ",terminal)
        print("  Taxi Movements")
        t_dist = 0
        for runway in runways: 
            for terminal in terminals:
                if runway_terminal[(flight,runway,terminal)].solution_value() > 0:
                    print("    ", runway, " to ", terminal)
                    t_dist += taxi_distance.loc[runway][terminal]
                if terminal_runway[(flight,runway,terminal)].solution_value() > 0:
                    print("    ", terminal, " to ", runway)
                    t_dist += taxi_distance.loc[runway][terminal]
        print("  Taxi Distance: ", t_dist)
        print("  Runway Allocation")
        for runway in runways:
            if arrival_allocation[(flight, runway)].solution_value() > 0 :
                print("    Arrival at ", runway)
            if departure_allocation[(flight, runway)].solution_value() > 0 :
                print("    Departure at ", runway)
#    print("Runway Allocation Check :")
#    for time in all_timeslots:
#        print(time)
#        for runway in runways:
#            print("  ",runway)
#            for flight in flights:
#                 
#                if arrival_allocation[(flight, runway)].solution_value() == 1 and arrival_time[(time, flight)] == 1 :
#                    print("    ",flight)
#                elif departure_allocation[(flight, runway)].solution_value() ==1 and departure_time[(time, flight)] ==1:
#                    print("    ",flight)
    print("Terminal Gate Allocation Count : ")
    for time in all_timeslots:
        print(time)
        for terminal in terminals:
            print("  ",terminal)
            gates_taken = 0
            for flight in flights:
                 
                if terminal_allocation[(terminal, flight)].solution_value() == 1 and flight_sched.loc[flight]['Departure'] > time and flight_sched.loc[flight]['Arrival'] <= time:
                    gates_taken += 1
            print("     Gates Occupied: ", gates_taken)
    
