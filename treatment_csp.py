from constraint import *

class treatment_csp(Problem):
    def __init__(self, solver=None):
        super().__init__(solver=solver)
        self.symptoms = ['affaticamento_motorio', 'mal_di_testa', 'pallore_pelle', 'sensazione_freddo', 'stanchezza', 'unghie_fragili']
        self.treatments = ['integrazione_di_ferro', 'idratazione_adeguata', 'supplementi_vitaminici', 'dieta_equilibrata', 'esercizio_regolare']
        self.assignments = {}

        # Aggiungi le variabili del problema (trattamenti per sintomi)
        for symptom in self.symptoms:
            self.addVariable(symptom, self.treatments)

        # Aggiungi i vincoli del problema (sintomo legato a un trattamento)
        for symptom in self.symptoms:
            self.addConstraint(lambda symptom, treatment, s=symptom, t=treatment: self.check_symptom_treatment(s, t), [symptom, treatment])

    def check_symptom_treatment(self, symptom, treatment):
        symptom_treatment_mapping = {
            'affaticamento_motorio': 'integrazione_di_ferro',
            'mal_di_testa': 'idratazione_adeguata',
            'pallore_pelle': 'supplementi_vitaminici',
            'sensazione_freddo': 'esercizio_regolare',
            'stanchezza': 'dieta_equilibrata',
            'unghie_fragili': 'integrazione_di_ferro'
        }

        return symptom_treatment_mapping[symptom] == treatment

    def solve_anemia_csp(self):
        # Risolvi il problema CSP
        solutions = self.getSolutions()

        # Se ci sono soluzioni, restituisci la prima soluzione trovata
        if solutions:
            self.assignments = solutions[0]
            return self.assignments
        else:
            return None

    def get_symptom_treatment(self, symptom):
        # Ottieni il trattamento assegnato a un sintomo
        if symptom in self.assignments:
            return self.assignments[symptom]
        else:
            return None

# Esempio di utilizzo della classe treatment_csp

# Crea un'istanza del problema CSP per i trattamenti dell'anemia basati sui sintomi
problem = treatment_csp()

# Risolvi il problema CSP
solutions = problem.solve_anemia_csp()

if solutions:
    # Stampa la soluzione
    for symptom, treatment in solutions.items():
        print(f"Sintomo {symptom}: Trattamento {treatment}")
else:
    print("Nessuna soluzione trovata.")
