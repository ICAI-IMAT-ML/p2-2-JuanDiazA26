# Laboratory practice 2.2: KNN classification
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme()
import numpy as np  
import seaborn as sns


def minkowski_distance(a: np.ndarray, b: np.ndarray, p: int = 2) -> float:
    """
    Compute the Minkowski distance between two arrays.

    Args:
        a (np.ndarray): First array.
        b (np.ndarray): Second array.
        p (int, optional): The degree of the Minkowski distance. Defaults to 2 (Euclidean distance).

    Returns:
        float: Minkowski distance between arrays a and b.
    """
    return float(np.sum([abs(a - b)**p])**(1/p))


# k-Nearest Neighbors Model

# - [K-Nearest Neighbours](https://scikit-learn.org/stable/modules/neighbors.html#classification)
# - [KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)


class knn:
    def __init__(self):
        self.k = None
        self.p = None
        self.x_train = None
        self.y_train = None

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, k: int = 5, p: int = 2):
        """
        Fit the model using X as training data and y as target values.

        You should check that all the arguments shall have valid values:
            X and y have the same number of rows.
            k is a positive integer.
            p is a positive integer.

        Args:
            X_train (np.ndarray): Training data.
            y_train (np.ndarray): Target values.
            k (int, optional): Number of neighbors to use. Defaults to 5.
            p (int, optional): The degree of the Minkowski distance. Defaults to 2.
        """
        if X_train.shape[0] == y_train.shape[0]:
            self.x_train = X_train
            self.y_train = y_train
        else:
            raise ValueError("Length of X_train and y_train must be equal.")
        
        if isinstance(k, int) and k > 0 and isinstance(p, int) and p > 0:
            self.k = k
            self.p = p
        else:
            raise ValueError("k and p must be positive integers.")

    def predict(self, X: np.ndarray) -> np.ndarray: # 4
        """
        Predict the class labels for the provided data.

        Args:
            X (np.ndarray): data samples to predict their labels.

        Returns:
            np.ndarray: Predicted class labels.
        """
        distancias = [knn.compute_distances(self, punto) for punto in X]
        vecinos = [knn.get_k_nearest_neighbors(self, dist) for dist in distancias]
        labels = self.y_train[vecinos]

        return np.array([knn.most_common_label(self, label) for label in labels])
        
    def predict_proba(self, X):
        """
        Predict the class probabilities for the provided data.

        Each class probability is the amount of each label from the k nearest neighbors
        divided by k.

        Args:
            X (np.ndarray): data samples to predict their labels.

        Returns:
            np.ndarray: Predicted class probabilities.
        """
        distancias = [knn.compute_distances(self, punto) for punto in X]
        vecinos = [knn.get_k_nearest_neighbors(self, dist) for dist in distancias]
        labels = self.y_train[vecinos]
        max_len = len(np.unique(self.y_train))

        return np.array([np.bincount(label, minlength=max_len) / len(label) for label in labels])

    def compute_distances(self, point: np.ndarray) -> np.ndarray: # 1
        """Compute distance from a point to every point in the training dataset

        Args:
            point (np.ndarray): data sample.

        Returns:
            np.ndarray: distance from point to each point in the training dataset.
        """
        return np.array([minkowski_distance(point, punto_train, self.p) for punto_train in self.x_train])

    def get_k_nearest_neighbors(self, distances: np.ndarray) -> np.ndarray: # 2
        """Get the k nearest neighbors indices given the distances matrix from a point.

        Args:
            distances (np.ndarray): distances matrix from a point whose neighbors want to be identified.

        Returns:
            np.ndarray: row indices from the k nearest neighbors.

        Hint:
            You might want to check the np.argsort function.
        """
        return np.argsort(distances)[:self.k]

    def most_common_label(self, knn_labels: np.ndarray) -> int: # 3
        """Obtain the most common label from the labels of the k nearest neighbors

        Args:
            knn_labels (np.ndarray): labels from the k nearest neighbors

        Returns:
            int: most common label
        """

        return np.where(np.bincount(knn_labels) == np.bincount(knn_labels).max())[0][0]

    def __str__(self):
        """
        String representation of the kNN model.
        """
        return f"kNN model (k={self.k}, p={self.p})"



def plot_2Dmodel_predictions(X, y, model, grid_points_n):
    """
    Plot the classification results and predicted probabilities of a model on a 2D grid.

    This function creates two plots:
    1. A classification results plot showing True Positives, False Positives, False Negatives, and True Negatives.
    2. A predicted probabilities plot showing the probability predictions with level curves for each 0.1 increment.

    Args:
        X (np.ndarray): The input data, a 2D array of shape (n_samples, 2), where each row represents a sample and each column represents a feature.
        y (np.ndarray): The true labels, a 1D array of length n_samples.
        model (classifier): A trained classification model with 'predict' and 'predict_proba' methods. The model should be compatible with the input data 'X'.
        grid_points_n (int): The number of points in the grid along each axis. This determines the resolution of the plots.

    Returns:
        None: This function does not return any value. It displays two plots.

    Note:
        - This function assumes binary classification and that the model's 'predict_proba' method returns probabilities for the positive class in the second column.
    """
    # Map string labels to numeric
    unique_labels = np.unique(y)
    num_to_label = {i: label for i, label in enumerate(unique_labels)}

    # Predict on input data
    preds = model.predict(X)

    # Determine TP, FP, FN, TN
    tp = (y == unique_labels[1]) & (preds == unique_labels[1])
    fp = (y == unique_labels[0]) & (preds == unique_labels[1])
    fn = (y == unique_labels[1]) & (preds == unique_labels[0])
    tn = (y == unique_labels[0]) & (preds == unique_labels[0])

    # Plotting
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Classification Results Plot
    ax[0].scatter(X[tp, 0], X[tp, 1], color="green", label=f"True {num_to_label[1]}")
    ax[0].scatter(X[fp, 0], X[fp, 1], color="red", label=f"False {num_to_label[1]}")
    ax[0].scatter(X[fn, 0], X[fn, 1], color="blue", label=f"False {num_to_label[0]}")
    ax[0].scatter(X[tn, 0], X[tn, 1], color="orange", label=f"True {num_to_label[0]}")
    ax[0].set_title("Classification Results")
    ax[0].legend()

    # Create a mesh grid
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, grid_points_n),
        np.linspace(y_min, y_max, grid_points_n),
    )

    # # Predict on mesh grid
    grid = np.c_[xx.ravel(), yy.ravel()]
    probs = model.predict_proba(grid)[:, 1].reshape(xx.shape)

    # Use Seaborn for the scatter plot
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=y, palette="Set1", ax=ax[1])
    ax[1].set_title("Classes and Estimated Probability Contour Lines")

    # Plot contour lines for probabilities
    cnt = ax[1].contour(xx, yy, probs, levels=np.arange(0, 1.1, 0.1), colors="black")
    ax[1].clabel(cnt, inline=True, fontsize=8)

    # Show the plot
    plt.tight_layout()
    plt.show()



def evaluate_classification_metrics(y_true, y_pred, positive_label): # Revisar enumerate roc
    """
    Calculate various evaluation metrics for a classification model.

    Args:
        y_true (array-like): True labels of the data.
        positive_label: The label considered as the positive class.
        y_pred (array-like): Predicted labels by the model.

    Returns:
        dict: A dictionary containing various evaluation metrics.

    Metrics Calculated:
        - Confusion Matrix: [TN, FP, FN, TP]
        - Accuracy: (TP + TN) / (TP + TN + FP + FN)
        - Precision: TP / (TP + FP)
        - Recall (Sensitivity): TP / (TP + FN)
        - Specificity: TN / (TN + FP)
        - F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
    """
    # Map string labels to 0 or 1
    y_true_mapped = np.array([1 if label == positive_label else 0 for label in y_true])
    y_pred_mapped = np.array([1 if label == positive_label else 0 for label in y_pred])

    # Confusion Matrix
    tn = []
    fp = []
    fn = []
    tp = []

    for i in range(len(y_true_mapped)):
        if y_pred_mapped[i] == y_true_mapped[i] and y_pred_mapped[i] == 1:
            tp.append(i)
        elif y_pred_mapped[i] == y_true_mapped[i]:
            tn.append(i)
        elif y_pred_mapped[i] == 1:
            fp.append(i)
        else:
            fn.append(i)
    
    tn = len(tn)
    fp = len(fp)
    fn = len(fn)
    tp = len(tp)

    # Accuracy
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    # Precision
    try:
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        precision = 0

    # Recall (Sensitivity)
    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        recall = 0

    # Specificity
    try:
        specificity = tn / (tn + fp)
    except ZeroDivisionError:
        specificity = 0

    # F1 Score
    try:
        f1 = 2 * (precision * recall) / (precision + recall)
    except ZeroDivisionError:
        f1 = 0

    return {
        "Confusion Matrix": [tn, fp, fn, tp],
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "Specificity": specificity,
        "F1 Score": f1,
    }



def plot_calibration_curve(y_true, y_probs, positive_label, n_bins=10):
    """
    Plot a calibration curve to evaluate the accuracy of predicted probabilities.

    This function creates a plot that compares the mean predicted probabilities
    in each bin with the fraction of positives (true outcomes) in that bin.
    This helps assess how well the probabilities are calibrated.

    Args:
        y_true (array-like): True labels of the data. Can be binary or categorical.
        y_probs (array-like): Predicted probabilities for the positive class (positive_label).
                            Expected values are in the range [0, 1].
        positive_label (int or str): The label that is considered the positive class.
                                    This is used to map categorical labels to binary outcomes.
        n_bins (int, optional): Number of bins to use for grouping predicted probabilities.
                                Defaults to 10. Bins are equally spaced in the range [0, 1].

    Returns:
        dict: A dictionary with the following keys:
            - "bin_centers": Array of the center values of each bin.
            - "true_proportions": Array of the fraction of positives in each bin

    """

    y_true_mapped = np.array([1 if label == positive_label else 0 for label in y_true])
    limites = np.linspace(0, 1, n_bins + 1)
    bins = [[] for _ in range(n_bins)]

    j = 0
    while j < len(y_probs):
        i = 0
        while i < n_bins:
            if y_probs[j] < limites[i+1]:
                bins[i].append(y_true_mapped[j])
                i = n_bins
            i += 1
        j += 1

    bin_centers = np.array([(limites[i] + limites[i+1]) / 2 for i in range(n_bins)])
    true_proportions = np.array([np.mean(bucket) for bucket in bins])

    plt.plot(bin_centers, true_proportions, label="Calibration curve")
    plt.plot([0, 1], [0, 1], linestyle='--', label='Perfectly calibrated', color='r')
    plt.legend()
    plt.show()
    
    return {"bin_centers": bin_centers, "true_proportions": true_proportions}



def plot_probability_histograms(y_true, y_probs, positive_label, n_bins=10):
    """
    Plot probability histograms for the positive and negative classes separately.

    This function creates two histograms showing the distribution of predicted
    probabilities for each class. This helps in understanding how the model
    differentiates between the classes.

    Args:
        y_true (array-like): True labels of the data. Can be binary or categorical.
        y_probs (array-like): Predicted probabilities for the positive class. 
                            Expected values are in the range [0, 1].
        positive_label (int or str): The label considered as the positive class.
                                    Used to map categorical labels to binary outcomes.
        n_bins (int, optional): Number of bins for the histograms. Defaults to 10. 
                                Bins are equally spaced in the range [0, 1].

    Returns:
        dict: A dictionary with the following keys:
            - "array_passed_to_histogram_of_positive_class": 
                Array of predicted probabilities for the positive class.
            - "array_passed_to_histogram_of_negative_class": 
                Array of predicted probabilities for the negative class.

    """
    y_true_mapped = np.array([1 if label == positive_label else 0 for label in y_true])

    plt.figure(figsize=(8, 6))
    plt.hist(y_probs[y_true_mapped == 1], color="blue", label="Clase positiva", bins=n_bins)
    plt.hist(y_probs[y_true_mapped == 0], color="orange", label="Clase negativa", bins=n_bins)
    plt.title("Clases positiva y negativa")
    plt.show()

    return {
        "array_passed_to_histogram_of_positive_class": y_probs[y_true_mapped == 1],
        "array_passed_to_histogram_of_negative_class": y_probs[y_true_mapped == 0],
    }



def plot_roc_curve(y_true, y_probs, positive_label):
    """
    Plot the Receiver Operating Characteristic (ROC) curve.

    The ROC curve is a graphical representation of the diagnostic ability of a binary
    classifier system as its discrimination threshold is varied. It plots the True Positive
    Rate (TPR) against the False Positive Rate (FPR) at various threshold settings.

    Args:
        y_true (array-like): True labels of the data. Can be binary or categorical.
        y_probs (array-like): Predicted probabilities for the positive class. 
                            Expected values are in the range [0, 1].
        positive_label (int or str): The label considered as the positive class.
                                    Used to map categorical labels to binary outcomes.

    Returns:
        dict: A dictionary containing the following:
            - "fpr": Array of False Positive Rates for each threshold.
            - "tpr": Array of True Positive Rates for each threshold.

    """
    y_true_mapped = np.array([1 if label == positive_label else 0 for label in y_true])

    thr = np.linspace(0, 1, 11) # Revisar

    tpr = []
    fpr = []

    for prob in thr:
        vp = 0
        vn = 0
        fp = 0
        fn = 0
        for i in range(len(y_probs)):
            if y_probs[i] >= prob and y_true_mapped[i] == 1:
                vp += 1
            elif y_probs[i] >= prob:
                fp += 1
            elif y_true_mapped[i] == 1:
                fn += 1
            else:
                vn += 1
        tpr.append(vp / (vp + fn) if (vp + fn) != 0 else 0)
        fpr.append(fp / (fp + vn) if (fp + vn) != 0 else 0)

    plt.plot(fpr, tpr)
    plt.title("ROC curve")
    plt.plot([0, 1], [0, 1], linestyle='--', label='Perfectly calibrated', color='r')
    plt.show()

    return {"fpr": np.array(fpr), "tpr": np.array(tpr)}
