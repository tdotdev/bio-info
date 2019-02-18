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

# Primer specifically created to target the strand mentioned above
PRIMER1 = "catcgactgcgcccaccagc"
PRIMER2 = complement(PRIMER1)

PRIMER_LENGTH = 20
EXTENSION_LEN = 200
CYCLE_LIMIT = 15

def pcr(dna_strand):
    # Denaturation - split DNA into single template strands
    five = dna_strand.five
    three = dna_strand.three
    
    # Annealing - introduction of primers
    try:
        five_start = five.index(PRIMER1)
    except:
        five_start = five.index(PRIMER2)
    try:
        three_start = three.index(PRIMER2)
    except:
        three_start = three.index(PRIMER1)

    # Elongation - extend primer with bases complementary to template strand
    five_complement = ""
    three_complement = ""
    for i in range(EXTENSION_LEN+randint(-50,50)):
        five_complement += BASE_MAP[five[i + five_start]]
        three_complement += BASE_MAP[three[i + three_start]]

    new_strand1 = DNA(five, five_complement)
    new_strand2 = DNA(three, three_complement)

    return (new_strand1, new_strand2)

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
        strand_buffer.append(new_strands[0])
        strand_buffer.append(new_strands[1])

print(f"Number of copies = {len(strand_buffer)} DNA segments")
