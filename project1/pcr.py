from random import choice, randint

class PCRSimulation():
    def __init__(self):
        self.dna = DNA()

    def run(self, cycles=50):
        res = self.simulate(self.dna)
    
    def simulate(self, dna):
        # Denature
        strands = self.__denature(dna)
        
        # Anneal
        primed_strands = self.__anneal(strands)
        
        # Extend
        matching_three_strand = self.__extension(primed_strands[0])
        matching_five_strand = self.__extension(primed_strands[1])

        return [dna.combine_strands(strands[0], matching_three_strand), dna.combine_strands(strands[1], matching_five_strand)]


    def __denature(self, dna):
        # Reversing three prime strand for simplicity in interaction
        return [dna.five_prime, dna.three_prime[::-1]]

    def __anneal(self, strands):
        return [strands[0][20::], strands[1][20::]]

    def __extension(self, strand, fall_off_const=200):
        match = ""
        for i in range(fall_off_const+randint(-50,50)):
            match += self.dna.match_base_pair(strand[i])

        return match

class DNA():
    def __init__(self, five=None, three=None):
        self.five_prime = five
        self.three_prime = three
        
        if self.five_prime == None and self.three_prime == None:
            self.generate_random_dna()
    
    def generate_random_dna(self, base_pairs=300, amplify=1):
        self.five_prime = self.__generate_dna_template(base_pairs, amplify)
        self.three_prime = self.__match_template(self.five_prime)

    def match_base_pair(self, base):
        if base == "A":
            return "T"
        elif base == "T":
            return "A"
        elif base == "G":
            return "C"
        elif base == "C":
            return "G"

    def combine_strands(self, five, three):
        return DNA(five, three)
        
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
                


