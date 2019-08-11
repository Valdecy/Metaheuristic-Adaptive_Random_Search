# Metaheuristic-Adaptive_Random_Search
Adaptive Random Search to Minimize Functions with Continuous VariablesThe function returns: 1) An array containing the used value(s) for the target function and the output of the target function f(x). For example, if the function f(x1, x2) is used, then the array would be [x1, x2, f(x1, x2)].  

* solutions = The population size. The Default Value is 5.

* min_values = The minimum value that the variable(s) from a list can have. The default value is -5.

* max_values = The maximum value that the variable(s) from a list can have. The default value is  5.

* step_size_factor = The variation (increase or decrease) of each step. The Default Value is 0.05.

* factor_1 = The variation (increase or decrease) of each large step in the large_step_threshold. The Default Value is 3.

* factor_2 = The variation (increase or decrease) of each large step out the large_step_threshold. The Default Value is 1.5.

* large_step_threshold = Range of the large step iterations. The Default Value is 10.

* improvement_threshold. Range of iterations used without decreasing the size steps. The Default Value is 25.

* iterations = The total number of iterations. The Default Value is 50.

* target_function = Function to be minimized.
