'''
Biologically-Inspired Mass Extinction in Evolutionary Algorithms
Author: Kaelan Engholdt
Version: 05/26/2021

Setup file for the 'mass_extinction' package.

'''

from setuptools import setup


# a shorter version of the 'README.md' that serves as a basic description of the package
long_description = "# **Biologically-Inspired Mass Extinction in Evolutionary Algorithms**\n" \
                   "## _The Biologically-Inspired Extinction Operator_\n" \
                   "###### Author: Kaelan Engholdt\n" \
                   "###### Version: 05/26/2021\n\n###\n\n" \
                   "## **Section 1 - Introduction**\n" \
                   "Mass extinction events have previously been shown to be a catalyst for accelerating the rate of " \
                   "evolution in evolutionary algorithms.  This increased rate of evolution combined with a " \
                   "destabilization of the dynamic equilibrium of the evolutionary algorithm can allow the " \
                   "algorithm to overcome local optima in the solution space; however, most implementations " \
                   "of mass extinction squander the full benefit of the increased evolutionary rate by relying " \
                   "upon random chance to generate better solutions in the post-extinction generations.\n\n" \
                   "This operator is a biologically-inspired mass extinction operator specifically designed for " \
                   "use in evolutionary algorithms, while retaining the benefits of extinction events from the " \
                   "natural world.  By increasing variability and decreasing selection pressure immediately after " \
                   "an extinction event, the evolutionary algorithm has a higher chance of yielding more fit " \
                   "individuals and overcoming local optima in the post-extinction generations.  The operator " \
                   "works especially well on problem domains with many local optima, with many evolutionary "\
                   "algorithms exhibiting a higher success rate than with standard implementations of mass "\
                   "extinction.\n\n" \
                   "This operator contains adjustable parameters for extinction events and methods of " \
                   "repopulation, and is designed to be integrated into an evolutionary algorithm.  Due to the " \
                   "problem-specific nature of evolutionary algorithms, minor parts of this package must be " \
                   "finished by the user.\n\n" \
                   "If used and tuned correctly, extinction can be a powerful tool in evolutionary algorithms.  " \
                   "This simple package attempts to provide a basis upon which users can integrate extinction " \
                   "events into their evolutionary algorithms, maintain population diversity, improve the overall " \
                   "fitness of their population, and attempt to overcome sub-optimal peaks within the search " \
                   "space of their particular problem.\n\n" \
                   "Includes support for integration with evolutionary algorithms that make use of the " \
                   "_Distributed Evolutionary Algorithms in Python (DEAP)_ library, which is a framework for " \
                   "writing evolutionary algorithms.  This package is not affiliated with DEAP, but offers " \
                   "support for evolutionary algorithms using that library.\n\n" \
                   "> This concludes the Introduction section.\n\n###\n###\n\n" \
                   "## **Section 2 - Compatibility**\n" \
                   "The files in this package are OS independent, and can be run on either Python 2 or Python 3.\n\n" \
                   "> This concludes the Compatibility section.\n\n###\n###\n\n" \
                   "## **Section 3 - Requirements**\n" \
                   "Requirements:  \n" \
                   " - A population-based evolutionary algorithm written in Python 2 or Python 3.  \n" \
                   " - The parent population must be sorted by fitness and stored in a list.  \n" \
                   " - Following and completing all `TODO` comments.  \n\n" \
                   "> This concludes the Requirements section.\n\n###\n###\n\n" \
                   "## **Section 4 - Contents**\n" \
                   "The package consists of the following files:  \n" \
                   " - `mass_extinction.py` : Contains the Extinction class.  \n" \
                   " - `ext_params.py` : Contains all of the adjustable extinction parameters for the " \
                   "Extinction class.  \n" \
                   " - `ext_types.py` : Contains numerous extinction parameter sets for testing purposes.  \n" \
                   " - `README.md` : Contains all documentation related to the Extinction class.  \n\n" \
                   "> This concludes the Contents section.\n\n###\n###\n\n" \
                   "## **Section 5 - Design**\n" \
                   "The files in this package have been specifically designed to be integrated and interlaced " \
                   "with an evolutionary algorithm.  Due to the problem-specific nature of evolutionary algorithms, " \
                   "some of this package must be finished by the user.\n\n" \
                   "This package features the following:  \n" \
                   " - A multitude of completely adjustable parameters that affect how both extinction and " \
                   "repopulation operate.  \n" \
                   " - Two methods of extinction:  \n" \
                   "    - Instant Extinction  \n" \
                   "    - Gradual Extinction  \n" \
                   " - Three types of extinction that can be used separately or in conjunction with one another:  \n" \
                   "    - Interval Extinction  \n" \
                   "    - Probabilistic Extinction  \n" \
                   "    - Fitness Extinction  \n" \
                   " - Two methods of repopulation:  \n" \
                   "    - Instant Repopulation  \n" \
                   "    - Gradual Repopulation  \n" \
                   " - Three types of repopulation that can be used separately or in conjunction with " \
                   "one another:  \n" \
                   "    - Repopulation using children of elite members.  \n" \
                   "    - Repopulation using children of surviving members of an extinction event.  \n" \
                   "    - Repopulation using random members.  \n" \
                   " - Testing of up to 324 parameter sets generated from permutations of user-defined " \
                   "parameters.  \n" \
                   " - All parameters can be saved as parameter sets and later called upon to revert back to a " \
                   "previous version of extinction/repopulation.  \n\n" \
                   "> This concludes the Design section.\n\n###\n###\n\n" \
                   "Additional information can be found in the `README.md`, which is included in the package download."

# define setup
setup(
    name = "mass_extinction",
    version = "1.0.0",
    author = "Kaelan Engholdt",
    author_email = "extinctionpackage@gmail.com",
    description = ("Mass extinction class for evolutionary algorithms."),
    keywords = "extinction evolutionary genetic algorithm",
    url = "https://bitbucket.org/Trench58/mass_extinction/src/master/",
    packages = ["mass_extinction"],
    package_data = {"" : ["README.md"]},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = ["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering :: Artificial Intelligence",
                   "Topic :: Scientific/Engineering :: Artificial Life"]
)
