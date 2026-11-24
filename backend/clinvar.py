"""
NOT PART OF THE PROJECT YET.
This page was completely written by AI and it's functionality is not yet
integrated nor tested.
Please, do NOT mistake this for a working part of the project.
""""



import httpx
from fastapi import HTTPException

import httpx
from fastapi import HTTPException

def get_diseases_for_variant(gene_name: str, variant_type: str = ""):
    """
    Sucht in ClinVar nach Krankheiten für ein Gen.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # Suchbegriff: Wir suchen nach dem Gen und klinisch relevanten Einträgen
    # (Das ist breiter gefasst und liefert bessere Ergebnisse als nur 'pathogenic')
    search_term = f"{gene_name}[gene] AND (pathogenic[clinical_significance] OR likely pathogenic[clinical_significance])"

    search_params = {
        "db": "clinvar",
        "term": search_term,
        "retmode": "json",
        "retmax": 5 # Wir nehmen die ersten 5 Ergebnisse
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            # 1. ClinVar nach IDs durchsuchen
            search_res = client.get(f"{base_url}/esearch.fcgi", params=search_params)
            search_res.raise_for_status()
            search_data = search_res.json()
            id_list = search_data.get("esearchresult", {}).get("idlist", [])

            if not id_list:
                return [{"message": f"Keine pathogenen Varianten für {gene_name} in ClinVar gefunden."}]

            # 2. Details zu diesen IDs abrufen
            summary_params = {
                "db": "clinvar",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            summary_res = client.get(f"{base_url}/esummary.fcgi", params=summary_params)
            summary_res.raise_for_status()
            summary_data = summary_res.json()

            results = summary_data.get("result", {})
            diseases_found = []

            for uid in id_list:
                variant_info = results.get(uid, {})

                # Der offizielle Name der Variante (z.B. NM_000518.5(HBB):c.20A>T)
                title = variant_info.get("title", "Unbekannte Variante")

                # Die klinische Signifikanz (z.B. Pathogenic)
                clinical_sig = variant_info.get("clinical_significance", {}).get("description", "N/A")

                # KlinVar speichert die Krankheiten oft unter 'germline_classification' oder 'trait_set'
                # Wir versuchen beides abzufangen
                diseases = []

                # Weg 1: trait_set (wird oft bei pathogenen Varianten genutzt)
                traits = variant_info.get("trait_set", [])
                if traits:
                    diseases = [t.get("trait_name") for t in traits if t.get("trait_name")]

                # Weg 2: germline_classification (falls trait_set leer ist)
                if not diseases and "germline_classification" in variant_info:
                    traits = variant_info["germline_classification"].get("trait_set", [])
                    diseases = [t.get("trait_name") for t in traits if t.get("trait_name")]

                diseases_found.append({
                    "clinvar_id": uid,
                    "variant_title": title,
                    "significance": clinical_sig,
                    "diseases": diseases if diseases else ["Keine spezifische Krankheit zugeordnet"]
                })

            return diseases_found

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"ClinVar API Fehler: {e}")
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="ClinVar API hat zu lange gebraucht.")

# Wir testen es mit dem Gen HBB und der Art der Mutation "deletion"
print("Suche Krankheiten für HBB...")
results = get_diseases_for_variant("INFL1", "Point Mutation")

for res in results:
    print(f"- Variante: {res.get('variant_title')}")
    print(f"  Signifikanz: {res.get('significance')}")
    print(f"  Krankheiten: {res.get('diseases')}")
    print("---")
