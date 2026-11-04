import time
import requests, sys
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from DNA_sequence import find_gRNA_Candidates

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENSEMBL_SERVER = "https://rest.ensembl.org"

def get_json_data(url: str):
    for attempt in range(3):
        try:
            with httpx.Client(timeout= 300.0) as client:
                response = client.get(url, headers={"Content-Type": "application/json"})
                response.raise_for_status()
                data = response.json()
                return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (429, 500, 502, 503, 504) and attempt < 2:
                print(f"Ensembl Sequenz-Fehler (Versuch {attempt+1}/3). Warte 2 Sekunden...")
                time.sleep(2)
                continue
            else:
                raise HTTPException(status_code=500, detail=f"Failed to retrieve sequence after 3 attempts: {e}")

def get_gene_id(gene_name: str):
    xref_url = f"{ENSEMBL_SERVER}/xrefs/symbol/homo_sapiens/{gene_name}"

    try:
        id_data = get_json_data(xref_url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            raise HTTPException(status_code=404, detail= f"Gene {gene_name} was not found.")


    #GET THE ENSEMBL SEQUENCE ID FROM THE PARSED JSON XREF
    ensembl_id = None
    for xref in id_data:
        if xref.get("type") == "gene":
            ensembl_id = xref.get("id")
            return ensembl_id

    if not ensembl_id:
        raise HTTPException(status_code=404, detail=f"No gene ID found for '{gene_name}'.")


def get_gene_seq(ensembl_id: str):

    seq_url = f"{ENSEMBL_SERVER}/sequence/id/{ensembl_id}"
    try:
        seq_data = get_json_data(seq_url)
        return (seq_data.get("seq"))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            raise HTTPException(status_code=404, detail= f"Gene {ensembl_id} was not found.")




def get_gene_position(ensembl_id: str):
    position_url = f"{ENSEMBL_SERVER}/lookup/id/{ensembl_id}"
    return get_json_data(position_url)


@app.get("/gRNA")
def get_gRNA_Candidates(gene: str):
    gene_ID = get_gene_id(gene)
    DNA_sequence = get_gene_seq(gene_ID)
    position = get_gene_position(gene_ID)

    print(position)
    candidates = find_gRNA_Candidates(DNA_sequence, position["start"], position["end"], position["seq_region_name"], position["strand"])

    return {
        "gene": position["display_name"],
        "candidates": candidates
    }

#  Testen
if __name__ == "__main__":
    seq = get_gene_seq("HBA1")
    print(seq)
    print(f"Possible gRNAs: {find_gRNA_Candidates(seq)}")
