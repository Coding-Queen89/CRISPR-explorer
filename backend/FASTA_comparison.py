from Bio import Align

def clean_FASTA(FASTA_seq: str) -> str:
    seq_lines = FASTA_seq.strip().split('\n')
    if seq_lines and seq_lines[0].startswith('>'):
        seq_lines = seq_lines[1:]
    return "".join("".join(seq_lines).split()).upper()

def variant_search(target: str, query: str ) -> list:
    variants = []
    i = 0

    while i < len(target) and i < len(query):
        if target[i] != query[i]:
            if target[i] == '-' and query[i] != '-':
                ins_str = ""
                while i < len(target) and target[i] == '-':
                    ins_str += query[i]
                    i += 1
                variants.append({
                    "type": "Insertion",
                    # "position": i,
                    "inserted_seq": ins_str
                })
            elif query[i] == '-' and target[i] != '-':
                del_str = ""
                while i < len(target) and query[i] == '-':
                    del_str += target[i]
                    i += 1
                variants.append({
                    "type": "Deletion",
                    # "position": i,
                    "deleted_seq": del_str
                })
            else:
                variants.append({
                    "type": "Substitution",
                    "wt_base": target[i],
                    "mut_base": query[i]
                })
                i += 1
        else:
            i += 1

    return variants

def compare_sequences(FASTA_seq1: str, FASTA_seq2: str) -> dict:
    FASTA_seq1 = clean_FASTA(FASTA_seq1)
    FASTA_seq2 = clean_FASTA(FASTA_seq2)


    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5
    aligner.match_score = 1
    aligner.mismatch_score = -1

    alignments = aligner.align(FASTA_seq1, FASTA_seq2)
    best_alignment = alignments[0]

    target_str = best_alignment[0]
    query_str = best_alignment[1]
    variants = variant_search(target_str, query_str)

    print(best_alignment.format())
    print(f"Global Alignment Score: {best_alignment.score}")
    return {
        "best_alignment": best_alignment.format(),
        "variant": variants,
        "score": best_alignment.score
    }
