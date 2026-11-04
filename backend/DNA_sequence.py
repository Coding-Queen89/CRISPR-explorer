"""
Taking in the gene's DNA sequence, this program will find the possible guide RNAs for SpCas9.
The Pam site will be the NGG on the forward and backward strand.
"""

def find_gRNA_Candidates(seq: str, gene_start: int, gene_end: int, region: int, strand: int) -> list[dict]:
    candidates = []
    n = len(seq)

    # FINDING THE gRNA ON THE FORWARD STRAND. EXCEPT IF THE GIVEN GENE WAS ON THE BACKWARD STRAND
    # IN THAT CASE THE FOLLOWING gRNAS WILL BE ON THE BACKWARD STRAND.

    for i in range(21, n-1):
        if seq[i] == 'G' and seq[i+1] == 'G':
            pam = seq[i-1:i+2]
            gRNA = seq[i-21:i-1]

            # Position of gRNA according to the human genome
            relative_position = i - 20
            if strand == 1:
                genomic_position = f"chr{region}:{gene_start + (relative_position)-1}"
            else:
                genomic_position =  f"chr{region}:{gene_end - (relative_position+20) -1}"

            # CHECKING FOR RELIABILITY OF gRNA
            gc_count = gRNA.count('G') + gRNA.count('C') # How many Guanine and Cytosine found in the gRNA
            gc_percentage = round(((gc_count/20)*100),1) # 3 H2O binding sites between G and C making it more stable
            has_poly_T = "TTTT" in gRNA  # 4 or more T trigger the RNA Polymerase to stop

            status = "fail"
            if gc_percentage >= 40 and gc_percentage <= 60 and not has_poly_T:
                status = "pass"

            candidates.append({
                "sequence": gRNA,
                "pam": pam,
                "strand": "+" if strand == 1 else "-",
                "position": genomic_position,
                "gc_content": gc_percentage,
                "poly_t": has_poly_T,
                "explanation": ("More than 4 Thymine bases found in gRNA sequence, leading to an early cease of polymerasation from RNA Polymerase " if has_poly_T else "GC% not in range of 40 to 60, leading to either instablity or clumping of DNA.") if status == "fail" else None,
                "status": status
            })

    """
    INSTEAD OF COMPLEMENTING THE ENTIRE STRAND, WE CAN LOOK FOR CCN ON THE FORWARD STRAND
    ALL 20 BASES AFTER THE CCN ON THE FOROWARD STRAND CORRESPOND TO THE 20 BASES BEFORE
    THE NGG ON THE REVERSE STRAND
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    def reverse_complement(s):
        return "".join(complement.get(base, base) for base in reversed(s))

    # FINDING THE gRNA ON THE REVERSE STRAND. EXCEPT IF THE GIVEN GENE WAS ON THE BACKWARD STRAND
    # IN THAT CASE THE FOLLOWING gRNAS WILL BE ON THE FORWARD STRAND.

    for j in range(1, n-21):
        if seq[j] == 'C' and seq[j-1] == 'C':
            pam = reverse_complement(seq[j-1:j+2])
            gRNA = reverse_complement(seq[j+2:j+22])

            # Position of gRNA according to the human genome
            relative_position = j + 3
            if strand == 1:
                genomic_position =  f"chr{region}:{gene_start + (relative_position) - 4}"
            else:
                genomic_position =  f"chr{region}:{gene_end - (relative_position+20)+2}"

            # CHECKING FOR RELIABILITY OF gRNA
            gc_count = gRNA.count('G') + gRNA.count('C') # How many Guanine and Cytosine found in the gRNA
            gc_percentage = round(((gc_count/20)*100),1) # 3 H2O binding sites between G and C making it more stable
            has_poly_T = "TTTT" in gRNA  # 4 or more T trigger the RNA Polymerase to stop

            status = "fail"
            if gc_percentage >= 40 and gc_percentage <= 60 and not has_poly_T:
                status = "pass"

            candidates.append({
                "sequence": gRNA,
                "pam": pam,
                "strand": "-" if strand == 1 else "+",
                "position": genomic_position,
                "gc_content": gc_percentage,
                "poly_t": has_poly_T,
                "explanation": ("More than 4 Thymine bases found in gRNA sequence, leading to an early cease of polymerasation from RNA Polymerase " if has_poly_T else "GC% not in range of 40 to 60, leading to either instablity or clumping of DNA.") if status == "fail" else None,
                "status": status
            })

    candidates.sort(key = lambda x : x["position"])
    return candidates
