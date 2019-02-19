import random
from dna import dna1

class DNA:
    def __init__(self, three_to_five, five_to_three):
        self.three = three_to_five
        self.five = five_to_three

BASE_MAP = {
    'a': 't',
    't': 'a',
    'g': 'c',
    'c': 'g',
}

def complement(strand):
    return ''.join([BASE_MAP[base] for base in strand])

STARTER_THREE = dna1
STARTER_FIVE = complement(STARTER_THREE)

PRIMER_LENGTH = 20
EXTENSION_LEN = 200
CYCLE_LIMIT = 15
FALL_OFF = 50

# Primer specifically created to target the strand mentioned above
PRIMER1 = "GCCACTACAATTGTATCTAA".lower()
PRIMER2 = complement("ACCGGTGTACGATTCAACTA".lower())
TARGET = "GCCGTGTAATGAGAACATCCACACCTTAGTGAATCGATGC\
CGCCGCTTCGGAATACCGTTTTGGCTACCTGTTACTAAGCCCATCGCGATTTTCAGGTAA\
TCGTGCACGTAGGGTTGCACCGCACGCATGTCGAACTGGTGGCGAAGTACGATTCCACGG".lower()

def pcr(dna_strand):
    # Denaturation - split DNA into single template strands
    three = dna_strand.three
    five = dna_strand.five[::-1]
    three_binding_fail = False
    five_binding_fail = False
    # Annealing - introduction of primers
    try:
        three_start = three.index(PRIMER1)
    except ValueError:
        three_binding_fail = True
    try:
        five_start = five.index(PRIMER2[::-1])
    except ValueError:
        five_binding_fail = True

    # Elongation - extend primer with bases complementary to template strand
    five_complement = ""
    three_complement = ""
    for i in range(EXTENSION_LEN + PRIMER_LENGTH * 2 + random.randint(-FALL_OFF, FALL_OFF)):
        if not three_binding_fail:
            try:
                three_complement += BASE_MAP[three[i + three_start]]
            except: pass
        if not five_binding_fail:
            try:
                five_complement += BASE_MAP[five[i + five_start]]
            except: pass

    

    if not three_binding_fail:
        new_strand1 = DNA(three, three_complement)
    else:
        new_strand1 = None
    if not five_binding_fail:
        new_strand2 = DNA(five_complement[::-1], five[::-1])
    else:
        new_strand2 = None

    return (new_strand1, new_strand2)

# Our starting DNA
starter = DNA(STARTER_THREE, STARTER_FIVE)

# A queue for DNA strands to be PCR'd
strand_buffer = [starter]

for i in range(CYCLE_LIMIT):
    # Iterate through strands that were in the buffer before this loop executes
    print(i)
    for j in range(len(strand_buffer)):
        # Aquire two new DNA strands through PCR of one strand

        new_strands = pcr(strand_buffer[0])
        
        # Remove current strand from buffer (this strand would no longer exist after real PCR)
        strand_buffer.pop(0)

        # Add our new strands to the buffer to be processed in the next loop of CYCLE_LIMIT
        if new_strands[0] is not None:
            strand_buffer.append(new_strands[0])
        if new_strands[1] is not None:
            strand_buffer.append(new_strands[1])

print(f"{len(strand_buffer)} DNA segments")