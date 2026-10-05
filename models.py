from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Pais(Base):
    __tablename__ = "pais"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True)
    continente: Mapped[str] = mapped_column(String(40))
    idioma: Mapped[str] = mapped_column(String(40))
    populacao: Mapped[int]

    # 1 país -> N cidades
    cidades: Mapped[list["Cidade"]] = relationship(
        back_populates="pais", cascade="all, delete-orphan"
    )

    def __str__(self):
        return (f"[{self.id}] {self.nome} | {self.continente} | "
                f"{self.idioma} | {self.populacao:,} hab.")


class Cidade(Base):
    __tablename__ = "cidade"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80))
    populacao: Mapped[int]
    area_km2: Mapped[float]
    capital: Mapped[bool] = mapped_column(default=False)
    pais_id: Mapped[int] = mapped_column(ForeignKey("pais.id"))

    pais: Mapped["Pais"] = relationship(back_populates="cidades")

    def __str__(self):
        cap = " (capital)" if self.capital else ""
        return (f"[{self.id}] {self.nome}{cap} | {self.populacao:,} hab. | "
                f"{self.area_km2} km² | país: {self.pais.nome}")