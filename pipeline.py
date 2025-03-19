from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Load the dataset
data = pd.read_csv('spam_ham_dataset.csv')

# Feature and target variables
X = data['text']
y = data['label_num']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Naive Bayes Pipeline
nb_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Text vectorization
    ('clf', MultinomialNB())  # Naive Bayes classifier
])

# Train the model
nb_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = nb_pipeline.predict(X_test)
print("Naive Bayes Accuracy:", accuracy_score(y_test, y_pred))
print("Naive Bayes Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.linear_model import LogisticRegression

# Logistic Regression Pipeline
lr_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Text vectorization
    ('clf', LogisticRegression())  # Logistic Regression classifier
])

# Train the model
lr_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = lr_pipeline.predict(X_test)
print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred))
print("Logistic Regression Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier

# Random Forest Pipeline
rf_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Text vectorization
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))  # Random Forest classifier
])

# Train the model
rf_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_pipeline.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, y_pred))
print("Random Forest Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.svm import SVC

# SVM Pipeline
svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Text vectorization
    ('clf', SVC(kernel='linear'))  # SVM classifier with linear kernel
])

# Train the model
svm_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = svm_pipeline.predict(X_test)
print("SVM Accuracy:", accuracy_score(y_test, y_pred))
print("SVM Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.model_selection import GridSearchCV

# Example: Tuning Naive Bayes Pipeline
param_grid = {
    'tfidf__max_features': [1000, 5000, 10000],  # Number of features for TF-IDF
    'clf__alpha': [0.1, 0.5, 1.0]  # Smoothing parameter for Naive Bayes
}

# GridSearchCV with Naive Bayes Pipeline
grid_search = GridSearchCV(nb_pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best parameters and score
print("Best Parameters:", grid_search.best_params_)
print("Best Accuracy:", grid_search.best_score_)

# Evaluate on test data
y_pred = grid_search.predict(X_test)
print("Tuned Naive Bayes Accuracy:", accuracy_score(y_test, y_pred))
print("Tuned Naive Bayes Classification Report:\n", classification_report(y_test, y_pred))