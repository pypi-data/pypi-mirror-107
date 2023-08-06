"""
    Linear regression using Ordinary Least Squares (OLS) function from the statsmodels library.
    
    OLS is a common technique used in analyzing linear regression. In brief, it compares the difference between individual points in your data set and the predicted best fit line to measure the amount of error produced.
    
    Covariance is a measure of how two variables are linked in a positive or negative manner, and a robust covariance is one that is calculated in a way to minimize or eliminate variables.
    
    R-squared is the measurement of how much of the independent variable is explained by changes in our dependent variables.
    
    The adjusted R-squared penalizes the R-squared formula based on the number of variables, therefore a lower adjusted score may be telling you some variables are not contributing to your model’s R-squared properly.
    Adjusted. R-squared reflects the fit of the model. R-squared values range from 0 to 1, where a higher value generally indicates a better fit, assuming certain conditions are met.
    
    The F-statistic in linear regression is comparing your produced linear model for your variables against a model that replaces your variables’ effect to 0, to find out if your group of variables are statistically significant. To interpret this number correctly, using a chosen alpha value and an F-table is necessary.
    
    Prob (F-Statistic) uses this number to tell you the accuracy of the null hypothesis, or whether it is accurate that your variables’ effect is 0.
    
    Log-likelihood is a numerical signifier of the likelihood that your produced model produced the given data. It is used to compare coefficient values for each variable in the process of creating the model.
    
    AIC and BIC are both used to compare the efficacy of models in the process of linear regression, using a penalty system for measuring multiple variables. These numbers are used for feature selection of variables.
    
    std err reflects the level of accuracy of the coefficients. The lower it is, the higher is the level of accuracy.
    
    P>|t| is one of the most important statistics in the summary. It uses the t statistic to produce the p value, a measurement of how likely your coefficient is measured through our model by chance. The p value of 0.378 for Wealth is saying there is a 37.8% chance the Wealth variable has no affect on the dependent variable, Lottery, and our results are produced by chance. Proper model analysis will compare the p value to a previously established alpha value, or a threshold with which we can apply significance to our coefficient. A common alpha is 0.05, which few of our variables pass in this instance.
    P >|t| is your p-value. A p-value of less than 0.05 is considered to be statistically significant
    
    [0.025 and 0.975] are both measurements of values of our coefficients within 95% of our data, or within two standard deviations. Outside of these values can generally be considered outliers.
    Confidence Interval represents the range in which our coefficients are likely to fall (with a likelihood of 95%)
    
    Omnibus describes the normalcy of the distribution of our residuals using skew and kurtosis as measurements. A 0 would indicate perfect normalcy.
    
    Prob(Omnibus) is a statistical test measuring the probability the residuals are normally distributed. A 1 would indicate perfectly normal distribution.
    
    Skew is a measurement of symmetry in our data, with 0 being perfect symmetry.
    
    Kurtosis measures the peakiness of our data, or its concentration around 0 in a normal curve. Higher kurtosis implies fewer outliers.
    
    Durbin-Watson is a measurement of homoscedasticity, or an even distribution of errors throughout our data. Heteroscedasticity would imply an uneven distribution, for example as the data point grows higher the relative error grows higher. Ideal homoscedasticity will lie between 1 and 2.
    
    Jarque-Bera (JB) and Prob(JB) are alternate methods of measuring the same value as Omnibus and Prob(Omnibus) using skewness and kurtosis. We use these values to confirm each other. 
    
    Condition number is a measurement of the sensitivity of our model as compared to the size of changes in the data it is analyzing. Multicollinearity is strongly implied by a high condition number. Multicollinearity a term to describe two or more independent variables that are strongly related to each other and are falsely affecting our predicted variable by redundancy.
    
    Thanks to :
    https://medium.com/swlh/interpreting-linear-regression-through-statsmodels-summary-4796d359035a
    https://datatofish.com/statsmodels-linear-regression/
"""

import statsmodels.formula.api as __model

import anoapycore as __ap

class __result :
    summary = None

def run (a_data,a_feature,a_target) :
    loc_feature = __ap.data.array_to_str(a_feature,'+')
    loc_model = __model.ols(a_target + " ~ " + loc_feature,a_data).fit()
    loc_result = __result()
    loc_result.summary = loc_model.summary()
    return loc_result