# ROADRUNNER
Renewable energy system robust design Optimization AnD unceRtainty qUaNtificatioN framEwoRk

## The models
In the TestCase (TC) folder, you find the available energy models to evaluate.
Currently, a photovoltaic-battery system model is available, for which the capacity of the photovoltaic array, battery stack, DC-DC converter for the photovoltaic array and DC-DC converter for the battery stack are the design variables.
For every design, the Levelized Cost Of Electricity and Self-sufficiency Ratio are quantified for a dwelling. A typical day for electricity demand, solar irradiance and ambient temperature are used to evaluate a typical system lifetime.
Five locations are available to evaluate, which differentiate based on their demand and climate data:
- Athens
- Brussels
- Madrid
- Oslo
- Warschau

Uncommon libraries that are required to run the models:
- rainflow
- pyDOE
- deap



### Set-up
In the folder of your model (e.g. ...\TC\PV_BAT_BRUSSELS), you will set the design variable ranges, the values for the model parameters and the configuration of the optimizer.   

#### designSpace and designSpace_UQ
In this file, you define the model parameters which need a quantification in your model. This consists of both model parameters and design parameters. The design parameters are controllable by the designer, hence a range of possibilities for these variables should be defined (i.e. design of experiments). To define a design variable, the set-up in the designSpace file is as follows:
name type_parameter type_value min max\
where:
1. name: name of the parameter/variable;
2. type_parameter: variable (var);
3. type_value: integer (int) or real value (real);
4. min: minimum of the range (in the case of PV_BAT, a value >0 should be selected e.g. 1e-8);
5. max: maximum of the variable range. 

An example of a configured design variable is:\
n_pv var real 1e-8 50

A model parameter will remain fixed in a deterministic optimization. You can set the value of this parameter in this file. In a later stage, this parameter can be subjected to uncertainty. Therefore, these fixed parameters are defined like this, as opposed to directly defining them in the model. The configuration of a model parameter is similar than for a design variable:\
name type_parameter type_value value\
where:
1. name: name of the parameter/variable;
2. type_parameter: parameter (par);
3. type_value: integer (int) or real value (real);
4. parameter value (or mean of the parameter).

An example of a configured design variable is:\
opex_dcdc par real 0.03

An example of a configured design space:\
par_1 par real 4\
par_2 par real 2.5\
par_3 par real 175\
design_var_1 var real 1 3\
design_var_2 var real 1e-8 100

When considering Uncertainty Quantification, there are no design variables. Instead, the previous design variables should be fixed with a value. Therefore, create a "designSpace_UQ" file, which consists of a (the same) list of parameters, and the design variables replaced by parameters:
design_var_1 var real 1 3
==>
design_var_1 par real 2

#### U and U_UQ
For robust optimization and uncertainty quantification, several parameters should be subjected to uncertainty. This uncertainty can be allocated through the file "U". For every design variable and model parameter defined in designSpace (or designSpaceUQ), an uncertainty can be defined.
Defining the uncertainty of a parameter can be done through the following syntax:\
name type_parameter type_value type_uncertainty distribution value\
where:
1. name: name of the parameter/variable;
2. type_parameter: parameter (par);
3. type_value: integer (int) or real value (real);
4. type_uncertainty: absolute (absolute) or relative (relative) uncertainty;
5. distribution: The distribution of the uncertainty (uniform or Gaussian);
6. value: Value of uncertainty. When uniform (uniform), the value indicates the minimum and maximum value ([mean-value,mean+value]), when Gaussian (Gaussian), the value indicates the standard deviation.

An example of a configured uncertainty:\
par_1 par real absolute uniform 30

Also the design variables can be allocated with uncertainty:\
design_var_1 var real absolute Gaussian 1

Not every parameter or variable in designSpace needs to be allocated with uncertainty.

When considering Uncertainty Quantification, there are no design variables. Instead, the previous design variables should be fixed with a value. Therefore, create a "U_UQ" file, which consists of a (the same) list of parameters, and the design variables replaced by parameters:
var_1 var real absolute uniform 30
==>
var_1 par real absolute uniform 30


#### UserConfig
In this file, the configuration of the NSGA2 optimizer can be done. Additionally, the number of processes that will be performed in parallel (nProcs) can be defined. Usually, this number should be equal or half of the number of cores available on your machine.

## (robust) optimization

### initiation
The optimization can be initiated in run_optimization.py.\ 
In this script, you can define the main parameters for the optimization:

1. 'run mode': 'BENCH' for benchmarking cases, 'ENG' for (engineering) models introduced by the user;
2. 'case': the name of the folder where the case is defined which you want to optimize (in ...\TC\);
3. 'objectives': First, define if deterministic ('det') or robust ('rob') optimization is performed. Then, determine if the objectives need to be maximized or minimized. In this tuple, 1. indicates maximization, -1. indicates minimization, and the position of the value corresponds to the position of the parameter in the output of the model.\
To illustrate, if the model generates two outputs:\
y1, y2 = model(X)\
And the aim is to maximize the first output, but to minimize the second output in a deterministic optimization:\
'objectives':       {'det': (1.,-1.)}\
In a robust optimization, the first objective is the mean, and the second one corresponds to the standard deviation. The standard deviation needs to be minimized, while the mean can be maximized or minimized (depending on the value), e.g. minimization of both objectives is triggered by:\
'objectives':       {'rob': (-1.,-1.)}
4. 'optimizer': Define the optimizer, currently only 'NSGA2';
5. 'population number': The population size for NSGA2;
6. 'stop': Stopping criterium based on the computational budget (i.e. number of model evaluations possible, 'BUDGET'). e.g. ('BUDGET', 1000);
7. 'opt config': use 'DEFAULT' for default condiguration of optimizer, otherwise provide different configuration in 'UserConfig';
8. 'x0': 'AUTO' for automatic generation of design of experiments in 2 ways: 'RAND' for random sampling; 'LHS' for Latin Hypercube Sampling;
9. 'start from last gen': Set to True if you want to start from the last generation, achieved in a previous run. False if you start with no previous information.

When robust optimization is selected, the following parameters should be determined for Polynomial Chaos Expansion (PCE):
10. 'pol_order': The polynomial order for the PCE;
11. 'PCE method': 'OLS' for Ordinary Least Squares method with a full PCE, 'stepwise' for the sparse PCE;
12. 'n_samples': When sparse PCE is selected, set the number of samples for constructing the PCE;
13. 'sampling_method': method for sampling the samples for model evaluation. currently only 'Random';
14. 'objective_names': The names of the model outputs. Mainly for printing purposes in the result files;
15. 'objective_of_interest': The output on which the uncertainty quantification is performed;

16. 'results dir': name of result folder in .../RESULTS/.

### results
The results are printed in ...\RESULTS\'case'\'rob' (or 'det')\'result dir'\
In the results you find the following files:
1. pareto: For every design sample in every generation, the outputs of the model (or uncertainty quantification in robust optimization) is printed;
2. paretoSolutions: For every design sample in every generation, the design sample is printed;
3. STATUS: The status of the optimization, showing the current generation number and computational budget spent.

## Uncertainty Quantification

### Initiation
The uncertainty quantification can be initiated in run_uq.py.\ 
In this script, you can define the main parameters for the uncertainty quantification:
1. 'case': the name of the folder where the case is defined which you want to evaluate (in ...\TC\);
2. 'pol_order': The polynomial order for the PCE;
3. 'PCE method': 'OLS' for Ordinary Least Squares method with a full PCE, 'stepwise' for the sparse PCE;
4. 'n_samples': When sparse PCE is selected, set the number of samples for constructing the PCE;
5. 'sampling_method': method for sampling the samples for model evaluation. currently only 'Random';
6. 'objective_names': The names of the model outputs. Mainly for printing purposes in the result files;
7. 'objective_of_interest': The output on which the uncertainty quantification is performed;
8. 'n_jobs': the number of processes that will be performed in parallel (nProcs) can be defined. Usually, this number should be equal or half of the number of cores available on your machine.;
9. 'create_only_samples': When True, create the design of experiments without evaluation. This is valuable when you can not connect the model directly to the framework; 
10. 'draw_pdf_cdf': When True, after the UQ, the probability density function and cumulative probability function are generated for the quantity of interest; 
11. 'samples_pdf_cdf': When draw_pdf_cdf is True, determine the number of samples used for generating the PDF and CDF on the surrogate model through Monte Carlo Simulation; 
12. 'results dir': name of result folder in .../RESULTS/.

### results
The results are printed in ...\RESULTS\'case'\UQ\'result dir'
in the results you find the following files:
1. samples: The random samples and the correspondig output generated for generating the PCE;
2. (full or sparse)_pce_order_('pol_order')_('objective_of_interest'): The Leave-One-Out error, sparse basis (useful if sparse PCE), mean and standard deviation following the PCE;
3. (full or sparse)_pce_order_('pol_order')_('objective_of_interest')_Sobol_indices: The first-order and total-order Sobol indices for each stochastic parameter.

if 'draw_pdf_cdf' is True:
4. Data_pdf_lcoe: The data for printing the probability density function;
5. Data_cdf_lcoe: The data for printing the cumulative probability function.

## design space exploration

### initiation
The design spae exploration can be initiated in run_design_space_exploration.py.\ 
In this script, you can define the main parameters for the stochastic dimension reduction:
1. number_of_design_samples: Number of design samples in the stochastic dimension reduction;
2. design_variables: Names of the design variables that need to be overwritten.
3. low_bound: Lower boundary for the range of the design variables;
4. upp_bound: Upper boundary for the range of the design variables;

Inside the dictionary:
1. 'case': the name of the folder where the case is defined which you want to evaluate (in ...\TC\);
2. 'pol_order': The polynomial order for the PCE;
3. 'PCE method': 'OLS' for Ordinary Least Squares method with a full PCE, 'stepwise' for the sparse PCE;
4. 'n_samples': When sparse PCE is selected, set the number of samples for constructing the PCE;
5. 'sampling_method': method for sampling the samples for model evaluation. currently only 'Random';
6. 'objective_names': The names of the model outputs. Mainly for printing purposes in the result files;
7. 'objective_of_interest': The output on which the uncertainty quantification is performed;
8. 'n_jobs': the number of processes that will be performed in parallel (nProcs) can be defined. Usually, this number should be equal or half of the number of cores available on your machine;
9. 'create_only_samples': When True, create the design of experiments without evaluation. This is valuable when you can not connect the model directly to the framework; 
10. 'draw_pdf_cdf': When True, after the UQ, the probability density function and cumulative probability function are generated for the quantity of interest; 
11. 'samples_pdf_cdf': When draw_pdf_cdf is True, determine the number of samples used for generating the PDF and CDF on the surrogate model through Monte Carlo Simulation; 
12. 'results dir': name of result folder in .../RESULTS/.

### results
The results are printed in ...\RESULTS\'case'\UQ\'result dir'\
In the results you find the following files:
1. samples: The random samples and the correspondig output generated for generating the PCE;
2. (full or sparse)_pce_order_('pol_order')_('objective_of_interest'): The Leave-One-Out error, sparse basis (useful if sparse PCE), mean and standard deviation following the PCE;
3. (full or sparse)_pce_order_('pol_order')_('objective_of_interest')_Sobol_indices: The first-order and total-order Sobol indices for each stochastic parameter.

if 'draw_pdf_cdf' is True:
4. Data_pdf_lcoe: The data for printing the probability density function;
5. Data_cdf_lcoe: The data for printing the cumulative probability function.

In ...\PLOT\read_Sobol.py, the number of significant parameters (with a max(Sobol indices) > 1/number_of_stochastic_parameters) are printed.
In ...\PLOT\read_LOO.py, the Leave-One-Out error is read for all the designs evaluated during the design space exploration. The maximum LOO is printed


## Bugs/improvements
- put help functions in main script in supplementary script
- improve the tc files? Quite a lot of adjustments need to be made (to be discussed)
- only NSGA2 works for now, but only small adjustments are needed to run the other optimizers (but not yet for now)
- test de sparse
- zet de optimalisatiecode ook in classes
