import pandas as pd
import pickle
from func import miss_values, ordinal_encoding, stratified_splits, rob_scaling
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC


loan_data = pd.read_csv('./dataset/loan_data_set.csv')

miss_values(loan_data)

ordinal_encoding(loan_data)
X = loan_data.drop(["Loan_Status", "Loan_ID"], axis=1)
y = loan_data.Loan_Status

rob_scaling(X, y)
X_train, X_test, y_train, y_test = stratified_splits(n_split=3, x=X, y=y)

lr = LogisticRegression(random_state=1234, n_jobs=1)
svc = SVC(random_state=1234, C =1, kernel='poly', degree=0, max_iter=1)
rf = RandomForestClassifier(n_estimators=100, n_jobs=1, max_leaf_nodes=6)

voting_clf = VotingClassifier(estimators=[("lr", lr), ('rf', rf), ('svc', svc)], voting="hard")

voting_clf.fit(X_train, y_train)

