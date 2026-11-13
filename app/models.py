from enum import Enum
from sqlmodel import Field, SQLModel

class Provincia(str, Enum):
    BENGO = "Bengo"
    BENGUELA = "Benguela"
    BIE = "Bié"
    CABINDA = "Cabinda"
    CUANDO = "Cuando"
    CUBANGO = "Cubango"
    CUANZA_NORTE = "Cuanza Norte"
    CUANZA_SUL = "Cuanza Sul"
    CUNENE = "Cunene"
    HUAMBO = "Huambo"
    HUILA = "Huíla"
    ICOLO_E_BENGO = "Icolo e Bengo"
    LUANDA = "Luanda"
    LUNDA_NORTE = "Lunda Norte"
    LUNDA_SUL = "Lunda Sul"
    MALANJE = "Malanje"
    MOXICO = "Moxico"
    MOXICO_LESTE = "Moxico Leste"
    NAMIBE = "Namibe"
    UIGE = "Uíge"
    ZAIRE = "Zaire"

class FarmerBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    provincia: Provincia
    cultura: str = Field(min_length=2, max_length=50)
    latitude: float = Field(ge=-18, le=-4)
    longitude: float = Field(ge=11, le=24)


class FarmerCreate(FarmerBase):
    """Entrada: valida, sem id."""


class Farmer(FarmerBase, table=True):
    """Tabela. O id é gerado pela BD."""
    id: int | None = Field(default=None, primary_key=True)


class FarmerRead(FarmerBase):
    """Saída: id sempre presente."""
    id: int