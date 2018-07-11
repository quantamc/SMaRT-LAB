import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


csv_path = "./emo_raw_recordings.csv"


# Step 1: Load the data
def load_neural_data(path=csv_path):
    '''Returns the pandas dataframe'''

    if os.path.exists(csv_path) == True:
        return pd.read_csv(csv_path)

    else:
        print("No file to read from")


emo_dataframe = load_neural_data()
num_rows = emo_dataframe.shape[0]

# Step 2: Clean the data
# count the number of missing elements (NaN) in each column
counter_nan = emo_dataframe.isnull().sum()
counter_without_nam = counter_nan[counter_nan==0]
# remove the columns with missing elements
emo_dataframe = emo_dataframe[counter_without_nam.keys()]
# list of columns (last column is the class label)
columns = emo_dataframe.columns
print(columns)

# Step 3: Create feature vectors
x = emo_dataframe.ix[:,:-1].values
# shifting the distribution of each feature to have a mean of 0 and std of 1 (same scale)
standard_scalar = StandardScaler()
x_std = standard_scalar.fit_transform(x)

# step 4: get class labels y and then encode it into number
# get class label data
y = emo_dataframe.ix[:,-1].values
# encode the class label
class_labels = np.unique(y)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# step 5: split the data into training set and test set
test_percentage = 0.4
X_train, X_test, y_train, y_test = train_test_split(x_std, y, test_size = test_percentage, random_state = 0)

######################################################################################################################

# SVM
from sklearn.svm import LinearSVC

polynomial_svm_clf = Pipeline((
        ("poly_features", PolynomialFeatures(degree=3)),
        ("scaler", StandardScaler()),
        ("svm_clf", LinearSVC(C=10, loss='hinge'))
))

polynomial_svm_clf.fit(X_train, y_train)
svm_score = polynomial_svm_clf.score(X_test, y_test)

# Decision trees
from sklearn import tree

tree_clf = tree.DecisionTreeClassifier(criterion='entropy')
tree_clf.fit(X_train, y_train)

# visualize
from sklearn.tree import export_graphviz
#import graphviz

dot_data = export_graphviz(tree_clf, out_file=None,
                           feature_names=columns[:-1],
                           class_names=["stationary", "walk"], filled=True,
                           rounded=True, special_characters=True)
#graph = graphviz.Source(dot_data)
#graph.render("brain")

tree_score = tree_clf.score(X_test, y_test)

# Neural Network implementation
from sklearn.neural_network import MLPClassifier


neural_clf = MLPClassifier()

neural_clf.fit(X_train, y_train)
neural_score = neural_clf.score(X_test, y_test)

print("svm score:" + str(svm_score))
print ("Tree score:" + str(tree_score))
print("Neural Net score" + str(neural_score))



import pickle


# Save to file in the current working directory
plk_filename = "pickle_model.pk1"
with open(plk_filename, 'wb') as file:
    pickle.dump(tree_clf, file)