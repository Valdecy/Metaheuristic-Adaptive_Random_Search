############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Random Search

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Random_Search, File: Python-MH-Random Search.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Random_Search>

############################################################################

# Required Libraries
import pandas as pd
import numpy  as np
import math
import copy
import random
import os

# Function: Initialize Variables
def initial_position(solutions = 5, min_values = [-5,-5], max_values = [5,5]):
    position = pd.DataFrame(np.zeros((solutions, len(min_values))))
    position['Fitness'] = 0.0
    for i in range(0, solutions):
        for j in range(0, len(min_values)):
             position.iloc[i,j] = random.uniform(min_values[j], max_values[j])
        position.iloc[i,-1] = target_function(position.iloc[i,0:position.shape[1]-1])
    return position

# Function: Steps
def step(position, min_values = [-5,-5], max_values = [5,5], step_size = [0,0]):
    position_temp = position.copy(deep = True)
    for i in range(position.shape[0]):
        for j in range(position.shape[1]-1):
            minimun = min(min_values[j], position.iloc[i,j] + step_size[i][j])
            maximum = max(max_values[j], position.iloc[i,j] - step_size[i][j])
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            position_temp.iloc[i,j] = minimun + (maximum- minimun)*rand
            if (position_temp.iloc[i,j] > max_values[j]):
                position_temp.iloc[i,j] = max_values[j]
            elif (position_temp.iloc[i,j] < min_values[j]):
                position_temp.iloc[i,j] = min_values[j]                
        position_temp.iloc[i,-1] = target_function(position_temp.iloc[i,0:position_temp.shape[1]-1]) 
    return position_temp

# Function: Large Steps
def large_step(position, min_values = [-5,-5], max_values = [5,5], step_size = [0,0], threshold = [0,0], large_step_threshold = 10, factor_1 = 3, factor_2 = 1.5):
    factor = 0
    position_temp = position.copy(deep = True)
    step_size_temp = copy.deepcopy(step_size)
    for i in range(position.shape[0]):
        if (threshold[i] > 0 and threshold[i] % large_step_threshold == 0):
            factor = factor_1
        else:
            factor = factor_2
        for j in range(0, len(min_values)):
            step_size_temp[i][j] = step_size[i][j]*factor
    for i in range(position.shape[0]):
        for j in range(position.shape[1]-1):
            minimun = min(min_values[j], position.iloc[i,j] + step_size_temp[i][j])
            maximum = max(max_values[j], position.iloc[i,j] - step_size_temp[i][j])
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            position_temp .iloc[i,j] = minimun + (maximum- minimun)*rand
            if (position_temp .iloc[i,j] > max_values[j]):
                position_temp .iloc[i,j] = max_values[j]
            elif (position_temp .iloc[i,j] < min_values[j]):
                position_temp .iloc[i,j] = min_values[j]                
        position_temp .iloc[i,-1] = target_function(position_temp .iloc[i,0:position_temp .shape[1]-1]) 
    return step_size_temp, position_temp 

# ARS Function
def adaptive_random_search(solutions = 5, min_values = [-5,-5], max_values = [5,5], step_size_factor = 0.05, factor_1 = 3, factor_2 = 1.5, iterations = 50, large_step_threshold = 10, improvement_threshold = 25):    
    count = 0
    threshold = [0]*solutions
    position = initial_position(solutions = solutions, min_values = min_values, max_values = max_values)
    best_solution = position.iloc[position['Fitness'].idxmin(),:]
    step_size = []
    for i in range(0, position.shape[0]):
        step_size.append([0]*len(min_values))
        for j in range(0, len(min_values)):
            step_size[i][j] = (max_values[j] - min_values[j])*step_size_factor
    while (count <= iterations):
        
        print("Iteration = ", count, " f(x) = ", best_solution[-1])
        position_step = step(position, min_values = min_values, max_values = max_values, step_size = step_size)
        step_large, position_large_step = large_step(position, min_values = min_values, max_values = max_values, step_size = step_size, threshold = threshold, large_step_threshold = large_step_threshold, factor_1 = factor_1, factor_2 = factor_2)
        for i in range(position.shape[0]):
            if(position_step.iloc[i,-1] < position.iloc[i,-1] or position_large_step.iloc[i,-1] < position.iloc[i,-1]):
                if(position_large_step.iloc[i,-1] < position_step.iloc[i,-1]):
                    for j in range(0, position.shape[1]):
                        position.iloc[i,j] = position_large_step.iloc[i,j]
                    for j in range(0, position.shape[1] -1):
                       step_size[i][j] = step_large[i][j]
                else:
                    for j in range(0, position.shape[1]):
                        position.iloc[i,j] = position_step.iloc[i,j]  
                threshold[i] = 0
            else:
                threshold[i] = threshold[i] + 1
            if (threshold[i] >= improvement_threshold):
                threshold[i] = 0
                for j in range(0, len(min_values)):
                    step_size[i][j] = step_size[i][j]/factor_2
                        
        if(position.iloc[position['Fitness'].idxmin(),-1] < best_solution[-1]):
            for j in range(0, position.shape[1]):
                best_solution[j] = position.iloc[position['Fitness'].idxmin(),j]
        count = count + 1
        
    print(best_solution)    
    return best_solution

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

ars = adaptive_random_search(solutions = 15, min_values = [-5,-5], max_values = [5,5], step_size_factor = 0.05, factor_1 = 3, factor_2 = 1.5, iterations = 1000, large_step_threshold = 10, improvement_threshold = 25)
