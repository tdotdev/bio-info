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

PRIMER1 = "catcgactgcgcccaccagc"
PRIMER2 = complement(PRIMER1)

PRIMER_LENGTH = 20
TAQ_SIZE = 50
CYCLE_LIMIT = 20

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
    for i in range(TAQ_SIZE):
        five_complement += BASE_MAP[five[i + five_start]]
        three_complement += BASE_MAP[three[i + three_start]]

    new_strand1 = DNA(five, five_complement)
    new_strand2 = DNA(three, three_complement)

    return (new_strand1, new_strand2)

starter = DNA(STARTER_FIVE, STARTER_THREE)
strand_buffer = [starter]

for i in range(CYCLE_LIMIT):
    for j in range(len(strand_buffer)):
        new_strands = pcr(strand_buffer[0])
        strand_buffer.pop(0)
        strand_buffer.append(new_strands[0])
        strand_buffer.append(new_strands[1])

print(f"Number of copies = {len(strand_buffer)} DNA segments")