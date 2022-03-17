import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


if __name__ == "__main__":
    # Get data from csv file.
    dataset = pd.read_csv(filepath_or_buffer="Health_Network_Ads.csv")

    # We want to estimate Class values based on the independent values of Department, Age and EstimatedSalary.
    independent = dataset[['Department', 'Age', 'EstimatedSalary']]
    dependent = dataset['Class']

    # Split data in 80% training data and 20% test data and train support vector machine
    X_train, X_test, y_train, y_test = train_test_split(independent, dependent, test_size=0.2, random_state=10)
    clf = SVC()
    clf.fit(X_train, y_train)

    # Predict on independent test data and measure the classificiation.
    y_pred = clf.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    outcome = "True Negatives: {}\nFalse Positives: {}\nFalse Negatives: {}\nTrue Positives: {}".format(tn, fp, fn, tp)
    print(outcome)