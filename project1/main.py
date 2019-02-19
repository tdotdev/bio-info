from random import randint

class DNA:
    def __init__(self, five_to_three, three_to_five):
        self.five = five_to_three
        self.three = three_to_five

BASE_MAP = {
    'a': 't',
    't': 'a',
    'g': 'c',
    'c': 'g'
}

def complement(strand):
    return ''.join([BASE_MAP[base] for base in strand])

# We're going to target the first twenty bases in the third line of this strand
# Target: catcgactgcgcccaccagcagaagctggtcttctccctggtcaagcagggctatggtgg\
#         ctactaacacgggtggaagatagcttttgcaatactcggtttgcatgtgctgaaagtcat
# Primer for 5' = catcgactgcgcccaccagc
# Primer for 3' = complement(primer for 5') = gtagctgacgcgggtggtcg
STARTER_FIVE = \
"gcattagtctaatgagatgtttgcagctggagcgcagggctgctggagactaactgtgag\
catcgactgcgcccaccagcagaagctggtcttctccctggtcaagcagggctatggtgg\
ctactaacacgggtggaagatagcttttgcaatactcggtttgcatgtgctgaaagtcat\
agctgtagcacctcttctgcctgtgagcgatttgtcacctcattctgtaagactggcacc\
agcagaaatgcagtctcaaaggatcccggggagaaagcgaggccgaccctcacttcactc"

STARTER_THREE = complement(STARTER_FIVE)

PRIMER_LENGTH = 20
REPLICATION_ZONE = 0
EXTENSION_LENGTH = 200
CYCLE_LIMIT = 5

# Primer specifically created to target the strand mentioned above
PRIMER1 = complement(STARTER_FIVE[REPLICATION_ZONE+EXTENSION_LENGTH-PRIMER_LENGTH:REPLICATION_ZONE+EXTENSION_LENGTH])
PRIMER2 = complement(STARTER_THREE[REPLICATION_ZONE:REPLICATION_ZONE+PRIMER_LENGTH])
print(STARTER_FIVE[REPLICATION_ZONE+EXTENSION_LENGTH-PRIMER_LENGTH:REPLICATION_ZONE+EXTENSION_LENGTH])
print(PRIMER1)

def pcr(dna_strand):
    # Denaturation - split DNA into single template strands
    five = dna_strand.five
    three = dna_strand.three

    copies = []
    
    # Annealing - introduction of primers
    # Need to check if the primer matches what the complement is for the target start area
    if primer_can_bind(five, PRIMER1):
        # Extend five
        five_complement = ""
        five_start = REPLICATION_ZONE
        for i in range(EXTENSION_LENGTH+randint(-50,50)):
            if i+five_start < len(five):
                five_complement += BASE_MAP[five[i + five_start]]

        copies.append(DNA(five[::-1], five_complement[::-1]))

    if primer_can_bind(three, PRIMER2):
        # Extend three
        three_complement = ""
        three_start = REPLICATION_ZONE
        for i in range(EXTENSION_LENGTH+randint(-50,50)):
            if i+three_start < len(three):
                three_complement += BASE_MAP[three[i + three_start]]

        copies.append(DNA(three_complement, three))

    return copies

def primer_can_bind(base, primer):
    print(primer)
    print(base)
    for i in range(PRIMER_LENGTH):
        if primer[i] != BASE_MAP[base[REPLICATION_ZONE+i]]:
            return False
    return True

# Our starting DNA
starter = DNA(STARTER_FIVE, STARTER_THREE)

# A queue for DNA strands to be PCR'd
strand_buffer = [starter]

for i in range(CYCLE_LIMIT):
    # Iterate through strands that were in the buffer before this loop executes
    for j in range(len(strand_buffer)):
        # Aquire two new DNA strands through PCR of one strand
        new_strands = pcr(strand_buffer[0])
        
        # Remove current strand from buffer (this strand would no longer exist after real PCR)
        strand_buffer.pop(0)

        # Add our new strands to the buffer to be processed in the next loop of CYCLE_LIMIT
        for strands in strand_buffer:
            strand_buffer.append(strands)

print(f"Number of copies = {len(strand_buffer)} DNA segments")
