from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import repository as repo
import pandas as pd
import re
from sklearn import neighbors, metrics, linear_model

pd.set_option('display.max_columns', 12)
df_combined = repo.read_dataframe('kaggle')

#  reorder because of randomizing
dfhotelCombishuffle = df_combined.sample(frac=1).reset_index(drop=True)
dfhotelCombishuffle.head(20)

X_precleaned = dfhotelCombishuffle['Review'].reset_index(drop=True)

y = dfhotelCombishuffle["Status"]

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
NO_SPACE = ""
SPACE = " "


def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]

    return reviews


# name X is used for splitting
X = preprocess_reviews(X_precleaned)

# make the sets smaller
X = X[1:10000]
y = y[1:10000]

# skip advanced cleaning

# splitting the data

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=1000, binary=False)

# Note the difference between fit_transform and transform
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

print(X_train_cv)
########################################################## SVM #########################################################
# from sklearn import svm
#
# svc = svm.SVC(kernel='linear')
#
# svc.fit(X_train_cv, y_train)
#
# from sklearn.metrics import accuracy_score
#
# print("Final Accuracy: %s" % accuracy_score(y_test, svc.predict(X_test_cv)))
# #  0.93 by using a smaller set only 10.000   finished in No time

########################################################### KNN ########################################################

# #create model
# knn = neighbors.KNeighborsClassifier(n_neighbors=10, weights='distance')
#
# #train model with train set
# knn.fit(X_train_cv, y_train)
#
# #test model
# predictions = knn.predict(X_test_cv)
#
# accuracy = metrics.accuracy_score(y_test,predictions)
#
# print("accuracy", accuracy)


############################################################### Linear Regression  #####################################
# l_reg = linear_model.LinearRegression()
# l_reg.fit(X_train_cv, y_train)
#
# # predictions = model.predict(X_test_cv)
# accuracy = l_reg.score(X_test_cv, y_test)
#
# print('predictions Linear Regression: ', accuracy)
#

############################################################### Random Forrest  ########################################
clf = RandomForestClassifier(max_depth=5, random_state=0)

clf.fit(X_train_cv, y_train)

#test model
predictions = clf.predict(X_test_cv)

accuracy = accuracy_score(y_test,predictions)

print("accuracy", accuracy)



# import pickle
# from joblib import dump, load
#
# dump(svc, 'svc.joblib')
#
# # load pre calculated model
# stored = load('svc.joblib')
# print("stored: %s" % accuracy_score(y_test, stored.predict(X_test_cv)))
#


#predict manual review
# X_manual = ['blabalababla']
# # of course cleaning
# X_manual_cv = cv.transform(X_manual)  # DO NOT USE fit_transform
# print()
# # stored.predict(X_manual_cv)
