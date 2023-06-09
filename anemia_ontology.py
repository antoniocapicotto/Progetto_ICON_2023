from owlready2 import *
import os

class anemia_ontology:
    def __init__(self):
        self.ontology = get_ontology(os.path.basename("anemia_symptoms.owl")).load()
        self.dict_symptoms = {}

    def get_symptoms_descriptions(self):
        dict_symptoms_onto = {}
        for i in self.ontology.individuals():
            dict_symptoms_onto[str(i)] = i.descrizione_sintomo

        for k in dict_symptoms_onto.keys():

            k1 = k
            k1 = k1.replace("untitled-ontology-4.istanza_","")
            self.dict_symptoms[k1] = dict_symptoms_onto[k]


    def print_symptoms(self):

        i = 1
        dict_nums_symptoms = {}
        dict_nums_keys = {}

        for k in self.dict_symptoms.keys():

            print("Sintomo [%d]: Nome: %s"%(i,k))
            dict_nums_symptoms[i] = self.dict_symptoms[k]
            dict_nums_keys[i] = k
            i = i + 1

        return dict_nums_symptoms, dict_nums_keys

#ontologia = anemia_ontology()
#ontologia.get_symptoms_descriptions()
#ontologia.print_symptoms()