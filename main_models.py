from anemia_data import anemia_data
from model_comparison import *
from models import *

data = anemia_data()
default_test_size = 0.5

data.get_heatmap()
data.plot_results()
data.plot_hemoglobin()
data.plot_MCHC()
data.plot_MCV()

# logistic regression to predict anemia
model_1 = anemia_logistic_regression(data, 100, default_test_size)
model_1.predict()

print("\nLogistic Regression metrics")
model_1.print_metrics()
model_1.get_confusion_matrix()

print("\n\n")

# decision tree to predict anemia
model_2 = anemia_decision_tree(data, 50, default_test_size)
model_2.predict()

print("Decision tree metrics")
model_2.print_metrics()
model_2.get_confusion_matrix()

print("\n\n")

# k-nearest neighbors to predict anemia
model_3 = anemia_knn(data, default_test_size, 21)
model_3.predict()

print("K-Nearest Neighbors metrics")
model_3.print_metrics()
model_3.get_confusion_matrix()

# model comparisons
metrics_graph_lr(data, default_test_size)
metrics_graph_dt(data, default_test_size)
metrics_graph_knn(data, default_test_size)
comparison_metrics_models(data, default_test_size)
