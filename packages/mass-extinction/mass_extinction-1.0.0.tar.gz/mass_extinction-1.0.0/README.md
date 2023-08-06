# **Biologically-Inspired Mass Extinction in Evolutionary Algorithms**
## _The Biologically-Inspired Extinction Operator_
###### Author: Kaelan Engholdt
###### Version: 05/26/2021

###

### Table of Contents
**Section 1** - _Introduction_  
**Section 2** - _Compatibility_  
**Section 3** - _Requirements_  
**Section 4** - _Contents_  
**Section 5** - _Design_  
**Section 6** - _Use_  
**Section 7** - _Integration_  
**Section 8** - _Adjustable Extinction Parameters_  
**Section 9** - _Adjustable Alternate Parameters_

## **Section 1 - Introduction**
Mass extinction events have previously been shown to be a catalyst for accelerating the rate of evolution in evolutionary algorithms.  This increased rate of evolution combined with a destabilization of the dynamic equilibrium of the evolutionary algorithm can allow the algorithm to overcome local optima in the solution space; however, most implementations of mass extinction squander the full benefit of the increased evolutionary rate by relying upon random chance to generate better solutions in the post-extinction generations.

This operator is a biologically-inspired mass extinction operator specifically designed for use in evolutionary algorithms, while retaining the benefits of extinction events from the natural world.  By increasing variability and decreasing selection pressure immediately after an extinction event, the evolutionary algorithm has a higher chance of yielding more fit individuals and overcoming local optima in the post-extinction generations.  The operator works especially well on problem domains with many local optima, with many evolutionary algorithms exhibiting a higher success rate than with standard implementations of mass extinction.

This operator contains adjustable parameters for extinction events and methods of repopulation, and is designed to be integrated into an evolutionary algorithm.  Due to the problem-specific nature of evolutionary algorithms, minor parts of this package must be finished by the user.

If used and tuned correctly, extinction can be a powerful tool in evolutionary algorithms.  This simple package attempts to provide a basis upon which users can integrate extinction events into their evolutionary algorithms, maintain population diversity, improve the overall fitness of their population, and attempt to overcome sub-optimal peaks within the search space of their particular problem.

Includes support for integration with evolutionary algorithms that make use of the _Distributed Evolutionary Algorithms in Python (DEAP)_ library, which is a framework for writing evolutionary algorithms.  This package is not affiliated with DEAP, but offers support for evolutionary algorithms using that library.

> This concludes the Introduction section.

###
###

## **Section 2 - Compatibility**
The files in this package are OS independent, and can be run on either Python 2 or Python 3.

> This concludes the Compatibility section.

###
###

## **Section 3 - Requirements**
Requirements:  
 - A population-based evolutionary algorithm written in Python 2 or Python 3.  
 - The parent population must be sorted by fitness and stored in a list.  
 - Following and completing all `TODO` comments.  

> This concludes the Requirements section.

###
###

## **Section 4 - Contents**
The package consists of the following files:  
 - `mass_extinction.py` : Contains the Extinction class.  
 - `ext_params.py` : Contains all of the adjustable extinction parameters for the Extinction class.  
 - `ext_types.py` : Contains numerous extinction parameter sets for testing purposes.  
 - `README.md` : Contains all documentation related to the Extinction class.  

> This concludes the Contents section.

###
###

## **Section 5 - Design**
The files in this package have been specifically designed to be integrated and interlaced with an evolutionary algorithm.  Due to the problem-specific nature of evolutionary algorithms, some of this package must be finished by the user.

This package features the following:  
 - A multitude of completely adjustable parameters that affect how both extinction and repopulation operate.  
 - Two methods of extinction:  
    - Instant Extinction  
    - Gradual Extinction  
 - Three types of extinction that can be used separately or in conjunction with one another:  
    - Interval Extinction  
    - Probabilistic Extinction  
    - Fitness Extinction  
 - Two methods of repopulation:  
    - Instant Repopulation  
    - Gradual Repopulation  
 - Three types of repopulation that can be used separately or in conjunction with one another:  
    - Repopulation using children of elite members.  
    - Repopulation using children of surviving members of an extinction event.  
    - Repopulation using random members.  
 - Testing of up to 324 parameter sets generated from permutations of user-defined parameters.  
 - All parameters can be saved as parameter sets and later called upon to revert back to a previous version of extinction/repopulation.  

> This concludes the Design section.

###
###

## **Section 6 - Use**
### **Sub-Section 6.1 - Importing the Extinction Class**
To use the Extinction class and its associated parameters, `mass_extinction.py`, `ext_params.py`, and `ext_types.py` must be copied into the same directory where your evolutionary algorithm is located.  Once copied into your project directory, the files must be imported into your evolutionary algorithm. It is advised to do this using the following import statements at the top of your evolutionary algorithm:

```sh
import mass_extinction as ext
import ext_params as ep
```

Importing `mass_extinction.py` will allow you to instantiate the Extinction class and begin utilizing extinction each generation.  Importing `ext_params.py` will allow you to access extinction parameters from your evolutionary algorithm if you wish, but it is not required for the Extinction class to function.

It is advised to read through all of the code in `mass_extinction.py`, the code is heavily commented for ease of understanding so that others can understand the program flow and how the Extinction class operates.  The code may get a little complicated during the calculation section, but the important thing is to understand how the Extinction class is operating at a basic level.  All of the adjustable extinction parameters along with their basic descriptions are found in `ext_params.py`.  For more detailed descriptions of all adjustable parameters, see Sections 8 and 9 below.

###

### **Sub-Section 6.2 - Calling the Extinction Class**
There is only one method meant to be accessed outside the Extinction class (the `main` method), the rest are internal methods.  Once `mass_extinction.py` has been imported into the evolutionary algorithm, the `main` method of the Extinction class should be accessed by the following call:

```sh
population, XOPB, MUTPB, MUT_RATE, TOURN_SIZE = ext.Extinction().main(population, evolution_params, logpath, saved_idx)
```

The parameters for the `main` method are described below:

#### _population_
```sh
population = list
```
The sorted parent population.

###

#### _evolution_params_
```sh
evolution_params = list
```
This list must be in the following form: `[current_generation, maximum_generations, xo_prob, mut_prob, mut_rate, tourn_size]`

Where each element in the list is defined as the following:

`current_generation = int`  
The current generation.

`maximum_generations = int`  
The total number of generations that the evolutionary algorithm will run for.

`xo_prob = float`  
The probability of crossover occurring in the evolutionary algorithm, defined within the range [0.00, 1.00].

`mut_prob = float`  
The probability of mutation occurring in the evolutionary algorithm, defined within the range [0.00, 1.00].

`mut_rate = float`  
The mutation rate in the evolutionary algorithm, defined within the range [0.00, 1.00].

`tourn_size = int`  
The current tournament size used in selection for the evolutionary algorithm.

###

#### _logpath_
```sh
logpath = str
```
Specifies the absolute path to the log file, where information for the current run of the evolutionary algorithm is being stored.  If a log file for the evolutionary algorithm is currently being generated, you may wish to pass that same file path for this parameter.  If not, you should provide an additional path where the log file for extinction can be written to.  The log file is automatically generated and cannot be disabled.

The written-out information consists of the following:  
 - A short description of the current extinction parameter set.  
 - All extinction parameters currently in use, written in the form of Python code.  
 - The generation an extinction event began along with the type of extinction that occurred, followed by:  
    - The number of members that were killed as a result of both the extinction event and anti-elitism.  
    - The number of members that were repopulated during the extinction event due to population dynamics.  
 - The generation repopulation began, followed by:  
    - The number and types of members that were repopulated.  

The description and parameters are written out so that they can be copied and saved in the `_saved_parameters` method of `mass_extinction.py` in case you wish to revert back to a previous extinction parameter set (see Sub-Section 6.5).

###

#### _saved_idx_
```sh
saved_idx = int
```
Specifies the index into the extinction parameter sets saved in the `_saved_parameters` method of `mass_extinction.py`.  Alternatively, if `ext_testing_on` is enabled (see Sub-Section 8.1), the `saved_idx` specifies the extinction parameter set to use in `ext_types.py` (see Sub-Section 6.6).

Note that this is an optional parameter, the default values found in `ext_params.py` will be used if the `saved_idx` is not provided.

###

### **Sub-Section 6.3 - Using the Extinction Class**
The call to the `main` method of the Extinction class should be placed in the evolutionary algorithm inside the main loop exactly where you wish extinction to occur.  The population must be sorted according to fitness before it is passed to the Extinction class.  The best members can be sorted to either the beginning or end of the population list, just be sure to set the targeting variable `ext_sort_order` in `ext_params.py` so that the Extinction class knows which end of the list the best and worst members are on (for more information on this, see Sub-Section 8.1).

A list (represented by the variable `evolution_params` above) must also be passed to the Extinction class, and must be in the form described above.  The reason these values must be passed to the Extinction class is because if alternate parameters are enabled (see Section 9), these values will change during extinction and repopulation to reflect what happens in a biological ecosystem during an extinction event and the subsequent repopulation phase.  If your evolutionary algorithm does not employ the use of tournaments for selection, or employ the use of mutation (such as in crossover-only evolutionary algorithms), a value of `-1` should be passed in their place.  Ensure that the alternate parameters for those features that are not in use are set to `False` in `ext_params.py`.

The `main` method of the Extinction class will return the population (altered if extinction or repopulation occurred) and the old population will be completely inaccessible.  This new population will be unsorted, and should be resorted before it is passed to the Extinction class in the next generation.  The Extinction class will also return the new values to be used for your crossover probability (represented by the variable `XOPB` above), your mutation probability (represented by the variable `MUTPB` above), your mutation rate (represented by the variable `MUT_RATE` above), and your tournament size (represented by the variable `TOURN_SIZE` above).  Even if your evolutionary algorithm does not employ all of these features, the Extinction class will return these five values, so the evolutionary algorithm should be prepared to receive five return values.  The features not in use can simply have the return value stored in a variable and the variable can remain unused.

###

### **Sub-Section 6.4 - Configuring Extinction Parameters**
In order for the Extinction class to function, all of the extinction parameters desired to be used must be defined by the user in `ext_params.py`.  Any extinction parameters that fall out of their correct ranges or that have conflicts with other extinction parameters will be printed to the console and an exception will be raised to inform the user that their extinction parameters are incorrectly defined and will cause errors within the Extinction class.  See Sections 8 and 9 for more information and details regarding the adjustable extinction parameters.

###

### **Sub-Section 6.5 - Saving Extinction Parameter Sets**
To save parameter sets in the `_saved_parameters` method of `mass_extinction.py`, you may wish to enable `ext_print_on` in `ext_params.py` (see Sub-Section 8.1).  This will cause all of the information that goes into the log file to also be printed to the console.  All extinction parameters that were used during the current run will be printed in the form of Python code, along with a simple description of the parameter set.  Simply copy the printed code chunk and paste it under the next `if` block in the `_saved_parameters` method.  The `saved_idx` variable should be increased by one for each subsequent entry of a parameter set into the `_saved_parameters` method.  The description should also be copied and pasted as a block comment above the corresponding `if` code block holding the extinction parameter set.  The parameter that controls printing to the console, `ext_print_on`, is not included in parameter sets, this is always controlled from `ext_params.py`.

###

### **Sub-Section 6.6 - Testing Extinction Parameter Sets**
The last file included in this package is named `ext_types.py`.  It contains 324 extinction parameter sets that can be tested using the same methodology as the `_saved_parameters` method of `mass_extinction.py`.  To use it, simply enable `ext_testing_on` in `ext_params.py` (see Sub-Section 8.1).  This will call the `saved_params` function in `ext_types.py`, passing the same `saved_idx` and indexing into that set of parameters instead of the user-saved parameter sets.  The top portion of `ext_types.py` contains various lists of extinction parameter values that will be used in the parameter sets for testing.  The 324 parameter sets are generated from all permutations of the lists of parameter values.  There are also extinction parameters at the top of the file that will be used across all extinction sets.  If you do not want to use a certain parameter that takes a number as input, you can simply set it to zero.

Note that none of the parameter sets in `ext_types.py` utilize fitness extinction (see Sub-Section 8.7), they only utilize interval extinction (see Sub-Section 8.5) and probabilistic extinction (see Sub-Section 8.6).

> This concludes the Use section.

###
###

## **Section 7 - Integration**
As stated above, this package is incomplete and will not run if it is simply imported and the `main` method of the Extinction class is called.  You are required to do a few things to prepare the files for use in your specific evolutionary algorithm.  There isn't much to do, and most of the tasks are fairly trivial and should already be a part of your evolutionary algorithm, it's just a matter of calling those methods from the Extinction class.  Everything required of you is marked in `mass_extinction.py`, `ext_params.py`, and `ext_types.py` with `TODO` comments.

The following is a list of all comments that require your attention:  
 - `TODO` comments in `mass_extinction.py` :  
    - Line 16 requires `mass_extinction.py` to be copied into the evolutionary algorithm's same directory.  
    - Lines 476-480 contain the required information for finishing fitness extinction.  
    - Lines 810-815 contain the required information for finishing repopulation using children of elite members.  
    - Lines 843-848 contain the required information for finishing repopulation using children of surviving members.  
    - Lines 873-878 contain the required information for finishing repopulation using random members.  
    - Line 1206 simply informs the user that they can add the printed description for their saved extinction parameter sets.  
    - Line 1208 simply informs the user that they can copy and paste printed extinction parameter sets to save them for later use.  
 - `TODO` comments in `ext_params.py` :  
    - Line 14 requires `ext_params.py` to be copied into the evolutionary algorithm's same directory.  
    - Line 16 informs the user that they must adjust all parameters they desire to use.  
    - Lines 75-77 requires the user to add lines 78 and 79 to the initialization of their member class.  
 - `TODO` comments in `ext_types.py` :  
    - Line 11 requires `ext_types.py` to be copied into the evolutionary algorithm's same directory.  
    - Line 13 informs the user that they must adjust all parameters they desire to use in the permutations.  

> This concludes the Integration section.

###
###

## **Section 8 - Adjustable Extinction Parameters**
The following sub-sections describe all tunable extinction parameters found in `ext_params.py` in greater detail. There are a few parameters in `ext_params.py` that are listed as untunable, these parameters are used as global variables by the Extinction class and should **NOT** be changed.

###

### **Sub-Section 8.1 - Basic Extinction Parameters**
These are the basic extinction parameters used to modify the highest levels of extinction behavior.

Once an extinction event occurs via one of the extinction types (see Sub-Section 8.4), the `ext_duration` parameter specifies whether the extinction event occurs over a period of time (gradual extinction) or instantaneously (instant extinction).  In the biological world, instant extinction reflects a meteor impacting the planet and instantly killing off a majority of the members, while gradual extinction reflects a lethal virus spreading through a biological population and slowly killing off a majority of the members.  Here, the virus is represented by the gradual extinction process.  The virus can kill a constant number of members as it progresses, or the virus can get stronger or weaker as it progresses depending on its virulence, this is represented by the `ext_virulence` parameter.

The equation used to determine how many members to kill off in each generation is based on classical models in population dynamics in order to accurately model the logarithmic decline of a population in the midst of a lethal virus.  The model approximates quite well for normal extinction percentages (40% - 80%) and is relatively unaffected by varying population sizes.  To justify the use of logarithmic modeling, the duration of the extinction event must be at least 8 generations; for values between 1 and 7 generations, a constant rate of killing is used automatically, regardless of whether the `ext_kills_constant` parameter is enabled or not.

The members that are killed by an extinction event can either be completely random, or target the least fit members of the population, this is specified by the `ext_kills_least_fit` parameter.  An extinction event will never occur while the population is repopulating itself (see Sub-Section 8.8).

###

#### _ext_operator_on_
```sh
ext_operator_on = Boolean
```
Turns extinction on (`True`) or off (`False`).

It is possible for the extinction operator to be turned off towards the end of the evolutionary algorithm's run via the `ext_end_extinction` parameter.

###

#### _ext_percent_
```sh
ext_percent = float    Range: (0.00, 1.00)
```
Specifies the percent of the population that will be killed in an extinction event.

The anti-elitism percentage (see Sub-Section 8.3) is not included, so if anti-elitism is enabled, more members will be killed than this percentage defines.

###

#### _ext_duration_
```sh
ext_duration = int    Range: [1, maximum_generations)
```
Specifies the duration of an extinction event (the number of generations that it will take to kill off `ext_percent` of the population).

If this parameter is set to a value of `1`, this indicates instant extinction.  If this parameter is set to a value greater than `1`, this indicates gradual extinction.

If using gradual extinction, it is recommended that `ext_pop_dynamics_on` is enabled (see Sub-Section 8.1), otherwise there is no real purpose for using gradual extinction versus instant extinction (the reasoning behind this is explained under the `ext_pop_dynamics_on` parameter).  Additionally, if using gradual extinction, it is recommended that alternate parameters are enabled via the `alt_params_on` parameter (see Section 9), otherwise there is no real purpose for using gradual extinction versus instant extinction (the reasoning behind this is explained in Section 9).

###

#### _ext_sort_order_
```sh
ext_sort_order = Boolean
```
Indicates how the population list is sorted when it is passed from the evolutionary algorithm to the `main` method of the Extinction class.  From best fitness to worst fitness (`True`) or from worst fitness to best fitness (`False`).

This is an essential parameter setting:
 - If the best members in the population are sorted to the front of the population list, then this parameter must be set to `True`.
 - If the best members in the population are sorted to the end of the list, then this parameter must be set to `False`.

###

#### _ext_kills_least_fit_
```sh
ext_kills_least_fit = Boolean
```
Indicates if an extinction event will kill the least fit members (those with the worst fitness) of the population (`True`), or completely random members of the population (`False`).

Killing the least fit members functions similar to anti-elitism (see Sub-Section 8.3).

###

#### _ext_kills_constant_
```sh
ext_kills_constant = Boolean
```
Indicates if the number of members an extinction event kills every generation is constant (`True`) or logarithmic (`False`).

Note that to justify the use of logarithmic modeling, the duration of the extinction event (specified by `ext_duration`) must be at least 8 generations; for values between 1 and 7 generations, a constant rate of killing is used automatically, regardless of this parameter.

###

#### _ext_virulence_
```sh
ext_virulence = Boolean
```
Indicates if an extinction event gets stronger (`True`) or weaker (`False`) as it progresses over the course of `ext_duration` generations, according to the logarithmic model of extinction.

If `ext_kills_constant` is enabled, this parameter has no effect, since the number of deaths from an extinction event in each generation will be kept constant.  Additionally, this parameter has no effect if the duration of the extinction event (specified by `ext_duration`) is between 1 and 7 generations, since the duration must be at least 8 generations to justify the use of logarithmic modeling.

###

#### _ext_pop_dynamics_on_
```sh
ext_pop_dynamics_on = Boolean
```
Turns population dynamics on (`True`) or off (`False`).

Enabling population dynamics means that slightly more members will be killed off in an extinction event than normal.  These extra members that are killed off will then immediately be repopulated by random members.  This more accurately reflects population dynamics present in biological ecosystems.  A population will not simply completely die off over time, but it will continue to reproduce as it dies off.  These random members will help contribute new genetic material to the population as the overall population decreases in size.  By the end of the extinction event, the correct amount of `ext_percent` of members will have been killed off.  If using gradual extinction (where `ext_duration` has a value greater than `1`), it is recommended that `ext_pop_dynamics_on` is enabled, as this supports the motivation behind the use of gradual extinction versus instant extinction.

###

#### _ext_pop_dyn_strength_
```sh
ext_pop_dyn_strength = float    Range: [0.00, 1.00]
```
Specifies how strong the population dynamics will be when `ext_pop_dynamics_on` is enabled.

If `ext_pop_dynamics_on` is disabled, this parameter has no effect, `ext_pop_dynamics_on` must be enabled for this parameter to function.

A value of `0.00` means that no additional members will be killed off during an extinction event, it is equivalent to disabling `ext_pop_dynamics_on`.  A value of `1.00` means that double the extinction amount will be killed for each generation of `ext_duration` as the extinction event progresses.  It is recommended that `ext_pop_dyn_strength` be set to a value around to `0.15`, but you may want to experiment with what works best in your evolutionary algorithm.

###

#### _ext_end_extinction_
```sh
ext_end_extinction = Boolean
```
Indicates if the extinction operator (`ext_operator_on`) will turn off after reaching a certain generational point in the evolutionary algorithm's run (`True`), or if the extinction operator will remain on for the entirety of the evolutionary algorithm's run (`False`).

If this parameter is enabled, this means the extinction operator will turn off after reaching the number of generations specified by `ext_end_percent`.  This may be desirable to use if you do not want extinction to occur too close to the end of the evolutionary algorithm's run, as killing off a majority of the members too close to the end may not give the repopulated members enough time to evolve into better members.

###

#### _ext_end_percent_
```sh
ext_end_percent = float    Range: (0.00, 1.00]
```
Specifies the percent of generations that will execute before the extinction operator (`ext_operator_on`) is turned off.

If `ext_end_extinction` is disabled, this parameter has no effect, `ext_end_extinction` must be enabled for this parameter to function.

A value of `0.95` means that 95% of the maximum generations will execute, after which the extinction operator will be turned off and the evolutionary algorithm will continue without employing extinction.  If an extinction event occurred close to this generational point, repopulation will continue beyond this generational point to ensure that the population returns to its original size.  A value of `1.00` means the extinction operator will remain on for the entirety of the evolutionary algorithm's run, and is equivalent to disabling `ext_end_extinction`.

###

#### _ext_safeguard_
```sh
ext_safeguard = int    Range: [0, maximum_generations)
```
Specifies the minimum number of generations between possible extinction events.

Note that this parameter only applies to probabilistic extinction (see Sub-Section 8.6) and fitness extinction (see Sub-Section 8.7), since interval extinction by definition specifies the minimum number of generations between possible extinction events.  If you do not want extinction to have the chance to occur in close proximity to another extinction event, this safeguard will prevent that possibility.  A value of `0` means the safeguard will be shut off, and extinction has the possibility to occur every generation.

###

#### _ext_print_on_
```sh
ext_print_on = Boolean
```
Turns print statements for extinction and repopulation information on (`True`) or off (`False`).

The printed information relayed to the console is the same information that is printed to the log file, and consists of the following:  
 - A short description of the current extinction parameter set.  
 - All extinction parameters currently in use, printed in the form of Python code.  
 - The generation an extinction event began along with the type of extinction that occurred, followed by:  
    - The number of members that were killed as a result of both the extinction event and anti-elitism.  
    - The number of members that were repopulated during the extinction event due to population dynamics.  
 - The generation repopulation began, followed by:  
    - The number and types of members that were repopulated.  

The description and parameters are printed so that they can be copied and saved in the `_saved_parameters` method of `mass_extinction.py` in case you wish to revert back to a previous extinction parameter set (see Sub-Section 6.5).  The value of this parameter does not affect the log file, the log file will be written out with identical information regardless of this parameter's value.

###

#### _ext_testing_on_
```sh
ext_testing_on = Boolean
```
Indicates whether the pre-defined parameter sets held in `ext_types.py` will be used (`True`), or if the user defined parameter sets will be used (`False`).

If this parameter is enabled, any user-saved parameter sets in the `_saved_parameters` method of `mass_extinction.py` will be disregarded, and instead a pre-defined parameter set in `ext_types.py` will be used, depending on the passed `saved_idx` (see Sub-Sections 6.2 and 6.6).

###

#### _ext_uses_DEAP_
```sh
ext_uses_DEAP = Boolean
```
Indicates whether the evolutionary algorithm makes use of the _Distributed Evolutionary Algorithms in Python (DEAP)_ library, which is a framework for writing evolutionary algorithms.

The reason this is important is for checking and adjusting the newborn fields of individuals, which differs from simply accessing the fields in a normal member class versus a _DEAP_ individual.  Checking these fields and adjusting them appropriately is automatically taken care of within the Extinction class, assuming this parameter is set appropriately:
 - If your evolutionary algorithm does not use _DEAP_ as its framework, and members are created via a user-made class, then the appropriate code should be added to the initialization of the member class, and this parameter must be set to `False`.
 - If your evolutionary algorithm does use _DEAP_ as its framework, then the appropriate code should be added using _DEAP_, and this parameter must be set to `False`.

See Sub-Section 8.9 for more information and details regarding the code that needs to be added to members and how newborn fields of individuals are accessed and used.

###

### **Sub-Section 8.2 - Elitism Parameters**
Elitism ensures that the best members of the population (those with the best fitness) will be preserved if an extinction event occurs.  This is used to guarantee the survival of the best individuals in the population.  It is highly recommended to use some amount of elitism (such as 10% of the population).  If the best individuals are not protected, it is almost a certainty that they might be killed off in an extinction event, greatly reducing the effectiveness of the algorithm.

Members that are considered elite may be used during the repopulation phase via the `repop_use_elites` parameter (see Sub-Section 8.8).

###

#### _ext_elite_on_
```sh
ext_elite_on = Boolean
```
Turns elitism on (`True`) or off (`False`).

Members that are considered elite are guaranteed to survive extinction.  Members that are considered elite may also be used during the repopulation phase via the `repop_use_elites` parameter (see Sub-Section 8.8).

###

#### _ext_elite_percent_
```sh
ext_elite_percent = float    Range: [0.00, 1.00)
```
Specifies the percent of the population to consider elite (guaranteed to survive extinction).

Members that are considered elite may be used during the repopulation phase via the `repop_use_elites` parameter (see Sub-Section 8.8).

If `ext_elite_on` is disabled, this parameter has no effect, `ext_elite_on` must be enabled for this parameter to function.

###

### **Sub-Section 8.3 - Anti-Elitism Parameters**
Anti-elitism ensures that the worst members of the population (those with the worst fitness) will be terminated if an extinction event occurs.  This is used to guarantee the death of the worst individuals in the population.  If using gradual extinction (where `ext_duration` has a value greater than `1`), anti-elitism will only occur in the first generation of an extinction event.  If used, it is highly recommended that a very low amount of anti-elitism is used.  The percentage of the population killed due to anti-elitism is not included in the `ext_percent` of individuals killed in an extinction event (see Sub-Section 8.1).

###

#### _ext_anti_elite_on_
```sh
ext_anti_elite_on = Boolean
```
Turns anti-elitism on (`True`) or off (`False`).

Members that are anti-elite are guaranteed to be killed in the first generation of an extinction event.

###

#### _ext_anti_elite_percent_
```sh
ext_anti_elite_percent = float    Range: [0.00, 1.00)
```
Specifies the percent of the population to consider anti-elite (guaranteed to be killed in the first generation of an extinction event).

Note that this does not contribute to the `ext_percent` of individuals killed by extinction (see Sub-Section 8.1).

If `ext_anti_elite_on` is disabled, this parameter has no effect, `ext_anti_elite_on` must be enabled for this parameter to function.

###

### **Sub-Section 8.4 - Extinction Types**
At least one of the following extinction types must be enabled to determine when extinction events will occur during an evolutionary algorithm's run.  If desired, it is possible for two or all three types of extinction to work simultaneously with one another.

###

#### _interval_extinction_on_
```sh
interval_extinction_on = Boolean
```
Turns interval extinction on (`True`) or off (`False`).

See Sub-Section 8.5 for more information and details regarding interval extinction.

###

#### _prob_extinction_on_
```sh
prob_extinction_on = Boolean
```
Turns probabilistic extinction on (`True`) or off (`False`).

See Sub-Section 8.6 for more information and details regarding probabilistic extinction.

###

#### _fit_extinction_on_
```sh
fit_extinction_on = Boolean
```
Turns fitness extinction on (`True`) or off (`False`).

See Sub-Section 8.7 for more information and details regarding fitness extinction.

###

### **Sub-Section 8.5 - Interval Extinction**
The first of the three types of extinction, interval extinction means extinction events will occur periodically on a set interval.  Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

###

#### _i_ext_interval_
```sh
i_ext_interval = int    Range: [1, maximum_generations)
```
Specifies the number of generations between extinction events.

Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

If `interval_extinction_on` is disabled, this parameter has no effect, `interval_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

### **Sub-Section 8.6 - Probabilistic Extinction**
The second of the three types of extinction, probabilistic extinction means extinction events will occur with a set probability at periodic intervals.  If an extinction event does not occur, the probability can be increased that it will happen on the next interval.  After an extinction event occurs, the probability that an extinction event will occur on an interval resets to the base probability.  Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

###

#### _p_ext_interval_
```sh
p_ext_interval = int    Range: [1, maximum_generations)
```
Specifies the number of generations between checking the current probability to determine if an extinction event occurs.

A value of `1` means the probability of an extinction event occurring will be checked every generation.  If an extinction event does not occur, the probability that an extinction event will occur on the next interval increases by `p_ext_prob_inc`.  If an extinction event does occur, the probability that an extinction event will occur on the next interval resets to the base probability specified by `p_ext_base_prob`.  Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

If `prob_extinction_on` is disabled, this parameter has no effect, `prob_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

#### _p_ext_base_prob_
```sh
p_ext_base_prob = float    Range: [0.00, 1.00]
```
Specifies the base probability of an extinction event occurring on an interval.

After an extinction event occurs, the current probability of an extinction event occurring on the next interval will reset back to this parameter's value.  A value of `1.00` means the possibility of an extinction event occurring on each interval is guaranteed, and is equivalent to utilizing interval extinction (see Sub-Section 8.5).

If `prob_extinction_on` is disabled, this parameter has no effect, `prob_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

#### _p_ext_prob_inc_
```sh
p_ext_prob_inc = float    Range: [0.00, 1.00]
```
Specifies the amount to increase the current probability of an extinction event occurring on an interval by when a generation passes and no extinction event occurs.

A value of `1.00` means the probability of an extinction event occurring on the next interval is guaranteed.  A value of `0.00` means the probability of an extinction event occurring on the next interval will never change, and the probability will remain the value of `p_ext_base_prob` for the duration of the evolutionary algorithm's run.

If `prob_extinction_on` is disabled, this parameter has no effect, `prob_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

#### _p_ext_always_resets_
```sh
p_ext_always_resets = Boolean
```
Indicates whether the source of extinction events is exclusive to probabilistic extinction (`False`), or if any extinction event from other extinction types (interval extinction and fitness extinction) are acceptable (`True`), for the purposes of resetting the current probability of an extinction event occurring on the next interval back to `p_ext_base_prob`.

While the probability of an extinction event occurring on an interval is exclusive to probabilistic extinction, this parameter specifies whether the reset to base probability occurs from any extinction event (even those from other extinction types), or if the probability will only reset upon an extinction event triggered by probabilistic extinction.  By definition, this parameter will only matter when probabilistic extinction is used simultaneously with at least one other extinction type, such as interval extinction and/or fitness extinction (see Sub-Section 8.4).

If `prob_extinction_on` is disabled, this parameter has no effect, `prob_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).  Additionally, if neither `interval_extinction_on` nor `fit_extinction_on` is enabled, this parameter has no effect, at least one other extinction type must be enabled along with probabilistic extinction for this parameter to function (see Sub-Section 8.4).

###

### **Sub-Section 8.7 - Fitness Extinction**
The third and final type of extinction, fitness extinction means extinction events will occur after there has been no significant improvement in the fitness of the population since the last interval check, this improvement is measured at periodic intervals and the metric is defined by the user.  Being the most implementation-specific extinction type, incorporating this extinction type into an evolutionary algorithm is largely up to the user, but a few parameters are provided to assist in the integration.  The basis for this extinction type had only one fitness value in mind, but for members that have multiple fitness values (for multi-objective evolutionary algorithms), these can easily be incorporated by the user.  Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

###

#### _f_ext_interval_
```sh
f_ext_interval = int    Range: [1, maximum_generations)
```
Specifies the number of generations between checking if the required percentage of the population (`f_ext_pop_percent`) improved in fitness by `f_ext_improve_percent` to determine if an extinction event occurs.

A value of `1` means the possibility of an extinction event occurring will be checked every generation.  Intervals will only start counting after a repopulation phase has finished repopulating the population from a previous extinction event.

If `fit_extinction_on` is disabled, this parameter has no effect, `fit_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

#### _f_ext_pop_percent_
```sh
f_ext_pop_percent = float    Range: [0.00, 1.00]
```
Specifies the percent of the population that is required to improve in fitness by the amount specified by `f_ext_improve_percent`.

If the percentage of the population specified by this parameter is not reached by the population on the interval check, an extinction event will occur.

If `fit_extinction_on` is disabled, this parameter has no effect, `fit_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

#### _f_ext_improve_percent_
```sh
f_ext_improve_percent = float    Range: [0.00, 1.00]
```
Specifies the required percentage of fitness improvement since the previous interval check.

The user must define the metric used to measure the improvement in fitness between interval checks, this could be done by only comparing against the best member in the population from the previous interval check, or each member could contain a history of its own fitness values at each interval check.  This can be configured in a variety of ways and is left to the user for implementation.

If `fit_extinction_on` is disabled, this parameter has no effect, `fit_extinction_on` must be enabled for this parameter to function (see Sub-Section 8.4).

###

### **Sub-Section 8.8 - Repopulation Parameters**
Defines how the repopulation phase will function after an extinction event occurs.

Once an extinction event occurs via one of the extinction types (see Sub-Section 8.4), the population will need to repopulate its members to recover from the extinction event.  The `repop_duration` parameter specifies whether the repopulation phase occurs over a period of time (gradual repopulation) or instantaneously (instant repopulation).  Instant repopulation is not supported in the biological world, there are no cases where a population is able to instantaneously repopulate itself back to the carrying capacity of the environment (i.e., the original population size before the extinction event) after suffering a dramatic loss in population.  Gradual repopulation, on the other hand, is in line with every biological system for how populations repopulate themselves: gradually, over a series of generations until the carrying capacity of the environment is reached.  The repopulation phase can repopulate members at a constant rate, or repopulation can repopulate members at a logarithmic rate, getting stronger or weaker as repopulation progresses, this is represented by the `repop_growth` parameter.

If using gradual repopulation, it should be used in conjunction with alternate parameters (see Section 9) that modify the genetic operators of the evolutionary algorithm to model effects similar to those found in the wake of biological extinction events. Using gradual repopulation without employing any alternate parameters to modify genetic operators after an extinction event will most likely cause the algorithm to fair worse than the same parameter set run on instant repopulation.  Genetic operators should be modified to simulate similar effects found after biological extinction events. This includes lowering the selection pressure and increasing the crossover/mutation probability as well as the mutation rate.  As the population begins to refill back to its original size, these operators will be gradually returned back to their original values.

The equation used to determine how many members to repopulate each generation is based on classical models in population dynamics to accurately model the logarithmic increase of a population.  The model approximates quite well for normal extinction percentages (40% - 80%) and is relatively unaffected by varying population sizes.  To justify its use of logarithmic modeling, the duration of the repopulation phase must be at least 8 generations; for values between 1 and 7 generations, a constant rate of repopulation is used automatically, regardless of whether the `repop_constant` parameter is enabled or not.

Extinction will never occur while the population is repopulating itself.  If using gradual extinction (see Sub-Section 8.1), the repopulation phase will not begin until the extinction event has completed in its entirety.  The repopulation phase will begin in the same generation that the extinction event ends, and will repopulate the number of members lost due to the triggering of an extinction event, which consists of the number of members killed due to anti-elitism (see Sub-Section 8.3), and the number of members killed by the extinction event itself (see Sub-Section 8.1).

The makeup of repopulated members is parameterized, they may consist of children of elite members, if elitism is enabled (see Sub-Section 8.2), children of members that survived the extinction event, or randomly constructed members.  It is important that a large portion of the repopulated members are random so that their genetic material can proliferate and spread throughout the population (via crossover) in the following generations so that more of the search space can be explored.  This is an important aspect for overcoming local optima.  However, it is detrimental to have too many random members being repopulated, so this parameter will have to be tuned according to what works best in your evolutionary algorithm.

###

#### _repop_duration_
```sh
repop_duration = int    Range: [1, maximum_generations)
```
Specifies the duration of the repopulation phase (the number of generations that it will take for the population to return back to its original size before the extinction event occurred).

If this parameter is set to a value of `1`, this indicates instant repopulation.  If this parameter is set to a value greater than `1`, this indicates gradual repopulation.

If using gradual repopulation, it is recommended that alternate parameters are enabled via the `alt_params_on` parameter (see Section 9), otherwise there is no real purpose for using gradual repopulation versus instant repopulation (the reasoning behind this is explained in Section 9).

The repopulation phase will begin in the same generation that the extinction event ends, and will repopulate the number of members lost due to the triggering of an extinction event, which consists of the number of members killed due to anti-elitism (see Sub-Section 8.3), and the number of members killed by the extinction event itself (see Sub-Section 8.1).

###

#### _repop_constant_
```sh
repop_constant = Boolean
```
Indicates if the number of members the repopulation phase repopulates every generation is constant (`True`) or logarithmic (`False`).

Note that to justify the use of logarithmic modeling, the duration of the repopulation phase (specified by `repop_duration`) must be at least 8 generations; for values between 1 and 7 generations, a constant rate of repopulation is used automatically, regardless of this parameter.

###

#### _repop_growth_
```sh
repop_growth = Boolean
```
Indicates if repopulation gets stronger (`True`) or weaker (`False`) as it progresses over the course of `repop_duration` generations, according to the logarithmic model of repopulation.

If `repop_constant` is enabled, this parameter has no effect, since the number of births from repopulation in each generation will be kept constant.  Additionally, this parameter has no effect if the duration of the repopulation phase (specified by `repop_duration`) is between 1 and 7 generations, since the duration must be at least 8 generations to justify the use of logarithmic modeling.

###

#### _repop_use_elites_
```sh
repop_use_elites = Boolean
```
Turns the use of elite members for repopulation on (`True`) or off (`False`).

This means that of the number of members that need to be repopulated, the percentage of those members given by `repop_elite_percent` will be made up of children constructed using crossover and/or mutation between the elite members of the population.  The remaining members will either be constructed using the surviving members (if `repop_use_survivors` is enabled) or randomly constructed members.  Whatever percentage of members that is not made up of elite children or survivor children will be made up of random members.  Note that the elite members of the population are always a part of the surviving members of the population since elite members are guaranteed to survive extinction (see Sub-Section 8.2).

If `ext_elite_on` is disabled, this parameter has no effect, `ext_elite_on` must be enabled for this parameter to function (see Sub-Section 8.2).

###

#### _repop_elite_percent_
```sh
repop_elite_percent = float    Range: [0.00, 1.00]
```
Specifies the percent of members that will be generated by the elite members during the repopulation phase.

This means that of the number of members that need to be repopulated, the percentage of those members given by this parameter will be made up of children constructed using crossover and/or mutation between the elite members of the population.  The remaining members will either be constructed using the surviving members (if `repop_use_survivors` is enabled) or randomly constructed members.  Whatever percentage of members that is not made up of elite children or survivor children will be made up of random members.  Note that the elite members of the population are always a part of the surviving members of the population since elite members are guaranteed to survive extinction (see Sub-Section 8.2).

Repopulating using elite children can help produce individuals that are similar to the best individuals in the remaining population, but different enough to possibly explore different areas of the search space.  A value of `1.00` means that all of the repopulated members will be made up of children constructed from elite members.  A value of `0.00` means none of the repopulated members will be made up of children constructed from elite members, and is equivalent to disabling `repop_use_elites`.  It is recommended that 0%-30% of repopulated members be made up of elite children; it is important that a large portion of the repopulated members are random so that their genetic material can proliferate and spread throughout the population (via crossover) in the following generations so that more of the search space can be explored.  This is an important aspect for overcoming local optima.  However, it is detrimental to have too many random members being repopulated, so this parameter will have to be tuned according to what works best in your evolutionary algorithm.

If `ext_elite_on` is disabled, this parameter has no effect, `ext_elite_on` must be enabled for this parameter to function (see Sub-Section 8.2).  Additionally, if `repop_use_elites` is disabled, this parameter has no effect, `repop_use_elites` must be enabled for this parameter to function.

###

#### _repop_use_survivors_
```sh
repop_use_survivors = Boolean
```
Turns the use of surviving members (those members that survived the extinction event) for repopulation on (`True`) or off (`False`).

This means that of the number of members that need to be repopulated, the percentage of those members given by `repop_survivor_percent` will be made up of children constructed using crossover and/or mutation between the surviving members of the population.  The remaining members will either be constructed using the elite members (if `repop_use_elites` is enabled) or randomly constructed members.  Whatever percentage of members that is not made up of elite children or survivor children will be made up of random members.  Note that the elite members of the population are always a part of the surviving members of the population since elite members are guaranteed to survive extinction (see Sub-Section 8.2).

###

#### _repop_survivor_percent_
```sh
repop_survivor_percent = float    Range: [0.00, 1.00]
```
Specifies the percent of members that will be generated by the surviving members (those members that survived the extinction event) during the repopulation phase.

This means that of the number of members that need to be repopulated, the percentage of those members given by this parameter will be made up of children constructed using crossover and/or mutation between the surviving members of the population.  The remaining members will either be constructed using the elite members (if `repop_use_elites` is enabled) or randomly constructed members.  Whatever percentage of members that is not made up of elite children or survivor children will be made up of random members.  Note that the elite members of the population are always a part of the surviving members of the population since elite members are guaranteed to survive extinction (see Sub-Section 8.2).

Repopulating using survivor children can help produce individuals that are similar to the current individuals remaining in the population, but different enough to possibly explore different areas of the search space.  A value of `1.00` means that all of the repopulated members will be made up of children constructed from surviving members.  A value of `0.00` means none of the repopulated members will be made up of children constructed from surviving members, and is equivalent to disabling `repop_use_survivors`.  It is recommended that 30%-60% of repopulated members be made up of survivor children, it is important that a large portion of the repopulated members are random so that their genetic material can proliferate and spread throughout the population (via crossover) in the following generations so that more of the search space can be explored.  This is an important aspect for overcoming local optima.  However, it is detrimental to have too many random members being repopulated, so this parameter will have to be tuned according to what works best in your evolutionary algorithm.

If `repop_use_survivors` is disabled, this parameter has no effect, `repop_use_survivors` must be enabled for this parameter to function.

###

### **Sub-Section 8.9 - Newborn Parameters**
The term "newborn" refers to the status of a member that has recently been repopulated or "born" into the world after an extinction event.  These newborn members can be protected from future extinction events in close proximity to their birth.  These newborn members should also be protected from selection pressure in the evolutionary algorithm, this will allow these new members and their new genetic material to have a chance to spread into the population before being killed off in a selection phase of the evolutionary algorithm.  The goal is to maintain population diversity by giving new members a chance to survive and evolve into a possibly better member, as well as spread their genetic material to other members.  While testing this package and its integration into various evolutionary algorithms, protecting the newborn members from selection pressure was essential for the evolutionary algorithms to perform well.

As discussed in Section 7, one of the things required of the user is to add two fields to the initialization of the member class in their evolutionary algorithm, namely `ext_is_newborn` and `ext_newborn_gens`.  If individuals are structured using a user-made class, this can be accomplished using the following code:

```sh
# newborn parameters for the Extinction class
self.ext_is_newborn = False
self.ext_newborn_gens = 0
```

However, if the evolutionary algorithm makes use of the _Distributed Evolutionary Algorithms in Python (DEAP)_ library, adding these two fields to the initialization of members is performed differently, and can be accomplished using the following code:

```sh
# create DEAP structures
creator.create("Individual", list)

# toolbox for DEAP
toolbox = base.Toolbox()

# DEAP structure initializers
toolbox.register("genome")    # the genome structure of individuals is defined here
toolbox.register("ext_is_newborn", bool, False)
toolbox.register("ext_newborn_gens", int, 0)
toolbox.register("individual", tools.initCycle, creator.Individual,
                (toolbox.genome, toolbox.ext_is_newborn, toolbox.ext_newborn_gens), n=1)
```

If _DEAP_ individuals have more fields than just the genome (as is the case here since the `ext_is_newborn` and `ext_newborn_gens` fields have been added to the individual in addition to the genome), then the genome of the _DEAP_ individuals is accessed by indexing into the zeroth element of the individual.  Consequently, checking if the member is a newborn is found by checking the first element of the individual (checks the `ext_is_newborn` field), and checking how long the member has been a newborn is found by checking the second element of the individual (checks the `ext_newborn_gens` field).  Note that the indices for both of the newborn fields must be in exactly the first and second indices of the _DEAP_ individual, as described, otherwise these indices will have to be changed by the user in the Extinction class.

The meaning of the added newborn fields is the following:
 - `ext_is_newborn` : This field indicates the newborn status of the individual.  If this field is `True`, then the individual is considered a newborn member.  If this field is `False`, then the individual is not considered a newborn member.
 - `ext_newborn_gens` : This field indicates the number of generations that the individual has been a newborn member.

Checking these fields and adjusting them appropriately is automatically taken care of within the Extinction class, assuming the `ext_uses_DEAP` parameter is set appropriately in `ext_params.py` (see Sub-Section 8.1):
 - If your evolutionary algorithm does not use _DEAP_ as its framework, and members are created via a user-made class, then the appropriate code should be added to the initialization of the member class, and the `ext_uses_DEAP` parameter must be disabled.
 - If your evolutionary algorithm does use _DEAP_ as its framework, then the appropriate code should be added using _DEAP_, and the `ext_uses_DEAP` parameter must be enabled.

###

#### _newborn_params_on_
```sh
newborn_params_on = Boolean
```
Turns newborn parameters on (`True`) or off (`False`).

###

#### _newborn_expires_
```sh
newborn_expires = int    Range: [0, maximum_generations)
```
Specifies the number of generations that repopulated members are considered newborn members.

A value of `0` means that the newborn members will only be considered newborn members for the rest of the current generation, after which they will be the same as any other member.

If `newborn_params_on` is disabled, this parameter has no effect, `newborn_params_on` must be enabled for this parameter to function.

###

#### _newborn_protection_on_
```sh
newborn_protection_on = Boolean
```
Turns protection for newborn members on (`True`) or off (`False`).

This means that newborn members will be guaranteed to survive an extinction event (similar to elitism), but does not prevent newborn members from being killed by anti-elitism (see Sub-Section 8.3).  A newborn member's protection will expire after their newborn status expires (via the `newborn_expires` parameter).

If `newborn_params_on` is disabled, this parameter has no effect, `newborn_params_on` must be enabled for this parameter to function.

> This concludes the Adjustable Extinction Parameters section.

###
###

## **Section 9 - Adjustable Alternate Parameters**
Biological studies and the fossil record indicate that evolutionary activity increases post-extinction.  Due to the large loss in population, there is reduced competition among the survivors, which allows species to expand into niches that were previously occupied.  Using the biological world as inspiration, we can leverage these facts and utilize them to increase the evolutionary activity of individuals and decrease the selection pressure they face after an extinction event occurs.  This mimics biological extinction events and their bearing on evolution.

To incorporate these ideas into the extinction operator and your evolutionary algorithm, we need to alter some of the selection, crossover, and mutation parameters in the evolutionary algorithm after an extinction event occurs.  All of the following sub-sections contain parameters that are alternate parameters.  The alternate crossover and mutation parameters increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).  In order to decrease selection pressure, if the evolutionary algorithm employs tournament selection, the tournament size can be decreased upon the triggering of an extinction event (regardless of whether it is instant extinction or gradual extinction), and increased upon the completion of the repopulation phase (regardless of whether it is instant repopulation or gradual repopulation).  Selection pressure in your evolutionary algorithm can be further decreased by not allowing newborn members (see Sub-Section 8.9) to be killed during the selection phase for the parent population of the next generation.

These alternate parameters directly alter the tournament size, crossover probability, mutation probability, and mutation rate of the evolutionary algorithm, and as such these four values must be passed to the Extinction class directly each generation (see Sub-Sections 6.2 and 6.3), and are consequently returned back to the evolutionary algorithm after the Extinction class completes its operations each generation.

###

### **Sub-Section 9.1 - Basic Alternate Parameters**
If gradual extinction (see Sub-Section 8.1) or gradual repopulation (see Sub-Section 8.8) are in use, it is advised to also turn on alternate parameters, as not using them after an extinction event will most likely cause the algorithm to fair worse than the same parameter set run on instant extinction or instant repopulation.  The entire motivation behind using gradual extinction and gradual repopulation lies in the use of alternate parameters increasing the evolutionary activity of the evolutionary algorithm post-extinction, in order to reflect what happens in the natural world.

###

#### _alt_params_on_
```sh
alt_params_on = Boolean
```
Turns alternate parameters on (`True`) or off (`False`).

If alternate parameters are disabled, all four evolutionary parameters (the crossover probability, mutation probability, mutation rate, and the tournament selection size) passed from the evolutionary algorithm to the Extinction class will be returned unchanged back to the evolutionary algorithm each generation.  If alternate parameters are enabled and an extinction event or repopulation phase is in progress, then these values will change proportionally according to the population size in order to reflect what happens in biological extinction events.

If gradual extinction (see Sub-Section 8.1) or gradual repopulation (see Sub-Section 8.8) are in use, it is advised to also turn on alternate parameters, as not using them defeats the entire motivation behind using gradual extinction and gradual repopulation (the motivation being to increase the evolutionary activity of the evolutionary algorithm post-extinction).

###

### **Sub-Section 9.2 - Alternate Selection Parameters**
Alternate selection parameters function to decrease the selection pressure after the advent of an extinction event, after which the selection pressure will increase back to its original value upon completion of the repopulation phase.  Selection pressure in your evolutionary algorithm can be further decreased by not allowing newborn members (see Sub-Section 8.9) to be killed during the selection phase for the parent population of the next generation.

###

#### _alt_select_on_
```sh
alt_select_on = Boolean
```
Turns alternate selection parameters on (`True`) or off (`False`).

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).

###

#### _alt_tourn_size_
```sh
alt_tourn_size = int    Range: [0, tourn_size)
```
Specifies how much to decrease the tournament size by after the advent of an extinction event.

The tournament size will return back to its original value upon completion of the repopulation phase.  A value of `0` means the tournament size will not be altered upon the advent of an extinction event, and is equivalent to disabling `alt_select_on`.  This parameter is limited by the user's own tournament size passed in from their evolutionary algorithm (see Sub-Sections 6.2 and 6.3), and as such there is no reliable error checking for this parameter.

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).  Additionally, if `alt_select_on` is disabled, this parameter has no effect, `alt_select_on` must be enabled for this parameter to function.

###

### **Sub-Section 9.3 - Alternate Crossover Parameters**
Alternate crossover parameters increase the probability of crossover between members during child production.

The alternate crossover parameters increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).

###

#### _alt_xo_on_
```sh
alt_xo_on = Boolean
```
Turns alternate crossover parameters on (`True`) or off (`False`).

If this parameter is enabled, the crossover probability will increase by `alt_xo_prob` after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).  If this parameter is disabled (or if alternate parameters are disabled via the `alt_params_on` parameter), the crossover probability will not change during the course of the evolutionary algorithm's run.

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).

###

#### _alt_xo_prob_
```sh
alt_xo_prob = float    Range: [0.00, 1.00]
```
Specifies how much to increase the probability of crossover occurring by (crossover probability comes into play during the child production phase of the evolutionary algorithm).

A value of `1.00` means the probability of crossover occurring during child production is guaranteed.  A value of `0.00` means the crossover probability will not be altered upon the advent of an extinction event, and is equivalent to disabling `alt_xo_on`.

The crossover probability will increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).  Additionally, if `alt_xo_on` is disabled, this parameter has no effect, `alt_xo_on` must be enabled for this parameter to function.

###

### **Sub-Section 9.4 - Alternate Mutation Parameters**
Alternate mutation parameters increase the mutability of members during child production (both the probability and the rate of mutation).

The alternate mutation parameters increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).

###

#### _alt_mut_on_
```sh
alt_mut_on = Boolean
```
Turns alternate mutation parameters on (`True`) or off (`False`).

If this parameter is enabled, the mutation probability and mutation rate will increase by `alt_mut_prob` and `alt_mut_rate`, respectively, after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).  If this parameter is disabled (or if alternate parameters are disabled via the `alt_params_on` parameter), neither the mutation probability, nor the mutation rate will change during the course of the evolutionary algorithm's run.

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).

###

#### _alt_mut_prob_
```sh
alt_mut_prob = float    Range: [0.00, 1.00]
```
Specifies how much to increase the probability of mutation occurring by (mutation probability comes into play during the child production phase of the evolutionary algorithm).

A value of `1.00` means the probability of mutation occurring during child production is guaranteed.  A value of `0.00` means the mutation probability will not be altered upon the advent of an extinction event, and is equivalent to disabling `alt_mut_on`.

The mutation probability will increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).  Additionally, if `alt_mut_on` is disabled, this parameter has no effect, `alt_mut_on` must be enabled for this parameter to function.

###

#### _alt_mut_rate_
```sh
alt_mut_rate = float    Range: [0.00, 1.00]
```
Specifies how much to increase the rate of mutation by (mutation rate comes into play during the child production phase of the evolutionary algorithm).

A value of `0.00` means the mutation rate will not be altered upon the advent of an extinction event, and is equivalent to disabling `alt_mut_on`.

The mutation rate will increase after an extinction event (or slowly increase during a gradual extinction event, proportional to the duration and type of gradual extinction), and decrease after the population has been repopulated back to its pre-extinction level (or slowly decrease during gradual repopulation, proportional to the duration and type of gradual extinction).

If `alt_params_on` is disabled, this parameter has no effect, `alt_params_on` must be enabled for this parameter to function (see Sub-Section 9.1).  Additionally, if `alt_mut_on` is disabled, this parameter has no effect, `alt_mut_on` must be enabled for this parameter to function.

> This concludes the Adjustable Alternate Parameters section.
