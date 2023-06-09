from experta import *
from colorama import Fore
from anemia_data import anemia_data
from doctor_csp import doctor_csp
from pharmacy_csp import pharmacy_csp
from anemia_ontology import anemia_ontology

# valori di emoglobina soglia
ANEMIA_MALE_VALUE = 13.5
ANEMIA_FEMALE_VALUE = 12

# valori dell'MCH, MCHC, MCV
MAX_MCH_VALUE = 32 # macrocitica
MIN_MCH_VALUE = 26 # ipocromica-microcitica

MAX_MCHC_VALUE = 36 # anemia falciforme
MIN_MCHC_VALUE = 32 # ipocromica

MAX_MCV_VALUE = 100 # macrocitica
MIN_MCV_VALUE = 80  # microcitica



def reset_color():
    print(Fore.RESET)

def valid_response(response: str):

    valid = False
    response = response.lower()
    # modificato aggiungendo il sesso nelle valid response
    if response == "si" or response == "no":
        valid = True
    if response =='m' or response =='f':
        valid=True

    return valid



def valid_test_hb_value(test_value: float):

    valid = False
    if test_value <= 20:
        valid = True

    return valid


class anemia_expert(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(inizio="si")
        self.mean_anemia_tests = anemia_data().get_medium_values_anemia()
        self.number_prints = 0
        self.flag_no_symptoms = 0

        self.doc_analysis = doctor_csp("Studio del medico convenzionato")
        self.doc_analysis.addConstraint(lambda day,hours: hours >= 8 and hours <= 14 if day == "lunedi" else hours >= 15 and hours <= 20 if day == "giovedi" else None ,["day","hours"])
        self.pharmacy_analysis = pharmacy_csp()
        self.pharmacy_analysis.addConstraint(lambda farmaco, quantita: quantita <= 2 if farmaco in [solution['farmaci'] for solution in self.availability] else None ,["farmaci","quantita"])



    def print_facts(self):
        print("\n\nL'agente ragiona con i seguenti fatti: \n")
        print(self.facts)

    def _prototype_doc_booking(self, ask_text: str, doc_selected: doctor_csp):
        print("Vuoi prenotare un appuntamento presso un medico convenzionato? [si/no]")
        response = str(input())

        while valid_response(response) == False:
            print("Vuoi prenotare un appuntamento presso un medico convenzionato? [si/no]")
            response = str(input())
        
        if response == "si":
            first, last = doc_selected.get_availability()

            print("Insersci un turno inserendo il numero del turno associato")
            turn_input = int(input())

            while turn_input < first or turn_input > last:
                print("Insersci un turno inserendo il numero del turno associato")
                turn_input = int(input())
            
            doc_selected.print_single_availability(turn_input)

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
            self.declare(Fact(prenotazione_turno_medico="si"))

    @Rule(Fact(chedi_MCH='si'))
    def ask_MCH(self):
        print('Inserisci il valore di MCH')
        MCH_value=float(input("Inserisci il valore di MCH"))   
        if(MCH_value<MIN_MCH_VALUE):
            print("potresti avere l\'anemia microcitica")
        elif(MCH_value>MAX_MCH_VALUE):
            print("potresti avere l\'anemia macrocitica")
        else:
            print("i valori sono nella norma")



    @Rule(Fact(chedi_MCHC='si'))
    def ask_MCHC(self):
        print('Inserisci il valore di MCHC')
        MCHC_value=float(input("Inserisci il valore di MCHC"))   
        if(MCHC_value<MIN_MCHC_VALUE):
            print("potresti avere l\'anemia ipocromica")
        elif(MCHC_value>MAX_MCHC_VALUE):
            print("potresti avere l\'anemia falciforme")
        else:
            print("i valori sono nella norma")
    
    @Rule(Fact(chedi_MCV='si'))
    def ask_MCV(self):
        print('Inserisci il valore di MCV')
        MCV_value=float(input("Inserisci il valore di MCV"))   
        if(MCV_value<MIN_MCV_VALUE):
            print("potresti avere l\'anemia microcitica")
        elif(MCV_value>MAX_MCV_VALUE):
            print("potresti avere l\'anemia macrocitica")
        else:
            print("i valori sono nella norma")
    
    @Rule(Fact(chiedi_esami_tipo_anemia='si'))
    def rule_7(self):
        # chiedi se ha eseguito un test per l'MCH e se non lo fa , lui prenota il medico
        print("Hai eseguito un test dell\'MCH")
        mch_test = str(input())

        while valid_response(mch_test) == False:
            print("Hai eseguito un test dell\'MCH")
            mch_test = str(input())

        if mch_test == "si":
            self.declare(Fact(chiedi_MCH="si"))
        else:
            self.declare(Fact(chedi_MCH="no"))

        if  mch_test == "no":
            self.declare(Fact(prenotazione_turno_medico="si"))
        # chiedi se ha eseguito un test per l'MCHC e se non lo fa , lui prenota il medico
        print("Hai eseguito un test dell\'MCHC")
        mchc_test = str(input())

        while valid_response(mchc_test) == False:
            print("Hai eseguito un test dell\'MCHC")
            mchc_test = str(input())

        if mchc_test == "si":
            self.declare(Fact(chiedi_MCHC="si"))
        else:
            self.declare(Fact(chedi_MCHC="no"))

        if  mchc_test == "no":
            self.declare(Fact(prenotazione_turno_medico="si"))
        # chiedi se ha eseguito un test per l'MCV e se non lo fa , lui prenota il medico
        print("Hai eseguito un test dell\'MCV")
        mcv_test = str(input())

        while valid_response(mcv_test) == False:
            print("Hai eseguito un test dell\'MCV")
            mcv_test = str(input())

        if mcv_test == "si":
            self.declare(Fact(chiedi_MCV="si"))
        else:
            self.declare(Fact(chedi_MCV="no"))

        if  mcv_test == "no":
            self.declare(Fact(prenotazione_turno_medico="si"))
        
    

    @Rule(Fact(prenotazione_turno_medico="si"))
    def prenotazione_turno(self):
        self._prototype_doc_booking("prenotazione dal medico", self.doc_analysis)
        
        
    @Rule(Fact(test_emoglobina="si"))
    def rule_3(self):
        
        sesso = input("Il soggetto e' maschio o femmina? [m/f]\n")
        while(valid_response(sesso)==False):
            sesso = input("Il soggetto e' maschio o femmina? [m/f]\n")
        if (sesso=='m'):
            print("Inserisci il valore del test")
            test_value = float(input())
            while valid_test_hb_value(test_value) == False:
                print("Inserisci il valore del test")
                test_value = float(input())
            if test_value < ANEMIA_MALE_VALUE:
                self.declare(Fact(anemia="si"))
            else:
                self.declare(Fact(anemia="no"))
        elif(sesso=='f'):
            print("Inserisci il valore del test")
            test_value = float(input())
            while valid_test_hb_value(test_value) == False:
                print("Inserisci il valore del test")
                test_value = float(input())
            if test_value < ANEMIA_FEMALE_VALUE:
                self.declare(Fact(anemia="si"))
            else:
                self.declare(Fact(anemia="no"))
        

        if(Fact(anemia='si')):
            self.declare(Fact(chiedi_MCH='si'))
            self.declare(Fact(chiedi_MCHC='si'))
            self.declare(Fact(chiedi_MCV='si'))
            self.declare(Fact(chiedi_prenotazione_farmaci='si'))



        # Non fa bene il controllo sul valore dell'emoglobina
        # OUTPUT (quando è anemico)
        # Il valore di emoglobina è maggiore del valore minimo
        # Potresti avere l'anemia
        if(Fact(anemia='no')):
            print(Fore.GREEN+'Il valore di emoglobina è maggiore del valore minimo')
            reset_color()
            
    @Rule(Fact(chiedi_prenotazione_farmaci='si'))
    def rule_8(self):
        prenota_farmaci("prenotazione farmaci",self.pharmacy_analysis)
        


    def prenota_farmaci(self, ask_text: str, pharmacy_selected: pharmacy_csp):
        print("Vuoi prenotare farmaci presso una farmacia convenzionata? [si/no]")
        response = str(input())

        while valid_response(response) == False:
            print("Vuoi prenotare farmaci presso una farmacia convenzionata? [si/no]")
            response = str(input())
        
        if response == "si":
            first, last = pharmacy_selected.get_availability()

            print("Insersci un turno inserendo il numero del turno associato")
            turn_input = int(input())

            while turn_input < first or turn_input > last:
                print("Insersci un turno inserendo il numero del turno associato")
                turn_input = int(input())
            
            doc_selected.print_single_availability(turn_input)


    @Rule(Fact(chiedi_sintomi="si"))
    def rule_5(self):

        r1 = self._prototype_ask_symptom("Ti affatichi molto più del solito quando fai attività motoria? [si/no]", Fact(affaticamento_motorio="si"))
        r2 = self._prototype_ask_symptom("Soffri di dolori alla testa ultimamente? (cefalea) [si/no]", Fact(mal_di_testa="si"))
        r3 = self._prototype_ask_symptom("La tua pelle e' pallida? [si/no]", Fact(pallore_pelle="si"))
        r4 = self._prototype_ask_symptom("Avverti una sensazione di freddo? [si/no]", Fact(sensazione_freddo="si"))
        r5 = self._prototype_ask_symptom("Ti senti molto stanco? [si/no]", Fact(stanchezza="si"))
        r6 = self._prototype_ask_symptom("Le tue unghie sono molto fragili? [si/no]", Fact(unghie_fragili="si"))

        if r1 == "no" and r2 == "no" and r3 == "no" and r4 == "no" and r5 == "no" and r6 == "no":
            self.flag_no_symptoms = 1 # non ci sono i sintomi

    @Rule(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si")))
    def all_anemia_symptoms(self):
        print("Sembra che tu abbia TUTTI i sintomi dell'anemia")
        self.declare(Fact(tutti_sintomi="si"))
        self.declare(Fact(chiedi_esami_emoglobina="si"))
        
    @Rule(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si"), Fact(anemia="si")))
    def all_anemia_diagnosis_3(self):
        print(Fore.RED + "Potresti avere l'anemia")
        reset_color()
        self.declare(Fact(anemia_tutti_sintomi = "si"))

    @Rule(NOT(AND(Fact(affaticamento_motorio="si"), Fact(mal_di_testa="si"), Fact(pallore_pelle="si"), Fact(sensazione_freddo="si"), Fact(stanchezza="si"), Fact(unghie_fragili="si"))))
    def not_symptoms(self):

        if self.number_prints == 0 and self.flag_no_symptoms == 1:

            print(Fore.GREEN + "Non hai alcun sintomo dell'anemia")
            self.declare(Fact(niente_sintomi="si"))
            reset_color()
            self.number_prints = self.number_prints + 1

    @Rule(NOT(OR(Fact(diagnosi_anemia="si"),Fact(anemia_tutti_sintomi = "si"),Fact(tutti_sintomi="si"))))
    def intermediate_case(self):

        if self.flag_no_symptoms != 1:

            print(Fore.YELLOW + "Potresti avere l'anemia")
            self.declare(Fact(diagnosi_anemia_incerta = "si"))
            reset_color()
            # impostare il fact del test dell'emoglobina a si
            self.declare(Fact(chiedi_esami_emoglobina='si'))

        

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
# cambiare il printf con un'altra formula di benvenuto
    print("Benvenuto in Anemia Expert, un sistema esperto per la diagnosi e la cura del anemia")
    while exit_program == False:

# --> chiedere se è maschio o femmina ?
# --> chiedere i suoi sintomi attuali
# --> test emoglobina (utilizzare e salvare in una variabile un flag 
# per capire se è maschio o femmina e utilizzarlo per il test) 
# se non l'ha fatto va dal medico altrimenti inserisce il valore 
# --> dopo esce scritto sei anemico oppure no 
# --> se è anemico allora continua la diagnosi chiedendo MCH, MCHC e MCV altrimenti se non li ha i valori va dal medico
# --> chiedere se vuole mostrare dei trattamenti per i suoi sintomi

        print("\n[1] Mostra i possibili sintomi del'anemia\n[2] Esegui una diagnosi\n[3] Esci")
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

    
    
