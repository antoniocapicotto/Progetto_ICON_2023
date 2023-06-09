from constraint import *


class pharmacy_csp(Problem):

    def __init__(self, solver=None):
        super().__init__(solver=solver)
        self.farmaci = self.addVariable("farmaci", ["vitamina_b12", "integratore_ferro", "paracetamolo", "integratore_biotina", "vitamina_c"])
        self.quantita = self.addVariable("quantita", [1, 2, 3, 4])
        self.availability = None

    def prenota_farmaco(self):
        self.availability = self.getSolutions()
        choices = []

        if len(self.availability) > 0:
            print("Farmaci disponibili:\n")
            for index, solution in enumerate(self.availability):
                farmaco = solution['farmaci']
                quantita = solution['quantita']
                choices.append((farmaco, quantita))
                #print("%d. Farmaco: %s, Quantità: %d" % (index + 1, farmaco, quantita))
        else:
            print("Nessun farmaco disponibile.")

        return choices



    def stampa_soluzione(self):
        if self.availability is not None:
            print("Prenotazione effettuata:\n")
            for solution in self.availability:
                print("Farmaco: %s, Quantità: %d" % (solution['farmaci'], solution['quantita']))
        else:
            print("Nessuna soluzione trovata.")

