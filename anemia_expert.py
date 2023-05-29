from experta import *
from colorama import Fore
from anemia_data import anemia_data
from doctor_csp import doctor_csp
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

        self.lab_hb_analysis = doctor_csp("Laboratorio Analisi dell'emoglobina nei globuli rossi")
        self.lab_hb_analysis.addConstraint(lambda day,hours: hours >= 8 and hours <= 14 if day == "lunedi" else hours >= 15 and hours <= 20 if day == "giovedi" else None ,["day","hours"])

    def print_facts(self):
        print("\n\nL'agente ragiona con i seguenti fatti: \n")
        print(self.facts)

    def _prototype_lab_booking(self, ask_text: str, lab_selected: doctor_csp):
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

    @Rule(Fact(test_emoglobina="si"))
    def rule_3(self):
        sesso = input("Il soggetto e' maschio o femmina?")
        if (sesso=='maschio'):
            print(
                "Inserisci il valore del test [mmol/L]")
            test_value = float(input())
            while valid_test_hb_value(test_value) == False:
                print("Inserisci il valore del test [mmol/L]")
                test_value = float(input())
            if test_value < ANEMIA_MALE_VALUE:
                self.declare(Fact(anemia="si"))
            else:
                self.declare(Fact(anemia="no"))
        elif(sesso=='femmina'):
            print("Inserisci il valore del test [mmol/L]")
            test_value = float(input())
            while valid_test_hb_value(test_value) == False:
                print("Inserisci il valore del test [mmol/L]")
                test_value = float(input())
            if test_value < ANEMIA_FEMALE_VALUE:
                self.declare(Fact(anemia="si"))
            else:
                self.declare(Fact(anemia="no"))

    @Rule(Fact(chiedi_sintomi="si"))
    def rule_5(self):

        r1 = self._prototype_ask_symptom("Ti affatichi molto più del solito quando fai attività motoria? [si/no]", Fact(affaticamento_motorio="si"))
        r2 = self._prototype_ask_symptom("Soffri di dolori alla testa ultimamente? (cefalea) [si/no]", Fact(mal_di_testa="si"))
        r3 = self._prototype_ask_symptom("La tua pelle e' pallida? [si/no]", Fact(pallore_pelle="si"))
        r4 = self._prototype_ask_symptom("Avverti una sensazione di freddo? [si/no]", Fact(sensazione_freddo="si"))
        r5 = self._prototype_ask_symptom("Ti senti molto stanco? [si/no]", Fact(stanchezza="si"))
        r6 = self._prototype_ask_symptom("Le tue unghie sono molto fragili? [si/no]", Fact(unghie_fragili="si"))

        if r1 == "no" and r2 == "no" and r3 == "no" and r4 == "no" and r5 == "no" and r6 == "no":
            self.flag_no_symptoms = 1

    @Rule(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si")))
    def all_anemia_symptoms(self):
        print("Sembra che tu abbia TUTTI i sintomi del diabete")
        self.declare(Fact(tutti_sintomi="si"))
        self.declare(Fact(chiedi_esami_emoglobina="si"))
        
    @Rule(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si"), Fact(anemia="si")))
    def all_anemia_diagnosis_3(self):
        print(Fore.RED + "Hai sicuramente l'anemia")
        reset_color()
        self.declare(Fact(anemia_tutti_sintomi = "si"))

    @Rule(NOT(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si"))))
    def not_symptoms(self):

        if self.number_prints == 0 and self.flag_no_symptoms == 1:

            print(Fore.GREEN + "Non hai alcun sintomo dell'anemia")
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

    
    
