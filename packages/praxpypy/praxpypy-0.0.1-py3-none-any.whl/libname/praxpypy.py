import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def Graphs(data, variables=None, directory=os.getcwd()):
        ''' This package requires three arguments
         data : data frame for which the Graphs should be plotted
         Variable : default=None (all variable will be taken in consideration)
                    explicitly user defined must given in to the list format
                    e.g Variable = ['MPG', 'Weight','Acceleration']
        directory : default = current working directory
                    user can define their own directory for which they need to store the
                    EDA ouput graphs
        '''
        if variables == None:
            variables = data.columns
        data = data[variables]
        numerical = []
        categorical = []
        for i in data:
            cols = data[i]
            if cols.dtypes == "int64" or cols.dtypes == "float64":
                numerical.append(i)
            elif cols.dtypes == "object" and (data[i].nunique() < 20):
                categorical.append(i)
        numerical_df = data[numerical]
        categorical_df = data[categorical]
        for i in numerical_df:
            plt.hist(numerical_df[i], bins=100)
            plt.xlabel(i)
            plt.ylabel("{} histogram".format(i))
            plt.title(i)
            plt.savefig(directory + "\\" + "{} histogram.png".format(i))
            plt.show()
        for i in numerical_df:
            plt.boxplot(numerical_df[i], vert=False)
            plt.ylabel(i)
            plt.title("{} Boxplot".format(i))
            plt.savefig(directory + "\\" + "{} boxplot.png".format(i))
            plt.show()
        for i in categorical_df:
            data[i].value_counts().plot(kind="bar", figsize=(4, 4), color="coral", fontsize=13)
            plt.xlabel(i)
            plt.ylabel("Number")
            plt.title("{} Barplot".format(i))
            plt.savefig(directory + "\\" + "{} barplot.png".format(i))
            plt.show()
