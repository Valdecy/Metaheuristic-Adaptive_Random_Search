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
import numpy  as np
import math
import copy
import random
import os

# Function
def target_function():
    return

# Function: Initialize Variables
def initial_position(solutions = 5, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    position = np.zeros((solutions, len(min_values) + 1))
    for i in range(0, solutions):
        for j in range(0, len(min_values)):
             position[i,j] = random.uniform(min_values[j], max_values[j])
        position[i,-1] = target_function(position[i,0:position.shape[1]-1])
    return position

# Function: Steps
def step(position, min_values = [-5,-5], max_values = [5,5], step_size = [0,0], target_function = target_function):
    position_temp = np.copy(position)
    for i in range(position.shape[0]):
        for j in range(position.shape[1]-1):
            minimun = min(min_values[j], position[i,j] + step_size[i][j])
            maximum = max(max_values[j], position[i,j] - step_size[i][j])
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1) 
            position_temp[i, j] = np.clip(minimun + (maximum - minimun)*rand, min_values[j], max_values[j]) 
        position_temp[i,-1] = target_function(position_temp[i,0:position_temp.shape[1]-1]) 
    return position_temp

# Function: Large Steps
def large_step(position, min_values = [-5,-5], max_values = [5,5], step_size = [0,0], count = 0, large_step_threshold = 10, factor_1 = 3, factor_2 = 1.5, target_function = target_function):
    factor = 0
    position_temp = np.copy(position)
    step_size_temp = copy.deepcopy(step_size)
    for i in range(position.shape[0]):
        if (count > 0 and count % large_step_threshold == 0):
            factor = factor_1
        else:
            factor = factor_2
        for j in range(0, len(min_values)):
            step_size_temp[i][j] = step_size[i][j]*factor
    for i in range(position.shape[0]):
        for j in range(position.shape[1]-1):
            minimun = min(min_values[j], position[i,j] + step_size[i][j])
            maximum = max(max_values[j], position[i,j] - step_size[i][j])
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1) 
            position_temp[i, j] = np.clip(minimun + (maximum - minimun)*rand, min_values[j], max_values[j])                
        position_temp[i,-1] = target_function(position_temp[i,0:position_temp.shape[1]-1]) 
    return step_size_temp, position_temp 

# ARS Function
def adaptive_random_search(solutions = 5, min_values = [-5,-5], max_values = [5,5], step_size_factor = 0.05, factor_1 = 3, factor_2 = 1.5, iterations = 50, large_step_threshold = 10, improvement_threshold = 25, target_function = target_function):    
    count = 0
    threshold = [0]*solutions
    position = initial_position(solutions = solutions, min_values = min_values, max_values = max_values, target_function = target_function)
    best_solution = np.copy(position[position[:,-1].argsort()][0,:])
    step_size = []
    for i in range(0, position.shape[0]):
        step_size.append([0]*len(min_values))
        for j in range(0, len(min_values)):
            step_size[i][j] = (max_values[j] - min_values[j])*step_size_factor
    while (count <= iterations):       
        print("Iteration = ", count, " f(x) = ", best_solution[-1])
        position_step = step(position, min_values = min_values, max_values = max_values, step_size = step_size, target_function = target_function)
        step_large, position_large_step = large_step(position, min_values = min_values, max_values = max_values, step_size = step_size, count = count, large_step_threshold = large_step_threshold, factor_1 = factor_1, factor_2 = factor_2, target_function = target_function)
        for i in range(position.shape[0]):
            if(position_step[i,-1] < position[i,-1] or position_large_step[i,-1] < position[i,-1]):
                if(position_large_step[i,-1] < position_step[i,-1]):
                    position[i,:] = np.copy(position_large_step[i,:])
                    for j in range(0, position.shape[1] -1):
                       step_size[i][j] = step_large[i][j]
                else:
                    position[i,:] = np.copy(position_step[i,:]) 
                threshold[i] = 0
            else:
                threshold[i] = threshold[i] + 1
            if (threshold[i] >= improvement_threshold):
                threshold[i] = 0
                for j in range(0, len(min_values)):
                    step_size[i][j] = step_size[i][j]/factor_2                       
        if(best_solution[-1] > position[position[:,-1].argsort()][0,-1]):
            best_solution = np.copy(position[position[:,-1].argsort()][0,:])
        count = count + 1        
    print(best_solution)    
    return best_solution, position

######################## Part 1 - Usage ####################################

# Function to be Minimized (Six Hump Camel Back). Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def six_hump_camel_back(variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

ars = adaptive_random_search(solutions = 50, min_values = [-5,-5], max_values = [5,5], step_size_factor = 0.05, factor_1 = 3, factor_2 = 1.5, iterations = 15000, large_step_threshold = 10, improvement_threshold = 25, target_function = six_hump_camel_back)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

ars = adaptive_random_search(solutions = 100, min_values = [-5,-5], max_values = [5,5], step_size_factor = 0.05, factor_1 = 3, factor_2 = 1.5, iterations = 1000, large_step_threshold = 15, improvement_threshold = 25, target_function = rosenbrocks_valley)
