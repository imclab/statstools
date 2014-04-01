import easygui as eg
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices
from statsmodels.graphics.regressionplots import plot_partregress
import csv as csv
import os

#helper function to write to a file
def writerow(thing, name, isfirst):
    output_name = name + ".csv"
    if isfirst: #if first time writing to file, overwrite rather than append
        mywriter = csv.writer(open(output_name, 'wb'), dialect='excel')
    else:
        mywriter = csv.writer(open(output_name, 'ab'), dialect='excel')
    mywriter.writerow(thing)


def fast_regression(regressors_path, predictors_path, resid_directory, plots_directory):

    regressors = pd.read_csv(regressors_path, index_col=0)
    row_names = regressors.index
    label_points = eg.multchoicebox("Choose which datapoints will be labeled in the output plots:",
                                     "Label Datapoints", choices=row_names)
    regressor_names = list(regressors.columns.values)
    isfirst = True
    
    """
    Regression Loop
    """
    for regressor_name in regressor_names:
        #read predictor file, first column is dataframe index
        predictors = pd.read_csv(predictors_path, index_col=0)
        predictor_names = list(predictors.columns.values)
        predictors[regressor_name] = regressors[regressor_name]
        print regressor_name
        regressor_name = regressor_name
        for predictor_name in predictor_names:
            print "   -" + predictor_name
            patsy_string =  regressor_name + ' ~ ' + predictor_name
            y, x = dmatrices(patsy_string, data=predictors, return_type='dataframe')
            company_names = x.index
            results = sm.OLS(y, x).fit()

            scale = results.scale
            p_value = results.pvalues[1] #p value of variable, not intercept
            rsquared = results.rsquared
            std_error = scale**(0.5)
            fittedvalues = results.fittedvalues

            """
            Plot results
            """
            x = x.drop('Intercept',1) #remove intercept column from dataframe (automatically added by patsy)
            figure = plt.figure(figsize=(8,10.5))
            figure.add_subplot(2,1,1).plot(x, fittedvalues, "--k")
            figure.add_subplot(2,1,1).plot(x, y, "ro")
            figure.add_subplot(2,1,1).plot(x, fittedvalues + std_error, 'g-')
            figure.add_subplot(2,1,1).plot(x, fittedvalues - std_error, 'g-')

            #annotate all points, each a particular company, with its respective name   
            labeled_points =  list(set(company_names).intersection(set(label_points)))
            for company_name in labeled_points:
                xp = x.ix[company_name,0]
                yp = y.ix[company_name,0]
                plt.annotate(company_name, (xp,yp), xycoords = 'data',  color = 'b')

            plt.xlabel(predictor_name)
            plt.ylabel(regressor_name)
            plt.figtext(.02, 0.05, results.summary(), size='small')

            """
            Save plots and residual file
            """
            plt.savefig(plots_directory + regressor_name + "-" +predictor_name + ".jpg")
            plt.clf()

            if isfirst: #write column headers if this is the first row in the file
                writerow(["utility","regressor", "predictor", "rsquared", "p_value", 
                            "std_error", "residual", "category_spend"], resid_directory, isfirst)
                isfirst = False
            #write residuals to file
            for i, utility_name in enumerate(company_names):
                cat_spend = regressors[regressor_name]
                utility_cat_spend = cat_spend.ix[utility_name]
                resid_data = [utility_name, regressor_name, predictor_name, rsquared, p_value, 
                                std_error, results.resid[i], utility_cat_spend]
                writerow(resid_data, resid_directory, isfirst)

