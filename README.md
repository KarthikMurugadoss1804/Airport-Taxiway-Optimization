# Airport Taxiway Optimization
 The goal of this project is to develop and optimize an Integer Linear Programming model to solve airport taxiway optimization
 
 **main.py - Python implementation of the project.** 

## Problem Statement

In this task you will optimise the taxi movements for arriving and departing aircraft moving between runways and terminals. The input data for this task is contained in the Excel file “data.xlsx” and can be downloaded from Canvas. 

The file contains 3 sheets: 
- **Flight schedule** This table outlines the arrival and departure times for all flights of the day. 
- **Taxi distances** This table outlines the taxi distances between the different runways and terminals of the airport. 
- **Terminal capacity** This table shows the gate capacity of each terminal, i.e. how many planes can be present at the terminal at any given time. 

The same runway cannot be occupied at the same time, neither for arrival nor for departure. For example, Flight B departing at 10:00 and flight L arriving at 10:00 cannot be assigned the same runway. Further to that, planes are occupying their allocated gate the whole timespan between arrival and departure during which the gate capacity of the terminal needs to be taken into consideration when allocating terminals. Planes have to taxi from the allocated arrival runway to the allocated terminal and then from the allocated terminal to the allocated departure runway. Arrival and departure runways can be different. The total taxi distance for each flight is the distance from the arrival runway to the allocated terminal and the way back from the terminal to the departure runway. The goal of this task is to develop and optimise an Integer Liner Programming model for allocating an arrival runway, a departure runway and a terminal for each flight so that the overall taxi distance of all planes is minimised. 

## Constraints

- A. Load the input data from the file “Assignment_DA_2_b_data.xlsx” [1 point]. Make sure to use the data from the file in your code, please do not hardcode any values that can be read from the file. 

- B. Identify and create the decision variables for the arrival runway allocation, for the departure runway allocation, and for the terminal allocation using the OR Tools wrapper of the CBC_MIXED_INTEGER_PROGRAMMING solver. 

- C. Define and create auxiliary variables for the taxi movements between runways and terminals for each flight.

- D. Define and implement the constraints that ensure that every flight has exactly two taxi movements.

- E. Define and implement the constraints that ensure that the taxi movements of a flight are to and from the allocated terminal .

- F. Define and implement the constraints that ensure that the taxi movements of a flight include the allocated arrival and departure runways.

- G. Define and implement the constraints that ensure that each flight has exactly one allocated arrival runway and exactly one allocated departure runway

- H. Define and implement the constraints the ensure that each flight is allocated to exactly one terminal

- I. Define and implement the constraints that ensure that no runway is used by more than one flight during each timeslot 

- J. Define and implement the constraints that ensure that the terminal capacities are not exceeded

- K. Define and implement the objective function. Solve the linear program and determine the optimal total taxi distances for all flights. 

- L. Determine the arrival runway allocation, the departure runway allocation, and the terminal allocation for each flight. Also determine the taxi distance for each flight. 

 - M. Determine for each time of the day how many gates are occupied at each terminal.
