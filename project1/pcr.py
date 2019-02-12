from random import choice

class PCRSimulation():
    def __init__(self):
        self.dna = DNA()
    
    def run(self, cycles=50):
        # Denature
        # Anneal
        # Extend
        pass
    

    def __denature(self):
        pass

    def __anneal(self):
        pass

    def __extension(self):
        pass

class DNA():
    def __init__(self, base_pairs=2000, amplify=200):
        self.five_prime = self.__generate_dna_template(base_pairs, amplify)
        self.three_prime = self.__match_template(self.five_prime)

    def __generate_dna_template(self, base_pairs, amplify):
        dna = ""

        for i in range(base_pairs):
            dna+= choice("ATGC")

        return (dna * amplify)

    def __match_template(self, templ):
        dna = ""
        
        for b in templ:
            if b == "A":
                dna += "T"
            elif b == "T":
                dna += "A"
            elif b == "G":
                dna += "C"
            elif b == "C":
                dna += "G"

        return dna
                


