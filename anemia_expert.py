from experta import *
from colorama import Fore
from anemia_data import anemia_data
from laboratory_csp import laboratory_csp
from anemia_ontology import anemia_ontology

ANEMIA_MALE_VALUE = 13.5
ANEMIA_FEMALE_VALUE = 12

def reset_color():
    print(Fore.RESET)

def valid_response(response: str):

    valid = False
    response = response.lower()

    if response == "si" or response == "no":
        valid = True

    return valid


def valid_male_test_hb_value(test_value: float):

    valid = False

    if test_value >= 13.5:
        valid = True

    return valid

def valid_female_test_hb_value(test_value: float):

    valid = False

    if test_value >= 12:
        valid = True

    return valid


class anemia_expert(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(inizio="si")
        self.mean_anemia_tests = anemia_data().get_medium_values_anemia()
        self.number_prints = 0
        self.flag_no_symptoms = 0

        self.lab_hb_analysis = laboratory_csp("Laboratorio Analisi dell'emoglobina nei globuli rossi")
        self.lab_hb_analysis.addConstraint(lambda day,hours: hours >= 8 and hours <= 14 if day == "lunedi" else hours >= 15 and hours <= 20 if day == "giovedi" else None ,["day","hours"])

    def print_facts(self):
        print("\n\nL'agente ragiona con i seguenti fatti: \n")
        print(self.facts)

    def _prototype_lab_booking(self, ask_text: str, lab_selected: laboratory_csp):
        print("Hai avuto la prescrizione per %s, vuoi prenotare presso uno studio convenzionato? [si/no]" %ask_text)
        response = str(input())

        while valid_response(response) == False:
            print("Hai avuto la prescrizione per %s, vuoi prenotare presso uno studio convenzionato? [si/no]"%ask_text)
            response = str(input())
        
        if response == "si":
            first, last = lab_selected.get_availability()

            print("Insersci un turno inserendo il numero del turno associato")
            turn_input = int(input())

            while turn_input < first or turn_input > last:
                print("Insersci un turno inserendo il numero del turno associato")
                turn_input = int(input())
            
            lab_selected.print_single_availability(turn_input)

    def _prototype_ask_symptom(self, ask_text: str, fact_declared: Fact):

        print(ask_text)
        response = str(input())

        while valid_response(response) == False:
            print(ask_text)
            response = str(input())
        if response == "si":
            self.declare(fact_declared)

        return response

    @Rule(Fact(inizio="si"))
    def rule_1(self):
        print(Fore.CYAN + "\nInizio della diagnosi...\n")
        reset_color()
        self.declare(Fact(chiedi_sintomi="si"))

    @Rule(Fact(chiedi_esami_emoglobina="si"))
    def rule_2(self):
        print("Hai eseguito un test dell'emoglobina?")
        hb_test = str(input())

        while valid_response(hb_test) == False:
            print("Hai eseguito un test dell'emoglobina?")
            hb_test = str(input())


        if hb_test == "si":
            self.declare(Fact(test_emoglobina="si"))
        else:
            self.declare(Fact(test_emoglobina="no"))

        if  hb_test == "no":
            self.declare(Fact(prescrizione_esami_emoglobina="si"))

    @Rule(Fact(test_casuale_sangue="si"))
    def rule_3(self):
        print(
            "Inserisci il valore del test espresso in millimoli su litro [mmol/L]")
        test_value = float(input())

        while valid_random_test_blood_value(test_value) == False:
            print("Inserisci il valore del test espresso in millimoli su litro [mmol/L]")
            test_value = float(input())

        if test_value > ANEMIA_RANDOM_TEST:
            self.declare(Fact(glicemia_casuale_alta="si"))

        else:
            self.declare(Fact(glicemia_normale="si"))

    @Rule(Fact(test_digiuno_sangue="si"))
    def rule_4(self):
        print(
            "Inserisci il valore del test espresso in millimoli su litro [mmol/L]")
        test_value = float(input())

        while valid_random_test_blood_value(test_value) == False:
            print(
                "Inserisci il valore del test espresso in millimoli su litro [mmol/L]")
            test_value = float(input())

        if test_value > ANEMIA_FASTING_TEST:
            self.declare(Fact(glicemia_digiuno_alta="si"))
        else:
            self.declare(Fact(glicemia_normale="si"))

    @Rule(Fact(chiedi_sintomi="si"))
    def rule_5(self):

        r1 = self._prototype_ask_symptom("Ti senti molto assetato di solito (sopratutto di notte) ? [si/no]", Fact(molta_sete="si"))
        r2 = self._prototype_ask_symptom("Ti senti molto stanco? [si/no]", Fact(molto_stanco="si"))
        r3 = self._prototype_ask_symptom("Stai perdendo peso e massa muscolare? [si/no]", Fact(perdita_massa="si"))
        r4 = self._prototype_ask_symptom("Senti prurito? [si/no]", Fact(prurito="si"))
        r5 = self._prototype_ask_symptom("Hai la vista offuscata? [si/no]", Fact(vista_offuscata="si"))
        r6 = self._prototype_ask_symptom("Consumi spesso bevande/alimenti zuccherati? [si/no]", Fact(bevande_zuccherate="si"))
        r7 = self._prototype_ask_symptom("Hai fame costantemente? [si/no]", Fact(fame_costante="si"))
        r8 = self._prototype_ask_symptom("Hai spesso la bocca asciutta? [si/no]", Fact(bocca_asciutta="si"))

        if r1 == "no" and r2 == "no" and r3 == "no" and r4 == "no" and r5 == "no" and r6 == "no" and r7 == "no" and r8 == "no":
            self.flag_no_symptoms = 1

        self.declare(Fact(chiedi_imc="si"))


    @Rule(Fact(chiedi_imc="si"))
    def ask_bmi(self):

        medium_bmi_anemia = self.mean_anemia_tests['BMI']

        print(Fore.CYAN + "\n\nInserisci l'altezza in centimetri")
        reset_color()
        height = int(input())

        while height < 135 or height > 220:
            print(Fore.CYAN + "Inserisci di nuovo l'altezza in centimetri")
            reset_color()
            height = int(input())

        print(Fore.CYAN + "Inserisci il peso in kilogrammi")
        reset_color()
        weight = int(input())

        while weight < 30 or weight > 250:
            print(Fore.CYAN + "Inserisci DI NUOVO il peso in kilogrammi")
            reset_color()
            weight = int(input())

        bmi = round(height/(weight*weight), 3)

        if bmi >= medium_bmi_anemia:
            print(Fore.YELLOW + "Il valore del tuo indice di massa corporea paria a %f e' superiore al valore medio di indice di massa corporea dei diabetici" % bmi)
            reset_color()

    @Rule(Fact(esami_pressione="si"))
    def ask_pressure_exam(self):
        print("Hai fatto l'esame della pressione sanguigna?")
        response = str(input())

        while valid_response(response) == False:
            print("Hai fatto l'esame della pressione sanguigna?")
            response = str(input())

        if response == "si":
            self.declare(Fact(esame_pressione_eseguito="si"))
        else:
            self.declare(Fact(prescrizione_esame_pressione="no"))
    
    @Rule(Fact(prescrizione_esame_pressione="no"))
    def pressure_exams_book(self):
        self._prototype_lab_booking("gli esami della pressione", self.lab_pressure_analysis)

    @Rule(Fact(esame_pressione_eseguito="si"))
    def pressure_exam(self):

        medium_pressure = self.mean_anemia_tests['BloodPressure']

        print("Inserisci il valore della pressione sanguigna")
        pressure_value = int(input())

        while valid_blood_pressure(pressure_value) == False:
            print("Inserisci il valore della pressione sanguigna")
            pressure_value = int(input())

        if pressure_value >= medium_pressure:
            self.declare(Fact(diagnosi_pressione_diabete="si"))

        else:
            self.declare(Fact(diagnosi_pressione_normale="si"))

    @Rule(Fact(diagnosi_pressione_normale="si"))
    def normal_blood_pressure(self):
        print("Il valore della pressione sembra nella norma")

    @Rule(Fact(diagnosi_pressione_diabete="si"))
    def blood_pressure_anemia(self):
        print("Il valore della pressione e' maggiore o uguale a quella dei diabetici")

    @Rule(OR(Fact(fame_costante="si"), Fact(bevande_zuccherate="si")))
    def exam_1(self):
        self.declare(Fact(chiedi_esami_glicemia="si"))

    @Rule(OR(Fact(vista_offuscata="si"), Fact(molto_stanco="si"), Fact(bocca_asciutta="si")))
    def exam_2(self):
        self.declare(Fact(esami_pressione="si"))

    @Rule(AND(Fact(molta_sete="si"), Fact(molto_stanco="si"), Fact(perdita_massa="si"), Fact(prurito="si"), Fact(vista_offuscata="si"), Fact(bevande_zuccherate="si"), Fact(fame_costante="si"), Fact(bocca_asciutta="si")))
    def all_anemia_symptoms(self):
        print("Sembra che tu abbia TUTTI i sintomi del diabete")
        self.declare(Fact(tutti_sintomi="si"))
        self.declare(Fact(chiedi_esami_glicemia="si"))
        self.declare(Fact(esami_pressione="si"))

    @Rule(AND(Fact(molta_sete="si"), Fact(molto_stanco="si"), Fact(perdita_massa="si"), Fact(prurito="si"), Fact(vista_offuscata="si"), Fact(bevande_zuccherate="si"), Fact(fame_costante="si"), Fact(bocca_asciutta="si")), Fact(diagnosi_pressione_diabete="si"), Fact(glicemia_digiuno_alta="si"), Fact(glicemia_casuale_alta="si"), Fact(diagnosi_pressione_diabete="si"), Fact(insulina_alta_diabete="si"))
    def all_anemia_diagnosis_3(self):
        print(Fore.RED + "Hai sicuramente il diabete")
        reset_color()
        self.declare(Fact(diabete_tutti_sintomi = "si"))

    @Rule(OR(Fact(prurito="si"), Fact(perdita_massa="si")))
    def ask_itching_test(self):
        print("Hai fatto un test per misurare lo spessore della piega cutanea del tricipite?")
        response = str(input())

        while valid_response(response) == False:
            print("Hai fatto un test per misurare lo spessore della piega cutanea del tricipite?")
            response = str(input())

        if response == "si":
            self.declare(Fact(esame_pelle="si"))

        else:
            self.declare(Fact(prescrizione_esame_pelle="si"))
    
    @Rule(Fact(prescrizione_esame_pelle="si"))
    def skin_exams_book(self):

       self._prototype_lab_booking("gli esami della pelle", self.lab_skin_analysis)

    @Rule(Fact(esame_pelle="si"))
    def itching_test(self):

        medium_anemia_thickness = self.mean_anemia_tests['SkinThickness']
        print("Hai detto di aver fatto l'esame per misurare lo spessore della piega cutanea del tricipite")

        print("Inserisci il valore in millimetri")
        skin_thick = int(input())

        while skin_thick < MINIMUM_SKIN_TICKNESS or skin_thick > MAXIMUM_SKIN_TICKNESS:
            print("Inserisci DI NUOVO il valore in millimetri")
            skin_thick = int(input())

        if skin_thick >= medium_anemia_thickness:
            print(Fore.YELLOW + "Lo spessore della pelle e' maggiore o uguale a quello dei diabetici, prova a fare altri esami!")
            reset_color()

    @Rule(OR(Fact(fame_costante="si"), Fact(bevande_zuccherate="si")))
    def ask_insulin_exam(self):

        print("Hai eseguito un test per misurare il valore di insulina")
        response = str(input())

        while valid_response(response) == False:
            print("Hai eseguito un test per misurare il valore di insulina")
            response = str(input())

        if response == "si":
            self.declare(Fact(test_insulina="si"))

        else:
            self.declare(Fact(prescrivi_test_insulina="si"))

    @Rule(Fact(test_insulina="si"))
    def insulin_exam(self):

        medium_insulin_anemia = self.mean_anemia_tests['Insulin']

        print("Insersci il valore dell'insulina espresso in mu U/ml")
        insulin_value = float(input())

        while insulin_value < 0 or insulin_value > 700:
            print("Insersci il valore dell'insulina espresso in mu U/ml")
            insulin_value = float(input())

        if insulin_value >= medium_insulin_anemia:
            self.declare(Fact(insulina_alta_diabete="si"))

    @Rule(Fact(prescrivi_test_insulina="si"))
    def insulin_prescription(self):
        print(Fore.YELLOW + "Dovresti fare il test per misurare l'insulina")
        reset_color()

        self._prototype_lab_booking("gli esami dell' insulina", self.lab_insulin_analysis)

    @Rule(AND(Fact(insulina_alta_diabete="si"),NOT(Fact(diagnosi_diabete_incerta = "si"))))
    def diagnosis_4(self):
        print(Fore.RED + "Hai il diabete")
        reset_color()
        self.declare(Fact(diagnosi_diabete="si"))

    @Rule(Fact(prescrizione_esami_sangue="si"))
    def prescription_1(self):
        print(Fore.RED + "Dovresti fare gli esami per misurare la glicemia nel sangue!")
        reset_color()

        self._prototype_lab_booking("gli esami della glicemia nel sangue",self.lab_glucose_analysis)

    @Rule(Fact(glicemia_normale="si"))
    def normal_blood_glucose(self):
        print(Fore.GREEN + "La glicemia e' nella norma")
        reset_color()

    @Rule(NOT(AND(Fact(molta_sete="si"),Fact(molto_stanco="si"),Fact(perdita_massa="si"),Fact(prurito="si"),Fact(vista_offuscata="si"),Fact(bevande_zuccherate="si"),Fact(fame_costante="si"),Fact(bocca_asciutta="si"))))
    def not_symptoms(self):

        if self.number_prints == 0 and self.flag_no_symptoms == 1:

            print(Fore.GREEN + "Non hai alcun sintomo del diabete")
            self.declare(Fact(niente_sintomi="si"))
            reset_color()
            self.number_prints = self.number_prints + 1

    @Rule(NOT(OR(Fact(diagnosi_diabete="si"),Fact(diabete_tutti_sintomi = "si"),Fact(tutti_sintomi="si"))))
    def intermediate_case(self):

        if self.flag_no_symptoms != 1:

            print(Fore.YELLOW + "Potresti avere il diabete, rivolgiti ad un medico")
            self.declare(Fact(diagnosi_diabete_incerta = "si"))
            reset_color()

def main_agent():
    expert_agent = anemia_expert()
    expert_agent.reset()
    expert_agent.run()
    expert_agent.print_facts()

def main_ontology():
    do = anemia_ontology()

    do.get_symptoms_descriptions()
    symptoms, keys_symptoms = do.print_symptoms()

    print("\nSeleziona il sintomo di cui vuoi conosere la descrizione, inserisci il numero del sintomo")
    symptom_number = int(input())

    while symptom_number not in symptoms.keys():
        print("\nSeleziona il sintomo di cui vuoi conosere la descrizione, inserisci il numero del sintomo")
        symptom_number = int(input())
            
    print("Sintomo: %s, descrizione: %s"%(keys_symptoms[symptom_number]," ".join(symptoms[symptom_number])))

if __name__ == '__main__':

    exit_program = False

    print("Benvanuto in Anemia Expert, un sistema esperto per la diagnosi e la cura del diabete di tipo 1")
    while exit_program == False:

        print("----------->MENU<-----------\n[1] Mostra i possibili sintomi del diabete\n[2] Esegui una diagnosi\n[3] Esci")
        user_choose = None

        try:
            user_choose = int(input())
        
        except ValueError:
            exit_program = True

        if user_choose == 1:
            main_ontology()

        elif user_choose == 2:
            main_agent()
        
        else:
            print("Uscita dal programma...")
            exit_program = True
        
        print("\n\n")

    
    
