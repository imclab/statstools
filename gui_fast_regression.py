import easygui as eg
import sys
import os
import fast_regression as fr

"""
Loops over two .csv files and regresses each column in the first with each column in the second. 
Saves .jpgs of regression plots and stats.
Saves a master residual file. 
"""

"""
User Interface Stuff: choosing file save locations, etc.
"""
while 1:
    #print out any exceptions
    try:
        predictors_path = None 
        regressors_path = None
        is_files = False
        image   = "logo.gif"
        title   = "Fast Regression"
        msg     = """Choose two .csv data files to regress against one another.
                     \n Files must be properly formatted according to the \'Help\' file"""
        while predictors_path==None or regressors_path==None or is_files==False:
            predictors_file = ""
            regressors_file = ""
            if predictors_path!=None:
                predictors_file = os.path.basename(predictors_path)
            if regressors_path!=None:
                regressors_file = os.path.basename(regressors_path)
            choices = ["Regressor Data " + regressors_file, "Predictor Data" + predictors_file]
            if predictors_path !=None and regressors_path!=None:
                choices.append("Run Regressions")
            reply = eg.buttonbox(msg, title, image=image,choices=choices)
            if reply == choices[0]:
                msg = ""
                title = "Choose regressors data file"
                regressors_path = eg.fileopenbox(msg, title, filetypes=['*.csv'])
            elif reply == choices[1]:
                msg = ""
                title = "Choose predictors data file"
                predictors_path = eg.fileopenbox(msg, title, filetypes=['*.csv'])
            elif reply == "Run Regressions":
                is_files = True
        #results of this loop
        print regressors_path
        print predictors_path 

        msg = "Choose Plot Output Folder"
        title = "Plot Output"
        eg.msgbox(msg, title)    
        msg = ""
        default_directory = "Plots Folder\\"
        plots_directory = eg.diropenbox(msg, title, default=default_directory) + "/"
        #TODO: Handle cancel
         
        msg = "Choose Resdiual Output Filename"
        title = "Resdiual Output"
        eg.msgbox(msg, title)
        msg = ""
        default_filename = "residuals"
        resid_directory = eg.filesavebox(msg, title, default=default_filename, filetypes=['*.csv'])
        #TODO: Handle cancel

        """
        Regression Loop
        """

        fr.fast_regression(regressors_path,predictors_path,resid_directory, plots_directory)

        eg.msgbox("Regressions Complete \n Residuals written to " + 
                    resid_directory + ".csv\n Plots written to " + plots_directory)
    except:
        #catch-all for exceptions
        message =   """An error has occured. Please double check the following: \n
                        There should be no trailing empty cells in the regresor or predictor .csv files \n
                        There can be no repeated column names in theses files\n
                        There can be no spaces or special charagers in the column names of these files \n
                        Row labels must be the same for bothe the regressor and predictor .csv files\n\n
                        Please see the Help file for more formatting information"""
        eg.exceptionbox(message, "Error")

    sys.exit(0)          