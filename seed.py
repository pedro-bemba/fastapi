import random

from sqlmodel import Session, func, select

from app.db import create_db_and_tables, engine
from app.models import Farmer, FarmerCreate, Provincia

TOTAL = 50

PRIMEIROS_NOMES = [
    "Manuel", "Ana", "Joaquim", "Maria", "António", "Isabel", "Domingos",
    "Teresa", "Pedro", "Luísa", "Francisco", "Esperança", "José", "Rosa",
    "Fernando", "Catarina", "Augusto", "Madalena", "Armando", "Celeste",
]
APELIDOS = [
    "Bemba", "Cambinda", "Tchipa", "Kiala", "Mendes", "Sapalo", "Tchissola",
    "Baptista", "Nzuzi", "Katumbela", "Chilombo", "Ndala", "Quissanga",
    "Capita", "Muhongo", "Sambo", "Lukamba", "Fortunato", "Cassule", "Dala",
]
CULTURAS = ["milho", "mandioca", "café", "feijão"]

# Caixas aproximadas (lat_min, lat_max, lon_min, lon_max) por província.
# Dentro dos limites do modelo: lat -18 a -4, lon 11 a 24.
CAIXAS = {
    Provincia.CABINDA: (-5.8, -4.5, 12.0, 13.0),
    Provincia.ZAIRE: (-7.5, -6.0, 12.5, 14.5),
    Provincia.UIGE: (-8.0, -6.5, 14.0, 16.0),
    Provincia.LUANDA: (-9.1, -8.7, 13.0, 13.5),
    Provincia.ICOLO_E_BENGO: (-9.4, -8.9, 13.2, 14.0),
    Provincia.BENGO: (-9.5, -8.0, 13.2, 14.5),
    Provincia.CUANZA_NORTE: (-9.5, -8.5, 14.5, 15.5),
    Provincia.MALANJE: (-10.0, -8.5, 15.5, 17.5),
    Provincia.LUNDA_NORTE: (-9.0, -7.0, 19.0, 21.5),
    Provincia.LUNDA_SUL: (-10.5, -9.0, 19.5, 21.5),
    Provincia.CUANZA_SUL: (-11.5, -10.0, 13.5, 15.0),
    Provincia.BENGUELA: (-13.5, -12.0, 13.2, 14.5),
    Provincia.HUAMBO: (-13.0, -12.0, 15.2, 16.0),
    Provincia.BIE: (-13.0, -12.0, 16.2, 17.5),
    Provincia.MOXICO: (-13.5, -11.5, 19.0, 21.0),
    Provincia.MOXICO_LESTE: (-13.5, -11.5, 21.0, 22.5),
    Provincia.NAMIBE: (-16.5, -15.0, 11.8, 13.0),
    Provincia.HUILA: (-15.5, -14.0, 13.0, 14.5),
    Provincia.CUNENE: (-17.5, -16.0, 14.5, 16.0),
    Provincia.CUBANGO: (-17.0, -15.5, 16.5, 18.0),
    Provincia.CUANDO: (-17.5, -15.5, 18.0, 20.5),
}


def gerar(rng: random.Random) -> FarmerCreate:
    provincia = rng.choice(list(CAIXAS))
    lat_min, lat_max, lon_min, lon_max = CAIXAS[provincia]
    return FarmerCreate(
        nome=f"{rng.choice(PRIMEIROS_NOMES)} {rng.choice(APELIDOS)}",
        provincia=provincia,
        cultura=rng.choice(CULTURAS),
        latitude=round(rng.uniform(lat_min, lat_max), 5),
        longitude=round(rng.uniform(lon_min, lon_max), 5),
    )


def main() -> None:
    create_db_and_tables()
    rng = random.Random(42)

    with Session(engine) as session:
        existentes = session.exec(select(func.count()).select_from(Farmer)).one()
        em_falta = TOTAL - existentes

        if em_falta <= 0:
            print(f"Já existem {existentes} agricultores. Nada a fazer.")
            return

        for _ in range(em_falta):
            session.add(Farmer.model_validate(gerar(rng)))
        session.commit()
        print(f"Inseridos {em_falta} agricultores (total: {TOTAL}).")


if __name__ == "__main__":
    main()