# Hierarchical Goal System Visualizations and Personality Traits in a Digital Goal Setting Intervention: A Correlational Study

Data sets and analysis scripts for a study conducted among university students to investigate correlations between Hierarchical Goal System visualizations and personality traits in a digital goal setting intervention.

 The analysis scripts are divided into pilot ("pre") and main study ("main") scripts indicated by prefixes while data sets are indicated by the suffix "data". In the following, a brief description of the scripts' content is provided along with information about the used packages and instructions to run the analysis scripts.

## Pilot Study Files

`prestudy_cronbachs-alpha`: Calculation of Cronbach's alpha analyzing the reliability of the Likert scale measuring the visualizations complexities.

`prestudy_demographic`: Demographic data of participants including age, gender, study track, semester, computer experience, and study tool usage.

`prestudy_helpers`: Helper functions used throughout the analysis. Definition of data paths and specification of csv saving locations.



## Main Study Files

`main_bigfive`: Big Five questionnaire analysis script including plausibility testings.

`main_complexity_rating`: Investigation of correlation between visualization complexity and preference ratings using plots and correlation coefficients.

`main_complexity`: Complexity ratings of visualizations.

`main_demographic`: Demographic data of participants including age, gender, study track, semester, computer experience, study tool usage, and consulting requests.

`main_helpers`: Helper functions used throughout the analysis. Definition of data paths and specification of csv saving locations.

`main_sus-openness`: Correlation between Openness trait scores and perceived usability of the intervention measured by the System Usability Scale (SUS).

`main_median-split`: Dichotimization of Big Five traits using the median split technique to compare preference ratings between the different trait expressions.

`main_qualitative`: Gather qualitative data in csv file.

`main_rating`: Preference ratings of visualizations.

`main_sus`: System Usability Scale (SUS) assessment.

## Used Packages
numpy, pandas, functools, pingouin, matplotlib, seaborn, plotnine, ast, datetime, scipy

## Running the Scripts

1. Download the data and the scripts. Due to multiple cross references within the main and pilot study analysis, it is advised to store scripts of one study part in the same directory.

2. Define the used paths in the `prestudy_helpers` and `main_helpers` files. Also, make sure that you have installed all necessary packages.

2. Run the script you wish to use by using the command `python example-file.py` (The `helpers`-files solely provides helper functions and do not need to be compiled on their own.)
