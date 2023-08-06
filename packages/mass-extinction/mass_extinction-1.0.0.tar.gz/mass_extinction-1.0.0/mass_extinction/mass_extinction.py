'''
Biologically-Inspired Mass Extinction in Evolutionary Algorithms
Author: Kaelan Engholdt
Version: 05/26/2021

A biologically-inspired mass extinction operator for use in evolutionary algorithms.
Executes extinction events and methods of repopulation via parameterized settings found in 'ext_params.py'.
Users may save extinction parameter sets by adding additional 'if' code blocks to the '_saved_parameters' method.
Adjustable parameters are found in 'ext_params.py', consult the 'README.md' for more information.

Note: Due to the problem-specific nature of evolutionary algorithms, minor parts of this class must be finished by
      the user. Follow the instructions in Section 7 of the 'README.md' to integrate this class successfully.

'''

# TODO user must copy this file and place it in the same directory as their evolutionary algorithm

from sys import exit
from random import uniform
from math import log

import ext_params as ep
import ext_types as et


class Extinction:
    def __init__(self):
        pass
    
    def main(self, population, evolution_params, logpath, saved_idx=0):
        '''
        Description
        ----------
        Main method, handles the top level functionality of the Extinction class.
        
        Parameters
        ----------
        :param population : the sorted parent population
            :type : list
        
        :param evolution_params : holds the values needed from the user's evolutionary algorithm
            :type : list of the form [current_gen, max_gens, xo_prob, mut_prob, mut_rate, tourn_size]
        
        :param logpath : the absolute path to the log file, where information for the current run is stored
            :type : str
        
        :param saved_idx : the index into the set of extinction parameters saved in the '_saved_parameters' method
            :type : int
        
        Return Values
        ----------
        :return : the altered population, must be resorted by the user after it is returned to their algorithm
            :type : list
        
        :return : the crossover probability, possibly altered by an extinction event or repopulation
            :type : float
        
        :return : the mutation probability, possibly altered by an extinction event or repopulation
            :type : float
        
        :return : the mutation rate, possibly altered by an extinction event or repopulation
            :type : float
        
        :return : the tournament size, possibly altered by an extinction event or repopulation
            :type : int
        '''
        
        # define population size
        population_size = len(population)
        
        # define user parameters
        generation = evolution_params[0]             # the current generation
        maximum_generations = evolution_params[1]    # the total generations the evolutionary algorithm will run for
        xo_prob = evolution_params[2]                # the probability of crossover occurring
        mut_prob = evolution_params[3]               # the probability of mutation occurring
        mut_rate = evolution_params[4]               # the mutation rate
        tourn_size = evolution_params[5]             # the tournament size
        
        # set the parameters to be returned back to the evolutionary algorithm
        evolution_params = [xo_prob, mut_prob, mut_rate, tourn_size]
        
        # reset output string
        ep.ext_out_str = ""
        
        # if generations are zero-indexed, indicate as such
        if generation == 0:
            # indicate this evolutionary algorithm uses zero-indexed generations
            ep.ext_gens_zeroed = True
        
        # if generations are zero-indexed, remedy this issue
        if ep.ext_gens_zeroed:
            # increase generation count by 1 to avoid screwing up calculations
            generation += 1
        
        # perform extinction start-up operations upon first iteration
        if generation == 1 and ep.ext_operator_on:
            # change extinction parameters according to saved parameter index (uses 'ext_params.py' if no index given)
            self._saved_parameters(saved_idx)
            
            # check if extinction parameter values are valid
            self._error_checking(population_size, maximum_generations)
            
            # fetch all starting extinction parameters for the log file
            self._fetch_parameters()
            
            # initialize starting values
            ep.ext_original_size = population_size
            ep.ext_remaining_pop = []
            ep.ext_pop_dyn_pop = []
            ep.ext_in_progress = False
            ep.ext_gens_tracker = 1
            ep.ext_generations = 0
            ep.ext_gens_since_repop = 0
            ep.ext_values = []
            ep.p_ext_prob = ep.p_ext_base_prob
            ep.repop_in_progress = False
            ep.repop_gens_tracker = 1
            
            # if population dynamics are not enabled
            if not ep.ext_pop_dynamics_on:
                # set population dynamics strength to zero
                ep.ext_pop_dyn_strength = 0.00
        
        # indicate an extinction event has not occurred yet this generation
        ep.ext_occurred = False
        
        # define list to hold all members that are not considered elite members
        non_elite_pop = []
        
        # clear the elite population from the previous generation
        del ep.ext_elite_pop[:]
        
        # use elitism, if enabled
        if ep.ext_elite_on and ep.ext_operator_on:
            # determine the number of members to be kept
            preserve = int(ep.ext_elite_percent * ep.ext_original_size)
            
            # since elitism is in use, at least one member must be kept
            if preserve < 1:
                preserve = 1
            
            # elitism cannot preserve members beyond the population size
            if preserve > population_size:
                preserve = population_size
            
            # if elitism targets members at the front of the population list
            if ep.ext_sort_order:
                # add elite members to their own population
                ep.ext_elite_pop.extend(population[:preserve])
                
                # add remaining members to their own population
                non_elite_pop.extend(population[preserve:])
            
            # if elitism targets members at the end of the population list
            else:
                # add elite members to their own population
                ep.ext_elite_pop.extend(population[-preserve:])
                
                # add remaining members to their own population
                non_elite_pop.extend(population[:-preserve])
        
        # if elitism isn't in use
        else:
            # set the non-elite population equal to the total population
            non_elite_pop.extend(population)
        
        # clear the remaining population from the previous generation
        del ep.ext_remaining_pop[:]
        
        # clear the newborn population from the previous generation
        del ep.newborn_pop[:]
        
        # use newborn parameters, if enabled
        if ep.newborn_params_on and ep.ext_operator_on:
            # if the evolutionary algorithm uses the DEAP library
            if ep.ext_uses_DEAP:
                # check each member in the elite population for newborn status
                for member in ep.ext_elite_pop:
                    # if the member is a newborn
                    if member[1]:
                        # increase the number of generations this member has been a newborn by 1
                        member[2] += 1
                        
                        # if the newborn member is old enough to become a normal member
                        if member[2] > ep.newborn_expires:
                            # switch the member from a newborn to a normal member
                            member[1] = False
                            member[2] = 0
                
                # check each member in the non-elite population for newborn status
                for member in non_elite_pop:
                    # if the member is a newborn
                    if member[1]:
                        # increase the number of generations this member has been a newborn by 1
                        member[2] += 1
                        
                        # if the newborn member is old enough to become a normal member
                        if member[2] > ep.newborn_expires:
                            # switch the member from a newborn to a normal member
                            member[1] = False
                            member[2] = 0
                            
                            # add the member to the remaining population
                            ep.ext_remaining_pop.append(member)
                        
                        # if the newborn member is not old enough to become a normal member
                        else:
                            # if newborn protection is enabled
                            if ep.newborn_protection_on:
                                # add the member to the newborn population
                                ep.newborn_pop.append(member)
                            
                            # if newborn protection is disabled
                            else:
                                # add the member to the remaining population
                                ep.ext_remaining_pop.append(member)
                    
                    # if the member is not a newborn
                    else:
                        # add the member to the remaining population
                        ep.ext_remaining_pop.append(member)
            
            # if the evolutionary algorithm does not use the DEAP library
            else:
                # check each member in the elite population for newborn status
                for member in ep.ext_elite_pop:
                    # if the member is a newborn
                    if member.ext_is_newborn:
                        # increase the number of generations this member has been a newborn by 1
                        member.ext_newborn_gens += 1
                        
                        # if the newborn member is old enough to become a normal member
                        if member.ext_newborn_gens > ep.newborn_expires:
                            # switch the member from a newborn to a normal member
                            member.ext_is_newborn = False
                            member.ext_newborn_gens = 0
                
                # check each member in the non-elite population for newborn status
                for member in non_elite_pop:
                    # if the member is a newborn
                    if member.ext_is_newborn:
                        # increase the number of generations this member has been a newborn by 1
                        member.ext_newborn_gens += 1
                        
                        # if the newborn member is old enough to become a normal member
                        if member.ext_newborn_gens > ep.newborn_expires:
                            # switch the member from a newborn to a normal member
                            member.ext_is_newborn = False
                            member.ext_newborn_gens = 0
                            
                            # add the member to the remaining population
                            ep.ext_remaining_pop.append(member)
                        
                        # if the newborn member is not old enough to become a normal member
                        else:
                            # if newborn protection is enabled
                            if ep.newborn_protection_on:
                                # add the member to the newborn population
                                ep.newborn_pop.append(member)
                            
                            # if newborn protection is disabled
                            else:
                                # add the member to the remaining population
                                ep.ext_remaining_pop.append(member)
                    
                    # if the member is not a newborn
                    else:
                        # add the member to the remaining population
                        ep.ext_remaining_pop.append(member)
        
        # if newborn parameters aren't in use
        else:
            # set the remaining population equal to the total population
            ep.ext_remaining_pop.extend(non_elite_pop)
        
        # check if the extinction operator will be turned off, if enabled
        if ep.ext_end_extinction and ep.ext_operator_on:
            # check if the current generation has passed the 'ext_end_percent' generation point
            if generation > int(ep.ext_end_percent * maximum_generations):
                # turn the extinction operator off
                ep.ext_operator_on = False
        
        # if the extinction operator is on, repopulation is not in progress, and an extinction event is not in progress
        if ep.ext_operator_on and not ep.repop_in_progress and not ep.ext_in_progress:
            # uses interval extinction, if enabled
            if ep.interval_extinction_on:
                # determine if an extinction event occurs this generation using interval extinction
                self._interval_extinction(generation)
            
            # uses probabilistic extinction, if enabled, and an extinction event hasn't occurred yet
            if ep.prob_extinction_on and not ep.ext_occurred:
                # check safeguard, proceed if sufficient generations have passed since last extinction event
                if ep.ext_generations >= ep.ext_safeguard:
                    # determine if an extinction event occurs this generation using probabilistic extinction
                    self._probabilistic_extinction(generation)
            
            # uses fitness extinction, if enabled, and an extinction event hasn't occurred yet
            if ep.fit_extinction_on and not ep.ext_occurred:
                # check safeguard, proceed if sufficient generations have passed since last extinction event
                if ep.ext_generations >= ep.ext_safeguard:
                    # determine if an extinction event occurs this generation using fitness extinction
                    self._fitness_extinction(population, population_size, generation)
        
        # if an extinction event occurred this generation
        if ep.ext_occurred:
            # indicate that an extinction event is now in progress
            ep.ext_in_progress = True
            
            # reset the number of generations since the last extinction event
            ep.ext_generations = 0
            
            # define original population size before the extinction event occurred
            ep.ext_original_size = population_size
            
            # use anti-elitism, if enabled, for the first generation of the extinction event
            if ep.ext_anti_elite_on and ep.ext_anti_elite_percent != 0 and ep.ext_gens_tracker == 1:
                # determine the number of members to be terminated
                terminate = int(ep.ext_anti_elite_percent * ep.ext_original_size)
                
                # since anti-elitism is in use, at least one member must be terminated
                if terminate < 1:
                    terminate = 1
                
                # anti-elitism cannot terminate members beyond the population size
                if terminate > population_size:
                    terminate = population_size
                
                # if there are sufficient members in the remaining population to be killed by anti-elitism
                if terminate <= len(ep.ext_remaining_pop):
                    # if anti-elitism targets members at the front of the remaining population list
                    if not ep.ext_sort_order:
                        # kill all members to be terminated
                        del ep.ext_remaining_pop[:terminate]
                    
                    # if anti-elitism targets members at the end of the remaining population list
                    else:
                        # kill all members to be terminated
                        del ep.ext_remaining_pop[-terminate:]
                
                # if there are not sufficient members in the remaining population to be killed by anti-elitism
                else:
                    # kill all members in the remaining population
                    del ep.ext_remaining_pop[:]
                
                # log anti-elitism deaths
                ep.ext_out_str += "Anti-Elitism Deaths: {}\n".format(terminate)
        
        # if an extinction event did not occur
        else:
            # increment the number of generations since the advent of the last extinction event
            ep.ext_generations += 1
        
        # if an extinction event is currently in progress
        if ep.ext_in_progress:
            # decrease the remaining population according to the extinction parameters
            population, evolution_params = self._extinction(generation, evolution_params)
        
        # if the population is repopulating
        if ep.repop_in_progress:
            # increase the population according to the repopulation parameters
            population, evolution_params = self._repopulation(population, generation, evolution_params)
            
            # reset the number of generations since the previous repopulation finished
            ep.ext_gens_since_repop = 0
        
        # if the population has finished repopulating
        else:
            # increment the number of generations since repopulation finished
            ep.ext_gens_since_repop += 1
        
        # if an extinction event is currently in progress or the population is repopulating
        if ep.ext_in_progress or ep.repop_in_progress:
            # end the output string
            ep.ext_out_str += "\n"
        
        # if print statements are enabled, print all information from this generation to the console
        if ep.ext_print_on and ep.ext_out_str != "":
            print(ep.ext_out_str)
        
        # open the log file and save all information from this generation
        log_file = open(logpath, 'a')
        log_file.write(ep.ext_out_str)
        log_file.close()
        
        # return the altered population (unsorted and unevaluated) and the altered evolutionary algorithm parameters
        return population, evolution_params[0], evolution_params[1], evolution_params[2], evolution_params[3]
    
    def _interval_extinction(self, generation):
        '''
        Description
        ----------
        Determines whether an extinction event occurs or not by utilizing interval extinction.
        
        Parameters
        ----------
        :param generation : the current generation
            :type : int
        '''
        
        # check if the extinction interval lands on this generation
        if (ep.i_ext_interval == 1) or (ep.ext_gens_since_repop % (ep.i_ext_interval - 1) == 0 and
                                        ep.ext_gens_since_repop != 0):
            # indicate an extinction event occurred this generation
            ep.ext_occurred = True
            
            # if probabilistic extinction is enabled and probability resets upon the advent of any extinction event
            if ep.prob_extinction_on and ep.p_ext_always_resets:
                # reset the current probability of extinction back to the base probability
                ep.p_ext_prob = ep.p_ext_base_prob
            
            # log the advent of the extinction event
            ep.ext_out_str += "\n----------\n"
            ep.ext_out_str += "Interval Extinction Occurred: Generation {}\n".format(generation)
    
    def _probabilistic_extinction(self, generation):
        '''
        Description
        ----------
        Determines whether an extinction event occurs or not by utilizing probabilistic extinction.
        
        Parameters
        ----------
        :param generation : the current generation
            :type : int
        '''
        
        # check if the extinction interval lands on this generation
        if (ep.p_ext_interval == 1) or (ep.ext_gens_since_repop % (ep.p_ext_interval - 1) == 0 and
                                        ep.ext_gens_since_repop != 0):
            # determine if an extinction event occurs based on the current probability of extinction
            if uniform(0, 1) < ep.p_ext_prob:
                # indicate an extinction event occurred this generation
                ep.ext_occurred = True
                
                # log the advent of the extinction event
                ep.ext_out_str += "\n----------\n"
                ep.ext_out_str += "Probabilistic Extinction Occurred: Generation {}\n".format(generation)
            
            # if an extinction event occured this generation
            if ep.ext_occurred:
                # reset the current probability of extinction back to the base probability
                ep.p_ext_prob = ep.p_ext_base_prob
            
            # if an extinction event did not occur this generation
            else:
                # increase probability of an extinction event occurring next generation
                ep.p_ext_prob += ep.p_ext_prob_inc
    
    def _fitness_extinction(self, population, population_size, generation):
        '''
        Description
        ----------
        Determines whether an extinction event occurs or not by utilizing fitness extinction.
        
        Parameters
        ----------
        :param population : the sorted parent population
            :type : list
        
        :param population_size : the current size of the population
            :type : int
        
        :param generation : the current generation
            :type : int
        '''
        
        # check if the extinction interval lands on this generation
        if (ep.f_ext_interval == 1) or (ep.ext_gens_since_repop % (ep.f_ext_interval - 1) == 0 and
                                        ep.ext_gens_since_repop != 0):
            # determine the number of members required to pass the percentage of fitness improvement
            fit_members = int(ep.f_ext_pop_percent * population_size)
            
            # define the number of members in the population that pass the percentage of fitness improvement
            pop_fit = 0
            
            # TODO user must finish this code chunk, code instructions are found below
            '''
            1) Set 'pop_fit' equal to the number of members in the population whose fitness has improved by a
               percentage of at least 'f_ext_improve_percent' since the last interval check.
            '''
            
            # if there is not a sufficient number of fit members, extinction occurs
            if pop_fit < fit_members:
                # indicate an extinction event occurred this generation
                ep.ext_occurred = True
                
                # if probabilistic extinction is enabled and probability resets upon the advent of any extinction event
                if ep.prob_extinction_on and ep.p_ext_always_resets:
                    # reset the current probability of extinction back to the base probability
                    ep.p_ext_prob = ep.p_ext_base_prob
                
                # log the advent of the extinction event
                ep.ext_out_str += "\n----------\n"
                ep.ext_out_str += "Fitness Extinction Occurred: Generation {}\n".format(generation)
    
    def _extinction(self, generation, evolution_params):
        '''
        Description
        ----------
        Performs extinction, decreases the remaining population according to the extinction parameters.
        
        Parameters
        ----------
        :param generation : the current generation
            :type : int
        
        :param evolution_params : the evolutionary algorithm parameters to be possibly altered by extinction
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        
        Return Value
        ----------
        :return : the altered population, decreased in size according to the extinction parameters
            :type : list
        
        :return : the evolutionary algorithm parameters, possibly altered by extinction
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        '''
        
        # set the current total population size
        population_size = len(ep.ext_remaining_pop) + len(ep.ext_elite_pop) + len(ep.newborn_pop)
        
        # set the current remaining population size
        remaining_size = len(ep.ext_remaining_pop)
        
        # determine the number of members to be killed this generation
        kill_num = self._calculate(ep.ext_original_size, population_size, ep.ext_duration, ep.ext_kills_constant)
        
        # determine the number of members to be repopulated by population dynamics this generation
        repop_num = ep.ext_pop_dyn_pop.pop(0)
        
        # determine the actual number of members to be killed due to population dynamics
        actual_num = kill_num - repop_num
        
        # if the number of members to be killed by extinction exceeds the number of members in the remaining population
        if kill_num > remaining_size:
            # determine the maximum possible number of members that can be killed
            kill_num = remaining_size
        
        # if alternate parameters are in use
        if ep.alt_params_on:
            # slowly increase the evolutionary algorithm parameters to their heightened values
            evolution_params = self._alt_param_increase(actual_num, evolution_params)
        
        # if the least fit members will be killed by the extinction event
        if ep.ext_kills_least_fit:
            # if the least fit members are at the end of the remaining population
            if ep.ext_sort_order:
                # kill the least fit members
                del ep.ext_remaining_pop[-kill_num:]
            
            # if the least fit members are at the front of the remaining population
            else:
                # kill the least fit members
                del ep.ext_remaining_pop[:kill_num]
        
        # if members will be killed randomly by the extinction event
        else:
            # randomly kill members for extinction
            for i in range(kill_num):
                # kill the randomly selected member
                del ep.ext_remaining_pop[int(uniform(0, remaining_size - i))]
        
        # begin the output string
        ep.ext_out_str += "----------\n"
        
        # if using gradual extinction
        if ep.ext_duration != 1:
            # log the extinction information
            ep.ext_out_str += "Gen {} Gradual Extinction - Deaths: {}".format(generation, kill_num)
        
        # if using instant extinction
        else:
            # log the extinction information
            ep.ext_out_str += "Gen {} Instant Extinction - Deaths: {}".format(generation, kill_num)
        
        # if population dynamics are enabled
        if ep.ext_pop_dynamics_on:
            # if 'kill_num' was reduced due to size restrictions on the remaining population
            if actual_num + repop_num > kill_num:
                # set the maximum number of members that can be repopulated
                repop_num = abs(kill_num - actual_num)
            
            # randomly generate the appropriate amount of members to be repopulated
            repop_pop = self._random_repop(repop_num)
            
            # add all newly generated members to the remaining population
            ep.ext_remaining_pop.extend(repop_pop)
            
            # log the repopulation information
            ep.ext_out_str += " | Births: {} | Aggregate Deaths: {}".format(repop_num, kill_num - repop_num)
        
        # log the extinction information
        ep.ext_out_str += "\n"
        
        # if an extinction event is currently in progress
        if ep.ext_in_progress:
            # if this is the final generation for the extinction event, terminate it
            if ep.ext_gens_tracker == ep.ext_duration:
                # turn the extinction indicator off
                ep.ext_in_progress = False
                
                # reset the extinction event generational tracker
                ep.ext_gens_tracker = 1
                
                # end the output string
                ep.ext_out_str += "----------\n"
        
        # if the extinction event is still in progress
        if ep.ext_in_progress:
            # increment extinction event progress
            ep.ext_gens_tracker += 1
        
        # if the extinction event has run its course
        else:
            # set gradual repopulation variable
            ep.repop_in_progress = True
        
        # consolidate the altered population with the elite and newborn populations
        population = ep.ext_remaining_pop
        population.extend(ep.newborn_pop)
        population.extend(ep.ext_elite_pop)
        
        # return the total altered population and the altered evolutionary algorithm parameters
        return population, evolution_params
    
    def _repopulation(self, population, generation, evolution_params):
        '''
        Description
        ----------
        Performs repopulation, increases the population back to its original size according to the repopulation
        parameters.
        
        Parameters
        ----------
        :param population : the sorted parent population
            :type : list
        
        :param generation : the current generation
            :type : int
        
        :param evolution_params : the evolutionary algorithm parameters to be altered by repopulation
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        
        Return Value
        ----------
        :return : the altered population, increased in size according to repopulation parameters
            :type : list
        
        :return : the evolutionary algorithm parameters altered by repopulation
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        '''
        
        # if this is the first generation of repopulation
        if ep.repop_gens_tracker == 1:
            # if using gradual repopulation
            if ep.repop_duration != 1:
                # log the repopulation information
                ep.ext_out_str += "\n----------\n"
                ep.ext_out_str += "Gradual Repopulation Begins: Generation {}\n".format(generation)
                ep.ext_out_str += "----------\n"
            
            # if using instant repopulation
            else:
                # log the repopulation information
                ep.ext_out_str += "\n----------\n"
                ep.ext_out_str += "Instant Repopulation Begins: Generation {}\n".format(generation)
                ep.ext_out_str += "----------\n"
        
        # if this is not the first generation of repopulation
        else:
            # begin the output string
            ep.ext_out_str += "----------\n"
        
        # if using gradual repopulation
        if ep.repop_duration != 1:
            # log the repopulation information
            ep.ext_out_str += "Gen {} Gradual Repopulation - ".format(generation)
        
        # if using instant repopulation
        else:
            # log the repopulation information
            ep.ext_out_str += "Gen {} Instant Repopulation - ".format(generation)
        
        # set the current population size
        population_size = len(population)
        
        # define the child population
        child_population = []
        
        # determine the number of members to be repopulated this generation
        repop_num = self._calculate(ep.ext_original_size, population_size, ep.repop_duration, ep.repop_constant)
        
        # define the number of members to repopulate using elite members
        elite_num = 0
        
        # define the number of members to repopulate using surviving members
        survivor_num = 0
        
        # if using elite repopulation
        if ep.repop_use_elites:
            # determine the number of members to repopulate using elite members
            elite_num = int(repop_num * ep.repop_elite_percent)
            
            # log the repopulation information
            ep.ext_out_str += "Elites: {} | ".format(elite_num)
            
            # generate the children constructed from elite members
            elite_children = self._elite_repop(ep.ext_elite_pop, elite_num)
            
            # add the generated elite children to the child population
            child_population.extend(elite_children)
        
        # if using survivor repopulation
        if ep.repop_use_survivors:
            # determine the number of members to repopulate using surviving members
            survivor_num = int(repop_num * ep.repop_survivor_percent)
            
            # log the repopulation information
            ep.ext_out_str += "Survivors: {} | ".format(survivor_num)
            
            # generate the children constructed from surviving members
            survivor_children = self._survivor_repop(population, survivor_num)
            
            # add the generated survivor children to the child population
            child_population.extend(survivor_children)
        
        # determine the remaining number of members to be generated randomly
        rand_num = repop_num - (elite_num + survivor_num)
        
        # log the repopulation information
        ep.ext_out_str += "Random: {} | ".format(rand_num)
        ep.ext_out_str += "Total: {}\n".format(elite_num + survivor_num + rand_num)
        
        # randomly generate the remaining children
        rand_children = self._random_repop(rand_num)
        
        # add the generated random children to the child population
        child_population.extend(rand_children)
        
        # use newborn parameters, if enabled
        if ep.newborn_params_on:
            # if the evolutionary algorithm uses the DEAP library
            if ep.ext_uses_DEAP:
                # iterate through the child population and mark them as newborn members
                for member in child_population:
                    # indicate that the member is a newborn
                    member[1] = True
                    member[2] = 0
            
            # if the evolutionary algorithm does not use the DEAP library
            else:
                # iterate through the child population and mark them as newborn members
                for member in child_population:
                    # indicate that the member is a newborn
                    member.ext_is_newborn = True
                    member.ext_newborn_gens = 0
        
        # add all newly generated children to the parent population
        population.extend(child_population)
        
        # if alternate parameters are in use
        if ep.alt_params_on:
            # slowly decrease the alternate parameters back to their original values
            evolution_params = self._alt_param_decrease(repop_num, evolution_params)
        
        # if repopulation is currently in progress
        if ep.repop_in_progress:
            # if this is the final generation for repopulation, terminate it
            if ep.repop_gens_tracker == ep.repop_duration:
                # turn repopulation off
                ep.repop_in_progress = False
                
                # reset the repopulation generational tracker
                ep.repop_gens_tracker = 1
                
                # end the output string
                ep.ext_out_str += "----------\n"
        
        # if repopulation is still in progress
        if ep.repop_in_progress:
            # increment repopulation progress
            ep.repop_gens_tracker += 1
        
        # return the altered population (unsorted and unevaluated) and the altered evolutionary algorithm parameters
        return population, evolution_params
    
    def _elite_repop(self, elite_pop, elite_num):
        '''
        Description
        ----------
        Generates child members based on the elite members for the repopulate method.
        
        Parameters
        ----------
        :param elite_pop : the elite members of the population
            :type : list
        
        :param elite_num : the number of elite children to generate
            :type : int
        
        Return Value
        ----------
        :return : the children that have been generated from elite members
            :type : list
        '''
        
        # define the elite child population
        elite_children = []
        
        # TODO user must finish this code chunk, code instructions are found below
        '''
        1) Generate 'elite_num' amount of children via crossover by using elite members in the 'elite_pop' list.
        2) Add the generated children to the 'elite_children' list.
        3) Evaluate the fitness of all generated children now held in the 'elite_children' list.
        '''
        
        # return the elite children
        return elite_children
    
    def _survivor_repop(self, survivor_pop, survivor_num):
        '''
        Description
        ----------
        Generates child members based on the surviving members for the repopulate method.
        
        Parameters
        ----------
        :param survivor_pop : the surviving population left over from an extinction event
            :type : list
        
        :param survivor_num : the number of survivor children to generate
            :type : int
        
        Return Value
        ----------
        :return : the children that have been generated from surviving members
            :type : list
        '''
        
        # define the survivor child population
        survivor_children = []
        
        # TODO user must finish this code chunk, code instructions are found below
        '''
        1) Generate 'survivor_num' amount of children via crossover using surviving members in the 'survive_pop' list.
        2) Add the generated children to the 'survivor_children' list.
        3) Evaluate the fitness of all generated children now held in the 'survivor_children' list.
        '''
        
        # return the survivor children
        return survivor_children
    
    def _random_repop(self, rand_num):
        '''
        Description
        ----------
        Generates random members for the repopulate method.
        
        Parameters
        ----------
        :param rand_num : the number of random members to generate
            :type : int
        
        Return Value
        ----------
        :return : the members that have been generated randomly
            :type : list
        '''
        
        # define the random population
        rand_members = []
        
        # TODO user must finish this code chunk, code instructions are found below
        '''
        1) Generate 'rand_num' amount of members using a user-defined method of randomly generating members.
        2) Add the generated members to the 'rand_members' list.
        3) Evaluate the fitness of all generated members now held in the 'rand_members' list.
        '''
        
        # return the random members
        return rand_members
    
    def _calculate(self, carrying_capacity, population_size, duration, constant):
        '''
        Description
        ----------
        Calculates the number of members to kill or repopulate this generation.
        
        Parameters
        ----------
        :param carrying_capacity : the maximum population size
            :type : int
        
        :param population_size : the current size of the population
            :type : int
        
        :param duration : the number of generations it will take for extinction or repopulation to complete
            :type : int
        
        :param constant : indicates if a constant value will be used instead of a logarithmic value
            :type : Boolean
        
        Return Value
        ----------
        :return : the number of members to kill or repopulate this generation
            :type : int
        '''
        
        # if this is the first generation of extinction or repopulation
        if (ep.ext_gens_tracker == 1 and ep.ext_in_progress) or (ep.repop_gens_tracker == 1 and ep.repop_in_progress):
            # if calculating for an extinction event
            if ep.ext_gens_tracker == 1 and ep.ext_in_progress:
                # adjust the population size to what it would be after a simulated extinction event
                population_size = population_size - int(ep.ext_percent * population_size)
            
            # cast all relevant arguments to floats
            carrying_capacity = float(carrying_capacity)
            population_size = float(population_size)
            duration = float(duration)
            
            # clear all old birth/death values
            ep.ext_values = ep.ext_values[:]
            
            # calculate the total number of members to be killed
            killed = int(ep.ext_percent * ep.ext_original_size)
            
            # calculate the total number of members to be repopulated
            repopulated = ep.ext_original_size - population_size
            
            # if the duration lies between one and seven generations or a constant value will be used
            if (1 <= duration <= 7) or constant:
                # calculate all birth/death values for the duration of the extinction event or repopulation phase
                for gen in range(int(duration)):
                    # if the values are being built for an extinction event
                    if ep.ext_gens_tracker == 1 and ep.ext_in_progress:
                        # calculate the number of members to remove this generation of the duration
                        members = int(killed / duration)
                        
                        # append the number of members to the death values
                        ep.ext_values.append(members)
                    
                    # if the values are being built for repopulation
                    if ep.repop_gens_tracker == 1 and ep.repop_in_progress:
                        # calculate the number of members to add this generation of the duration
                        members = int(repopulated / duration)
                        
                        # append the number of members to the birth values
                        ep.ext_values.append(members)
            
            # if the duration is at least eight generations and logarithmic values will be used
            else:
                # calculate all birth/death values for the duration of the extinction event or repopulation phase
                for gen in range(int(duration)):
                    # calculate the growth/decay rate of the population
                    rate = (1 / duration) * log((carrying_capacity * population_size), duration) - 0.5 * \
                                              log((population_size / carrying_capacity), duration)
                    
                    # calculate the number of members to add/remove this generation of the duration
                    members = int(rate * (1 - (population_size / carrying_capacity)) * population_size)
                    
                    # append the number of members to the birth/death values
                    ep.ext_values.append(members)
                    
                    # increment the current population size as if the population actually had those members added in
                    population_size += members
            
            # if the values are being built for an extinction event
            if ep.ext_gens_tracker == 1 and ep.ext_in_progress:
                # determine the fraction of individuals that are not zero
                recalculator = len([x for x in ep.ext_values if x is not 0]) / float(len(ep.ext_values))
                
                # ensure the recalculator is not zero
                if recalculator is not 0:
                    # alter each value
                    for idx in range(len(ep.ext_values)):
                        # recalculate the value to be smaller to extend the length of repopulation
                        ep.ext_values[idx] = int(ep.ext_values[idx] * recalculator)
                
                # define loop variable
                invalid = True
                
                # define list index to be altered
                idx = 0
                
                # due to truncation, the death values may be lacking in a few members
                while (invalid):
                    # check if the sum of the death values is equal to the total number of members to be killed
                    if sum(ep.ext_values) != killed:
                        # increment the number of members to be killed at the current index
                        ep.ext_values[idx] += 1
                        
                        # increment the list index
                        idx += 1
                        
                        # ensure the list index has not gone beyond the length of the list
                        if idx >= len(ep.ext_values):
                            # reset list index
                            idx = 0
                    
                    # if all death values are correct
                    else:
                        invalid = False
                
                # for each death value, calculate extra members to be killed for population dynamics
                for amount in ep.ext_values:
                    # calculate additional members to be killed for population dynamics
                    ep.ext_pop_dyn_pop.append(int(amount * ep.ext_pop_dyn_strength))
                
                # reverse the order of the population dynamics list to accurately reflect a biological ecosystem
                ep.ext_pop_dyn_pop.reverse()
                
                # if the extinction event gets stronger as it progresses
                if ep.ext_virulence:
                    # reverse the order of the death values list so that the extinction event gets stronger
                    ep.ext_values.reverse()
                    
                    # reverse the order of the population dynamics list to accurately reflect a biological ecosystem
                    ep.ext_pop_dyn_pop.reverse()
                
                # for each death value, increment it by the amount given by population dynamics
                for idx in range(len(ep.ext_values)):
                    # increment the death value by the amount given by population dynamics
                    ep.ext_values[idx] += ep.ext_pop_dyn_pop[idx]
            
            # if the values are being built for repopulation
            if ep.repop_gens_tracker == 1 and ep.repop_in_progress:
                # determine the fraction of individuals that are not zero
                recalculator = len([x for x in ep.ext_values if x is not 0]) / float(len(ep.ext_values))
                
                # ensure the recalculator is not zero
                if recalculator is not 0:
                    # alter each value
                    for idx in range(len(ep.ext_values)):
                        # recalculate the value to be smaller to extend the length of repopulation
                        ep.ext_values[idx] = int(ep.ext_values[idx] * recalculator)
                
                # define loop variable
                invalid = True
                
                # define list index to be altered
                idx = 0
                
                # due to truncation, the birth values may be lacking in a few members
                while (invalid):
                    # check if the sum of the birth values is equal to the total number of members to be repopulated
                    if sum(ep.ext_values) != repopulated:
                        # increment the number of members to be repopulated at the current index
                        ep.ext_values[idx] += 1
                        
                        # increment the list index
                        idx += 1
                        
                        # ensure the list index has not gone beyond the length of the list
                        if idx >= len(ep.ext_values):
                            # reset list index
                            idx = 0
                    
                    # if all birth values are correct
                    else:
                        invalid = False
                
                # if repopulation gets stronger as it progresses
                if ep.repop_growth:
                    # reverse the order of the list so that repopulation gets stronger
                    ep.ext_values.reverse()
        
        # return the number of members to kill or repopulate this generation
        return ep.ext_values.pop(0)
    
    def _alt_param_increase(self, kill_num, evolution_params):
        '''
        Description
        ----------
        Increases the evolutionary algorithm parameters as extinction causes the population size to decrease.
        
        Parameters
        ----------
        :param kill_num : the number of members to be killed this generation
            :type : int
        
        :param evolution_params : the evolutionary algorithm parameters to be altered by extinction
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        
        Return Value
        ----------
        :return : the evolutionary algorithm parameters altered by extinction
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        '''
        
        # determine the killed population size through a simulated extinction event
        killed_pop = int(ep.ext_percent * ep.ext_original_size)
        
        # cast the killed population amount to a float
        killed_pop = float(killed_pop)
        
        # if alternate selection parameters are in use and this is the first generation of extinction
        if ep.alt_select_on and (ep.ext_gens_tracker == 1):
            # decrease the tournament size to reduce the selection pressure
            evolution_params[3] -= ep.alt_tourn_size
        
        # if alternate crossover parameters are in use
        if ep.alt_xo_on:
            # calculate how much to increase the crossover probability by for this generation
            alt_xo_prob_inc = ep.alt_xo_prob * (kill_num / killed_pop)
            
            # increase the crossover probability
            evolution_params[0] += alt_xo_prob_inc
        
        # if alternate mutation parameters are in use
        if ep.alt_mut_on:
            # calculate how much to increase the mutation probability by for this generation
            alt_mut_prob_inc = ep.alt_mut_prob * (kill_num / killed_pop)
            
            # increase the mutation probability
            evolution_params[1] += alt_mut_prob_inc
            
            # calculate how much to increase the mutation rate by for this generation
            alt_mut_rate_inc = ep.alt_mut_rate * (kill_num / killed_pop)
            
            # increase the mutation probability
            evolution_params[2] += alt_mut_rate_inc
        
        # return the altered evolutionary algorithm parameters
        return evolution_params
    
    def _alt_param_decrease(self, repop_num, evolution_params):
        '''
        Description
        ----------
        Decreases the evolutionary algorithm parameters as repopulation causes the population size to increase.
        
        Parameters
        ----------
        :param repop_num : the number of members to be repopulated this generation
            :type : int
        
        :param evolution_params : the evolutionary algorithm parameters to be altered by repopulation
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        
        Return Value
        ----------
        :return : the evolutionary algorithm parameters altered by repopulation
            :type : list of the form [xo_prob, mut_prob, mut_rate, tourn_size]
        '''
        
        # determine the killed population size through a simulated extinction event
        killed_pop = int(ep.ext_percent * ep.ext_original_size)
        
        # cast the killed population amount to a float
        killed_pop = float(killed_pop)
        
        # if alternate selection parameters are in use and this is the final generation of repopulation
        if ep.alt_select_on and (ep.repop_gens_tracker == ep.repop_duration):
            # increase the tournament size back to its original value to increase the selection pressure
            evolution_params[3] += ep.alt_tourn_size
        
        # if alternate crossover parameters are in use
        if ep.alt_xo_on:
            # calculate how much to decrease the crossover probability by for this generation
            alt_xo_prob_dec = ep.alt_xo_prob * (repop_num / killed_pop)
            
            # decrease the crossover probability
            evolution_params[0] -= alt_xo_prob_dec
        
        # if alternate mutation parameters are in use
        if ep.alt_mut_on:
            # calculate how much to decrease the mutation probability by for this generation
            alt_mut_prob_dec = ep.alt_mut_prob * (repop_num / killed_pop)
            
            # decrease the mutation probability
            evolution_params[1] -= alt_mut_prob_dec
            
            # calculate how much to decrease the mutation rate by for this generation
            alt_mut_rate_dec = ep.alt_mut_rate * (repop_num / killed_pop)
            
            # decrease the mutation rate
            evolution_params[2] -= alt_mut_rate_dec
        
        # return the altered evolutionary algorithm parameters
        return evolution_params
    
    def _saved_parameters(self, saved_idx):
        '''
        Description
        ----------
        Holds saved extinction parameter sets. Consult Sub-Section 6.5 of the 'README.md' for more information and
        details regarding saving new parameter sets.
        
        Parameters
        ----------
        :param saved_idx : the index into the set of extinction parameters saved in this method
            :type : int
        '''
        
        # if the testing parameter sets in 'ext_types.py' will be used
        if ep.ext_testing_on:
            # call the given extinction parameter set
            et.saved_params(saved_idx)
        
        # if the user defined parameter sets will be used
        else:
            # use default values found in 'ext_params.py'
            if saved_idx == 0:
                pass
            
            # TODO user may copy and paste parameter set description printed via 'ext_print_on' in 'ext_params.py'
            if saved_idx == 1:
                # TODO user may copy and paste parameters printed via 'ext_print_on' in 'ext_params.py'
                pass
    
    def _fetch_parameters(self):
        '''
        Description
        ----------
        Takes all extinction parameters used in the current run and stores them in the form of Python code.
        '''
        
        # begin the output string
        ep.ext_out_str = "\nExtinction Operator Parameters:\n"
        ep.ext_out_str += "----------------------------------------------\n"
        ep.ext_out_str += "'''\n"
        
        # if the extinction operator is on, automatically generate a description based on current extinction parameters
        if ep.ext_operator_on:
            # generate the extinction description
            ep.ext_out_str += "Extinction:\n"
            
            # generate the extinction percentage description
            ep.ext_out_str += "    Kills {}% of the population\n".format(ep.ext_percent * 100)
            
            # generate the extinction duration description
            if ep.ext_duration == 1:
                ep.ext_out_str += "    Instant extinction\n"
            else:
                ep.ext_out_str += "    Gradual extinction over {} generations\n".format(ep.ext_duration)
            
            if (ep.ext_duration > 7) and not ep.ext_kills_constant:
                ep.ext_out_str += "    Logarithmic rate of extinction, "
                
                if ep.ext_virulence:
                    ep.ext_out_str += "gets stronger over the duration\n"
                else:
                    ep.ext_out_str += "gets weaker over the duration\n"
            elif ep.ext_duration != 1:
                ep.ext_out_str += "    Constant rate of extinction\n"
            
            if ep.ext_kills_least_fit:
                ep.ext_out_str += "    Least fit members are killed\n"
            else:
                ep.ext_out_str += "    Members are killed randomly\n"
            
            # generate the population dynamics description
            if ep.ext_pop_dynamics_on:
                ep.ext_out_str += "    Population dynamics enabled, {}% strength\n".format(ep.ext_pop_dyn_strength * 100)
            else:
                ep.ext_out_str += "    Population dynamics disabled\n"
            
            # generate the end of extinction description
            if ep.ext_end_extinction:
                ep.ext_out_str += "    Extinction possible until {}% of total generations\n" \
                    .format(ep.ext_end_percent * 100)
            else:
                ep.ext_out_str += "    Extinction possible for duration of run\n"
            
            # generate the safeguard description
            if ep.ext_safeguard == 0:
                ep.ext_out_str += "    Safeguard disabled\n"
            else:
                ep.ext_out_str += "    Safeguard: {} generations\n".format(ep.ext_safeguard)
            
            # generate the elitism description
            if ep.ext_elite_on:
                ep.ext_out_str += "    Elitism: {}% of the population\n".format(ep.ext_elite_percent * 100)
            else:
                ep.ext_out_str += "    Elitism disabled\n"
            
            # generate the anti-elitism description
            if ep.ext_anti_elite_on:
                ep.ext_out_str += "    Anti-elitism: {}% of the population\n".format(ep.ext_anti_elite_percent * 100)
            else:
                ep.ext_out_str += "    Anti-elitism disabled\n"
            
            # generate the interval extinction description
            if ep.interval_extinction_on:
                ep.ext_out_str += "    Interval Extinction:\n"
                
                if ep.i_ext_interval == 1:
                    ep.ext_out_str += "        Extinction occurs every generation\n"
                else:
                    ep.ext_out_str += "        Extinction occurs every {} generations\n".format(ep.i_ext_interval)
            
            # generate the probabilistic extinction description
            if ep.prob_extinction_on:
                ep.ext_out_str += "    Probabilistic Extinction:\n"
                
                if ep.p_ext_interval == 1:
                    ep.ext_out_str += "        Extinction has a chance to occur every generation\n"
                else:
                    ep.ext_out_str += "        Extinction has a chance to occur every {} generations\n" \
                        .format(ep.p_ext_interval)
                
                ep.ext_out_str += "        Base probability to occur: {}%\n".format(ep.p_ext_base_prob * 100)
                ep.ext_out_str += "        Probability increase: {}%\n".format(ep.p_ext_prob_inc * 100)
            
            # generate the fitness extinction description
            if ep.fit_extinction_on:
                ep.ext_out_str += "    Fitness Extinction:\n"
                
                if ep.f_ext_interval == 1:
                    ep.ext_out_str += "        Extinction has a chance to occur every generation\n"
                else:
                    ep.ext_out_str += "        Extinction has a chance to occur every {} generations\n" \
                        .format(ep.f_ext_interval)
                
                ep.ext_out_str += "        {}% of the population must improve in fitness by at least {}%\n" \
                    .format(ep.f_ext_pop_percent * 100, ep.f_ext_improve_percent)
            
            # generate the repopulation description
            ep.ext_out_str += "Repopulation:\n"
            
            if ep.repop_duration == 1:
                ep.ext_out_str += "    Instant repopulation\n"
            else:
                ep.ext_out_str += "    Gradual repopulation over {} generations\n".format(ep.repop_duration)
            
            if (ep.repop_duration > 7) and not ep.repop_constant:
                ep.ext_out_str += "    Logarithmic rate of repopulation, "
                
                if ep.repop_growth:
                    ep.ext_out_str += "gets stronger over the duration\n"
                else:
                    ep.ext_out_str += "gets weaker over the duration\n"
            elif ep.repop_duration != 1:
                ep.ext_out_str += "    Constant rate of repopulation\n"
            
            if ep.repop_use_elites:
                ep.ext_out_str += "    Elite children comprise {}% of repopulated members\n" \
                    .format(ep.repop_elite_percent * 100)
            
            if ep.repop_use_survivors:
                ep.ext_out_str += "    Survivor children comprise {}% of repopulated members\n" \
                    .format(ep.repop_survivor_percent * 100)
            
            ep.ext_out_str += "    Random members comprise {}% of repopulated members\n" \
                .format((1 - (ep.repop_elite_percent + ep.repop_survivor_percent)) * 100)
            
            # generate the newborn description
            ep.ext_out_str += "Newborn Parameters:\n"
            
            if ep.newborn_params_on:
                ep.ext_out_str += "    Newborn status expires after {} generations\n".format(ep.newborn_expires)
                
                if ep.newborn_protection_on:
                    ep.ext_out_str += "    Newborns protected\n"
                else:
                    ep.ext_out_str += "    Newborns unprotected\n"
            else:
                ep.ext_out_str += "Newborn parameters disabled\n"
            
            # generate the alternate parameters description
            ep.ext_out_str += "Alternate Parameters:\n"
            
            if ep.alt_params_on:
                if ep.alt_select_on:
                    ep.ext_out_str += "    Tournament selection size decreases by {}\n".format(ep.alt_tourn_size)
                else:
                    ep.ext_out_str += "    Alternate selection parameters disabled\n"
                
                if ep.alt_xo_on:
                    ep.ext_out_str += "    Crossover probability increases by {}\n".format(ep.alt_xo_prob)
                else:
                    ep.ext_out_str += "    Alternate crossover parameters disabled\n"
                
                if ep.alt_mut_on:
                    ep.ext_out_str += "    Mutation probability increases by {}\n".format(ep.alt_mut_prob)
                    ep.ext_out_str += "    Mutation rate increases by {}\n".format(ep.alt_mut_rate)
                else:
                    ep.ext_out_str += "    Alternate mutation parameters disabled\n"
            else:
                ep.ext_out_str += "    Alternate parameters disabled\n"
        
        # if the extinction operator is off
        else:
            ep.ext_out_str += "Extinction operator disabled\n"
        
        # end the description of the parameter set
        ep.ext_out_str += "'''\n"
        ep.ext_out_str += "----------------------------------------------\n"
        
        # print the extinction parameters
        ep.ext_out_str += "\n# basic extinction parameters\n"
        
        ep.ext_out_str += "ep.ext_operator_on = {}\n".format(ep.ext_operator_on)
        
        # if the extinction operator is on, generate all extinction parameters as Python code
        if ep.ext_operator_on:
            # generate the basic extinction parameters
            ep.ext_out_str += "ep.ext_percent = {}\n".format(ep.ext_percent)
            ep.ext_out_str += "ep.ext_duration = {}\n".format(ep.ext_duration)
            ep.ext_out_str += "ep.ext_sort_order = {}\n".format(ep.ext_sort_order)
            ep.ext_out_str += "ep.ext_kills_least_fit = {}\n".format(ep.ext_kills_least_fit)
            
            if (ep.ext_duration != 1):
                if (ep.ext_duration < 8):
                    ep.ext_out_str += "ep.ext_kills_constant = True\n"
                else:
                    ep.ext_out_str += "ep.ext_kills_constant = {}\n".format(ep.ext_kills_constant)
                    
                    if (ep.ext_duration > 7) and not ep.ext_kills_constant:
                        ep.ext_out_str += "ep.ext_virulence = {}\n".format(ep.ext_virulence)
            
            ep.ext_out_str += "ep.ext_pop_dynamics_on = {}\n".format(ep.ext_pop_dynamics_on)
            
            if ep.ext_pop_dynamics_on:
                ep.ext_out_str += "ep.ext_pop_dyn_strength = {}\n".format(ep.ext_pop_dyn_strength)
            
            ep.ext_out_str += "ep.ext_end_extinction = {}\n".format(ep.ext_end_extinction)
            
            if ep.ext_end_extinction:
                ep.ext_out_str += "ep.ext_end_percent = {}\n".format(ep.ext_end_percent)
            
            ep.ext_out_str += "ep.ext_safeguard = {}\n".format(ep.ext_safeguard)
            
            # generate the elitism parameters
            ep.ext_out_str += "\n# elitism parameters\n"
            ep.ext_out_str += "ep.ext_elite_on = {}\n".format(ep.ext_elite_on)
            
            if ep.ext_elite_on:
                ep.ext_out_str += "ep.ext_elite_percent = {}\n".format(ep.ext_elite_percent)
            
            # generate the anti-elitism parameters
            ep.ext_out_str += "\n# anti-elitism parameters\n"
            ep.ext_out_str += "ep.ext_anti_elite_on = {}\n".format(ep.ext_anti_elite_on)
            
            if ep.ext_anti_elite_on:
                ep.ext_out_str += "ep.ext_anti_elite_percent = {}\n".format(ep.ext_anti_elite_percent)
            
            # generate the extinction type parameters
            ep.ext_out_str += "\n# extinction types\n"
            ep.ext_out_str += "ep.interval_extinction_on = {}\n".format(ep.interval_extinction_on)
            ep.ext_out_str += "ep.prob_extinction_on = {}\n".format(ep.prob_extinction_on)
            ep.ext_out_str += "ep.fit_extinction_on = {}\n".format(ep.fit_extinction_on)
            
            # generate the interval extinction parameters
            if ep.interval_extinction_on:
                ep.ext_out_str += "\n# interval extinction parameters\n"
                ep.ext_out_str += "ep.i_ext_interval = {}\n".format(ep.i_ext_interval)
            
            # generate the probabilistic extinction parameters
            if ep.prob_extinction_on:
                ep.ext_out_str += "\n# probabilistic extinction parameters\n"
                ep.ext_out_str += "ep.p_ext_interval = {}\n".format(ep.p_ext_interval)
                ep.ext_out_str += "ep.p_ext_base_prob = {}\n".format(ep.p_ext_base_prob)
                ep.ext_out_str += "ep.p_ext_prob_inc = {}\n".format(ep.p_ext_prob_inc)
            
            # generate the fitness extinction parameters
            if ep.fit_extinction_on:
                ep.ext_out_str += "\n# fitness extinction parameters\n"
                ep.ext_out_str += "ep.f_ext_interval = {}\n".format(ep.f_ext_interval)
                ep.ext_out_str += "ep.f_ext_pop_percent = {}\n".format(ep.f_ext_pop_percent)
                ep.ext_out_str += "ep.f_ext_improve_percent = {}\n".format(ep.f_ext_improve_percent)
            
            # generate the repopulation parameters
            ep.ext_out_str += "\n# repopulation parameters\n"
            ep.ext_out_str += "ep.repop_duration = {}\n".format(ep.repop_duration)
            
            if (ep.repop_duration != 1):
                if (ep.repop_duration < 8):
                    ep.ext_out_str += "ep.repop_constant = True\n"
                else:
                    ep.ext_out_str += "ep.repop_constant = {}\n".format(ep.repop_constant)
                    
                    if (ep.repop_duration > 7) and not ep.repop_constant:
                        ep.ext_out_str += "ep.repop_growth = {}\n".format(ep.repop_growth)
            
            ep.ext_out_str += "ep.repop_use_elites = {}\n".format(ep.repop_use_elites)
            
            if ep.repop_use_elites:
                ep.ext_out_str += "ep.repop_elite_percent = {}\n".format(ep.repop_elite_percent)
            
            ep.ext_out_str += "ep.repop_use_survivors = {}\n".format(ep.repop_use_survivors)
            
            if ep.repop_use_survivors:
                ep.ext_out_str += "ep.repop_survivor_percent = {}\n".format(ep.repop_survivor_percent)
            
            # generate the newborn parameters
            ep.ext_out_str += "\n# newborn parameters\n"
            ep.ext_out_str += "ep.newborn_params_on = {}\n".format(ep.newborn_params_on)
            
            if ep.newborn_params_on:
                ep.ext_out_str += "ep.newborn_expires = {}\n".format(ep.newborn_expires)
                ep.ext_out_str += "ep.newborn_protection_on = {}\n".format(ep.newborn_protection_on)
            
            # generate the alternate parameters
            ep.ext_out_str += "\n# alternate parameters\n"
            ep.ext_out_str += "ep.alt_params_on = {}\n".format(ep.alt_params_on)
            
            if ep.alt_params_on:
                # generate the alternate selection parameters
                ep.ext_out_str += "\n# alternate selection parameters\n"
                ep.ext_out_str += "ep.alt_select_on = {}\n".format(ep.alt_select_on)
                
                if ep.alt_select_on:
                    ep.ext_out_str += "ep.alt_tourn_size = {}\n".format(ep.alt_tourn_size)
                
                # generate the alternate crossover parameters
                ep.ext_out_str += "\n# alternate crossover parameters\n"
                ep.ext_out_str += "ep.alt_xo_on = {}\n".format(ep.alt_xo_on)
                
                if ep.alt_xo_on:
                    ep.ext_out_str += "ep.alt_xo_prob = {}\n".format(ep.alt_xo_prob)
                
                # generate the alternate mutation parameters
                ep.ext_out_str += "\n# alternate mutation parameters\n"
                ep.ext_out_str += "ep.alt_mut_on = {}\n".format(ep.alt_mut_on)
                
                if ep.alt_mut_on:
                    ep.ext_out_str += "ep.alt_mut_prob = {}\n".format(ep.alt_mut_prob)
                    ep.ext_out_str += "ep.alt_mut_rate = {}\n".format(ep.alt_mut_rate)
        
        # end the output string
        ep.ext_out_str += "\n----------------------------------------------\n"
    
    def _error_checking(self, population_size, maximum_generations):
        '''
        Description
        ----------
        Determines if the input extinction parameters are valid.
        
        Parameters
        ----------
        :param population_size : the current size of the population
            :type : int
        
        :param maximum_generations : the total number of generations the evolutionary algorithm will run for
            :type : int
        '''
        
        # define the list to hold any errors if they are found
        error_list = []
        
        # ensure the percentage of the population to kill is in the correct range
        if not 0.00 < ep.ext_percent < 1.00:
            error_list.append("ERROR: 'ext_percent' is out of range! Possible input range: (0.00, 1.00)")
        
        # ensure the duration of extinction is less than the maximum number of generations
        if not 0 < ep.ext_duration < maximum_generations:
            error_list.append("ERROR: 'ext_duration' is out of range! " + \
                              "Possible input range: [1, {})".format(maximum_generations))
        
        # ensure the sort order of the population list has been assigned
        if ep.ext_sort_order is None:
            error_list.append("ERROR: 'ext_sort_order' must be assigned a Boolean value!")
        
        # ensure the members to target for extinction has been assigned
        if ep.ext_kills_least_fit is None:
            error_list.append("ERROR: 'ext_kills_least_fit' must be assigned a Boolean value!")
        
        # if population dynamics are in use, check for errors
        if ep.ext_pop_dynamics_on:
            # ensure the population dynamics strength is in the correct range
            if not 0.00 <= ep.ext_pop_dyn_strength <= 1.00:
                error_list.append("ERROR: 'ext_pop_dyn_strength' is out of range! Possible input range: [0.00, 1.00]")
        
        # if 'ext_end_extinction' is in use, check for errors
        if ep.ext_end_extinction:
            # ensure the percentage of the maximum generations is in the correct range
            if not 0.00 < ep.ext_end_percent <= 1.00:
                error_list.append("ERROR: 'ext_end_percent' is out of range! Possible input range: (0.00, 1.00]")
        
        # if elitism is in use, check for errors
        if ep.ext_elite_on:
            # ensure the percentage of population to consider elite is in the correct range
            if not 0.00 <= ep.ext_elite_percent < 1.00:
                error_list.append("ERROR: 'ext_elite_percent' is out of range! Possible input range: [0.00, 1.00)")
        
        # if anti-elitism is in use, check for errors
        if ep.ext_anti_elite_on:
            # ensure the percentage of population to consider anti-elite is in the correct range
            if not 0.00 <= ep.ext_anti_elite_percent < 1.00:
                error_list.append("ERROR: 'ext_anti_elite_percent' is out of range! Possible input range: [0.00, 1.00)")
        
        # if both elitism and anti-elitism are in use, check for errors
        if ep.ext_elite_on and ep.ext_anti_elite_on:
            # ensure elitism and anti-elitism percentages are not overlapping each other
            if not ep.ext_elite_percent + ep.ext_anti_elite_percent <= 1.00:
                error_list.append("ERROR: elitism and anti-elitism percentages cannot overlap!\n" + \
                                  "       'ext_elite_percent' and 'ext_anti_elite_percent' sum cannot exceed 1.00")
        
        # if either probabilistic extinction or fitness extinction is in use, check for errors
        if ep.prob_extinction_on or ep.fit_extinction_on:
            # ensure the safeguard is less than the maximum number of generations
            if not 0 <= ep.ext_safeguard < maximum_generations:
                error_list.append("ERROR: 'ext_safeguard' is out of range! " + \
                                  "Possible input range: [0, {})".format(maximum_generations))
        
        # ensure at least one of the extinction types is enabled
        if not (ep.interval_extinction_on or ep.prob_extinction_on or ep.fit_extinction_on):
            error_list.append("ERROR: at least one of the extinction types must be enabled!\n       " + \
                              "'interval_extinction_on', 'prob_extinction_on', or 'fit_extinction_on' must be True")
        
        # if interval extinction is in use, check for errors
        if ep.interval_extinction_on:
            # ensure the interval is less than the maximum number of generations
            if not 0 < ep.i_ext_interval < maximum_generations:
                error_list.append("ERROR: 'i_ext_interval' is out of range! " + \
                                  "Possible input range: [1, {})".format(maximum_generations))
        
        # if probabilistic extinction is in use, check for errors
        if ep.prob_extinction_on:
            # ensure the interval is less than the maximum number of generations
            if not 0 < ep.p_ext_interval < maximum_generations:
                error_list.append("ERROR: 'p_ext_interval' is out of range! " + \
                                  "Possible input range: [1, {})".format(maximum_generations))
            
            # ensure the base extinction probability is in the correct range
            if not 0.00 <= ep.p_ext_base_prob <= 1.00:
                error_list.append("ERROR: 'p_ext_base_prob' is out of range! Possible input range: [0.00, 1.00]")
            
            # ensure the probability increase is in the correct range
            if not 0.00 <= ep.p_ext_prob_inc <= 1.00:
                error_list.append("ERROR: 'p_ext_prob_inc' is out of range! Possible input range: [0.00, 1.00]")
        
        # if fitness extinction is in use, check for errors
        if ep.fit_extinction_on:
            # ensure the interval is less than the maximum number of generations
            if not 0 < ep.f_ext_interval < maximum_generations:
                error_list.append("ERROR: 'f_ext_interval' is out of range! " + \
                                  "Possible input range: [1, {})".format(maximum_generations))
            
            # ensure the percentage of the population to pass the percent of fitness improvement is in the correct range
            if not 0.00 <= ep.f_ext_pop_percent <= 1.00:
                error_list.append("ERROR: 'f_ext_pop_percent' is out of range!" + \
                                  "Possible input range: [0.00, 1.00]")
            
            # ensure the required percentage of fitness improvement is in the correct range
            if not 0.00 <= ep.f_ext_improve_percent <= 1.00:
                error_list.append("ERROR: 'f_ext_improve_percent' is out of range!" + \
                                  "Possible input range: [0.00, 1.00]")
        
        # ensure the duration of repopulation is less than the maximum number of generations
        if not 0 < ep.repop_duration < maximum_generations:
            error_list.append("ERROR: 'repop_duration' is out of range! " + \
                              "Possible input range: [1, {})".format(maximum_generations))
        
        # if using elite members for repopulation, check for errors
        if ep.repop_use_elites:
            # ensure elitism is enabled if elite members are needed for repopulation
            if not ep.ext_elite_on:
                error_list.append("ERROR: elitism must be enabled! 'ext_elite_on' must be True")
            
            # ensure the percentage of the population to be repopulated using elite members is in the correct range
            if not 0.00 <= ep.repop_elite_percent <= 1.00:
                error_list.append("ERROR: 'repop_elite_percent' is out of range! Possible input range: [0.00, 1.00]")
        
        # if using surviving members for repopulation, check for errors
        if ep.repop_use_survivors:
            # ensure the percentage of the population to be repopulated using surviving members is in the correct range
            if not 0.00 <= ep.repop_survivor_percent <= 1.00:
                error_list.append("ERROR: 'repop_survivor_percent' is out of range! Possible input range: [0.00, 1.00]")
        
        # if using both elite members and surviving members for repopulation, check for errors
        if ep.repop_use_elites and ep.repop_use_survivors:
            # ensure elite member and surviving member percentages are not overlapping each other
            if not ep.repop_elite_percent + ep.repop_survivor_percent <= 1.00:
                error_list.append("ERROR: elite and survivor percentages for repopulation cannot overlap!\n" + \
                                  "       'repop_elite_percent' and 'repop_survivor_percent' sum cannot exceed 1.00")
        
        # if newborn parameters are in use, check for errors
        if ep.newborn_params_on:
            # ensure number of generations members are considered newborn is less than the maximum number of generations
            if not 0 <= ep.newborn_expires < maximum_generations:
                error_list.append("ERROR: 'newborn_expires' is out of range! " + \
                                  "Possible input range: [0, {})".format(maximum_generations))
        
        # if alternate parameters are in use, check for errors
        if ep.alt_params_on:
            # if alternate selection parameters are in use, check for errors
            if ep.alt_select_on:
                # ensure the alternate tournament size is less than the current population size and not negative
                if not 0 <= ep.alt_tourn_size < population_size:
                    error_list.append("ERROR: 'alt_tourn_size' is out of range! " + \
                                      "Possible input range: [0, {})".format(population_size))
            
            # if alternate crossover parameters are in use, check for errors
            if ep.alt_xo_on:
                # ensure the alternate crossover probability is in the correct range
                if not 0.00 <= ep.alt_xo_prob <= 1.00:
                    error_list.append("ERROR: 'alt_xo_prob' is out of range! Possible input range: [0.00, 1.00]")
            
            # if alternate mutation parameters are in use, check for errors
            if ep.alt_mut_on:
                # ensure the alternate mutation probability is in the correct range
                if not 0.00 <= ep.alt_mut_prob <= 1.00:
                    error_list.append("ERROR: 'alt_mut_prob' is out of range! Possible input range: [0.00, 1.00]")
                
                # ensure the alternate mutation rate is in the correct range
                if not 0.00 <= ep.alt_mut_rate <= 1.00:
                    error_list.append("ERROR: 'alt_mut_rate' is out of range! Possible input range: [0.00, 1.00]")
        
        # if any errors are found, print all errors and exit the program
        if error_list:
            # console spacing
            print("\n_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#\n")
            
            # print all errors found
            for error in error_list:
                print(error)
            
            # print error message
            print("\nOne or more extinction parameters are invalid, fix the above input errors!")
            
            # console spacing
            print("\n_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#\n")
            
            # terminate the program
            exit(1)
