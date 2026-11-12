from pydantic import BaseModel, Field

# gRNADesign Request Schema

class DesignRequest(BaseModel):
    gene: str = Field(..., description="The gene symbol (e.g., HBB, BRCA1)", example="HBB")


# 2. The Model for the Sequence Comparator (POST /compare)
class SequenceInput(BaseModel):
    wildtype: str = Field(..., description="The wildtype FASTA sequence or raw DNA string", example="GACTCAGAGAGAACCCACCATGG")
    edited: str = Field(..., description="The edited FASTA sequence or raw DNA string", example="GACTCAGAGAGAACCCACCATCG")
