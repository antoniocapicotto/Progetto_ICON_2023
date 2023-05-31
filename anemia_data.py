import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ANEMIA_DATA_FILE = "anemia.csv"
TARGET = "Result"


class anemia_data:

    def __init__(self):
        self.data = pd.read_csv(ANEMIA_DATA_FILE).dropna()
        self.features_list = list(self.data.columns)

    def get_data(self):
        return self.data

    def get_features(self):
        return self.features_list

    def get_heatmap(self):
        sns.heatmap(self.data.corr(), annot=True)
        plt.show()

    def plot_results(self):
        plt.style.use("ggplot")
        self.data[TARGET].value_counts().plot.bar(title='Result', rot=0)
        plt.show()

    def plot_hemoglobin(self):
        plt.style.use("ggplot")
        list_hemoglobin = []

        for hb in self.data["Hemoglobin"]:
            for h in range(0, 20, 5):
                if hb >= h and hb <= (h + 4.9):
                    label = "%d-%.1f" % (h, (h + 4.9))
                    list_hemoglobin.append(label)

        pd.DataFrame(list_hemoglobin).value_counts().plot.bar(
            title='Hemoglobin', rot=0)
        plt.show()

    def plot_MCHC(self):
        plt.style.use("ggplot")
        list_MCHC = []

        for mchc in self.data["MCHC"]:
            for m in range(20, 40, 5):
                if mchc >= m and mchc <= (m + 4.9):
                    label = "%d-%.1f" % (m, (m + 4.9))
                    list_MCHC.append(label)

        pd.DataFrame(list_MCHC).value_counts().plot.bar(
            title='MCHC', rot=0)
        plt.show()

    def plot_MCV(self):
        plt.style.use("ggplot")
        list_MCV = []

        for mcv in self.data["MCV"]:
            for m in range(60, 100, 10):
                if mcv >= m and mcv <= (m + 9.9):
                    label = "%d-%.1f" % (m, (m + 9.9))
                    list_MCV.append(label)

        pd.DataFrame(list_MCV).value_counts().plot.bar(
            title='MCV', rot=0)
        plt.show()

    def get_training_data(self):
        y = self.data[[TARGET]].values
        x = self.data.drop(TARGET, axis='columns').values
        return x, y

    def get_medium_values_anemia(self):
        medium_values = {}
        positives = self.data[self.data[TARGET] == 1]

        medium_values['Hemoglobin'] = positives['Hemoglobin'].mean()
        medium_values['MCHC'] = positives['MCHC'].mean()
        medium_values['MCV'] = positives['MCV'].mean()

        return medium_values
