from models import *
from numpy import linspace
import matplotlib.pyplot as plt
from anemia_data import anemia_data


def get_linspace(start: int, end: int, step: int):
    linspace_vect = list(range(start, end, step))
    return linspace_vect


def metrics_graph_lr(data: anemia_data, test_size: float):

    iterations_vect = linspace(0, 2000, 100)
    precision_vect = []
    recall_vect = []
    f1_score_vect = []
    accuracy_vect = []

    fig, graph_lr = plt.subplots(4, 1)
    fig.tight_layout(pad=3.0)

    for i in range(len(iterations_vect)):
        model_i = anemia_logistic_regression(data, iterations_vect[i], test_size)

        model_i.predict()
        accuracy_vect.append(model_i.get_metric("Accuracy"))
        precision_vect.append(model_i.get_metric("Precision"))
        recall_vect.append(model_i.get_metric("Recall"))
        f1_score_vect.append(model_i.get_metric("F1_score"))

    graph_lr[0].plot(iterations_vect, accuracy_vect)
    graph_lr[0].set_title("Accuracy - Logistic Regression")

    graph_lr[1].plot(iterations_vect, precision_vect)
    graph_lr[1].set_title("Precision - Logistic Regression")

    graph_lr[2].plot(iterations_vect, recall_vect)
    graph_lr[2].set_title("Recall - Logistic Regression")

    graph_lr[3].plot(iterations_vect, f1_score_vect)
    graph_lr[3].set_title("F1 Score - Logistic Regression")

    plt.show()


def metrics_graph_dt(data: anemia_data, test_size: float):

    iterations_vect = linspace(0, 200, 5)
    precision_vect = []
    recall_vect = []
    f1_score_vect = []
    accuracy_vect = []

    fig, graph_dt = plt.subplots(2, 2)
    fig.tight_layout(pad=4.0)

    for i in range(len(iterations_vect)):
        model_i = anemia_decision_tree(data, iterations_vect[i], test_size)

        model_i.predict()
        accuracy_vect.append(model_i.get_metric("Accuracy"))
        precision_vect.append(model_i.get_metric("Precision"))
        recall_vect.append(model_i.get_metric("Recall"))
        f1_score_vect.append(model_i.get_metric("F1_score"))

    graph_dt[0, 0].plot(iterations_vect, accuracy_vect)
    graph_dt[0, 0].set_title("Accuracy - Decision Tree")

    graph_dt[0, 1].plot(iterations_vect, precision_vect)
    graph_dt[0, 1].set_title("Precision - Decision Tree")

    graph_dt[1, 0].plot(iterations_vect, recall_vect)
    graph_dt[1, 0].set_title("Recall - Decision Tree")

    graph_dt[1, 1].plot(iterations_vect, f1_score_vect)
    graph_dt[1, 1].set_title("F1 Score - Decision Tree")

    plt.show()


def metrics_graph_knn(data: anemia_data, test_size: float):

    iterations_vect = get_linspace(1, 50, 1)
    precision_vect = []
    recall_vect = []
    f1_score_vect = []
    accuracy_vect = []

    fig, graph_knn = plt.subplots(2, 2)
    fig.tight_layout(pad=4.0)

    for i in range(len(iterations_vect)):
        model_i = anemia_knn(data, test_size, iterations_vect[i])

        model_i.predict()
        accuracy_vect.append(model_i.get_metric("Accuracy"))
        precision_vect.append(model_i.get_metric("Precision"))
        recall_vect.append(model_i.get_metric("Recall"))
        f1_score_vect.append(model_i.get_metric("F1_score"))

    graph_knn[0, 0].plot(iterations_vect, accuracy_vect)
    graph_knn[0, 0].set_title("Accuracy - KNN")

    graph_knn[0, 1].plot(iterations_vect, precision_vect)
    graph_knn[0, 1].set_title("Precision - KNN")

    graph_knn[1, 0].plot(iterations_vect, recall_vect)
    graph_knn[1, 0].set_title("Recall - KNN")

    graph_knn[1, 1].plot(iterations_vect, f1_score_vect)
    graph_knn[1, 1].set_title("F1 Score - KNN")

    plt.show()


def comparison_metrics_models(data: anemia_data, test_size: float):

    model_1 = anemia_logistic_regression(data, 100, test_size)
    model_1.predict()

    model_2 = anemia_decision_tree(data, 50, test_size)
    model_2.predict()

    model_3 = anemia_knn(data, test_size, 21)
    model_3.predict()

    fig, graph_cm = plt.subplots(2, 2)
    fig.tight_layout(pad=4.0)

    precision_data_dict = {
        "Logistic_Regression": model_1.get_metric("Precision"),
        "Decision_Tree": model_2.get_metric("Precision"),
        "K-Nearest-Neighbor": model_3.get_metric("Precision")
    }

    recall_data_dict = {
        "Logistic_Regression": model_1.get_metric("Recall"),
        "Decision_Tree": model_2.get_metric("Recall"),
        "K-Nearest-Neighbor": model_3.get_metric("Recall")
    }

    f1_data_dict = {
        "Logistic_Regression": model_1.get_metric("F1_score"),
        "Decision_Tree": model_2.get_metric("F1_score"),
        "K-Nearest-Neighbor": model_3.get_metric("F1_score")
    }

    accuracy_data_dict = {
        "Logistic_Regression": model_1.get_metric("Accuracy"),
        "Decision_Tree": model_2.get_metric("Accuracy"),
        "K-Nearest-Neighbor": model_3.get_metric("Accuracy")
    }

    models_names = list(precision_data_dict.keys())

    models_precision_data = list(precision_data_dict.values())
    models_recall_data = list(recall_data_dict.values())
    models_f1_data = list(f1_data_dict.values())
    models_accuracy_data = list(accuracy_data_dict.values())

    graph_cm[0, 0].bar(models_names, models_precision_data, color="red")
    graph_cm[0, 0].set_title("Precision")

    graph_cm[0, 1].bar(models_names, models_recall_data, color="green")
    graph_cm[0, 1].set_title("Recall")

    graph_cm[1, 0].bar(models_names, models_f1_data, color="purple")
    graph_cm[1, 0].set_title("F1 Score")

    graph_cm[1, 1].bar(models_names, models_accuracy_data, color="blue")
    graph_cm[1, 1].set_title("Accuracy")

    plt.show()
