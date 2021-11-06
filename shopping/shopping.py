import csv
import sys


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Opens the file.
    with open(filename) as file:
        reader = csv.reader(file)
        # Skips the headers.
        next(reader)
        # Initialises labels and evidence.
        labels = list()
        evidence = list()
        label_types = ['FALSE', 'TRUE']
        # Populates label and evidence for each row in the csv file.
        for row in reader:
            labels.append(label_types.index(row.pop(-1)))
            evidence.append(format_csv_data(row))

    return (evidence, labels)


def format_csv_data(row):
    # Sets the indexes for the the different types of evidence to format.
    month_index = 10
    visitor_type_index = 15
    weekend_index = 16
    int_indexes = [0, 2, 4, 11, 12, 13, 14]
    float_indexes = [1, 3, 5, 6, 7, 8, 9]
    # Months and weekend lists for fetching the index given the evidence.
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    weekend = ['FALSE', 'TRUE']
    # For each evidence, replaces it with the right numeric value.
    for i, evidence in enumerate(row):
        if i in int_indexes:
            row[i] = int(row[i])
        if i in float_indexes:
            row[i] = float(row[i])
        if i == month_index:
            row[i] = months.index(evidence)
        if i == visitor_type_index:
            row[i] = (1 if evidence == 'Returning_Visitor' else 0)
        if i == weekend_index:
            row[i] = weekend.index(evidence)

    return row


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Initialises the k-nearest neighbor model.
    model = KNeighborsClassifier(n_neighbors=1)
    # Trains the model.
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    total_positive = labels.count(1)
    total_negative = labels.count(0)
    # Iterates through actual and predicted values tuples and calculates
    # sensitivity and specificity based on how many values we were
    # able to correctly predict.
    for actual, predicted in zip(labels, predictions):
        if actual == predicted:
            if actual == 1:
                sensitivity += 1
            else:
                specificity += 1
    # Normalises the sensitivity and specificity values returning a float between 0 and 1.
    sensitivity /= total_positive
    specificity /= total_negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
