# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 11:51:14 2021

@author: he
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


df = pd.read_csv('jobs_final.csv')

df.columns
#choosing relevant columns.
df_model = df[['Rating','Size','Type of ownership','Industry', 'Sector', 'Revenue','hourly', 
               'employer_provided','avg_salary','job_state', 'same_state', 'age', 'python','aws', 'spark', 'excel', 'job_level',
       'job_desc_len','num_competitors','simple_job_title']]
#get dummy data
df_dummy = pd.get_dummies(df_model)
#train test plit
X = df_dummy.drop('avg_salary', axis=1)
y = df_dummy.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#multiple linear regression

#using statsmodel
#import statsmodels.api as sm
#X_sm = X = sm.add_constant(X)
#model = sm.OLS(y, X_sm)
#model.fit().summary()
#using sklearn
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=2))

#lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

alpha = []
error = []

for i in range(1, 100):
    alpha.append(i/100)
    lml = Lasso(alpha =(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))
plt.plot(alpha, error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

#random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))
#tune models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_

#test ensembles
pred_lm = lm.predict(X_test)
pred_lml = lm_l.predict(X_test)
pred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, pred_lm)
mean_absolute_error(y_test, pred_lml)
mean_absolute_error(y_test, pred_rf)

mean_absolute_error(y_test, (pred_lm + pred_lml)/2)