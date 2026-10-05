from sqlalchemy import select

import db
from models import Cidade, Pais


# ---------- entrada de dados ----------
def ler_texto(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("Valor obrigatório.")


def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro.")


def ler_float(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Digite um número.")


def ler_bool(msg):
    return input(msg + " (s/n): ").strip().lower() == "s"


# ---------- conexão ----------
def conectar():
    print("\n1 - SQLite (arquivo local)\n2 - MySQL (.env)")
    opcao = input("Escolha o banco: ").strip()
    tipo = {"1": "sqlite", "2": "mysql"}.get(opcao)
    if not tipo:
        print("Opção inválida.")
        return None
    try:
        engine = db.criar_engine(tipo)
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None
    print(f"Conectado ao {tipo.upper()}.")
    return tipo, engine, db.abrir_sessao(engine)


# ---------- operações ----------
def inserir_pais(s):
    p = Pais(
        nome=ler_texto("Nome: "),
        continente=ler_texto("Continente: "),
        idioma=ler_texto("Idioma: "),
        populacao=ler_int("População: "),
    )
    s.add(p)
    s.commit()
    print("País inserido.")


def inserir_cidade(s):
    paises = s.scalars(select(Pais).order_by(Pais.nome)).all()
    if not paises:
        print("Cadastre um país primeiro.")
        return
    for p in paises:
        print(p)
    pais_id = ler_int("ID do país da cidade: ")
    pais = s.get(Pais, pais_id)
    if not pais:
        print("País não encontrado.")
        return
    c = Cidade(
        nome=ler_texto("Nome: "),
        populacao=ler_int("População: "),
        area_km2=ler_float("Área (km²): "),
        capital=ler_bool("É capital?"),
        pais=pais,
    )
    s.add(c)
    s.commit()
    print("Cidade inserida.")


def listar_paises(s):
    paises = s.scalars(select(Pais).order_by(Pais.nome)).all()
    if not paises:
        print("Nenhum país cadastrado.")
    for p in paises:
        print(p)
        for c in p.cidades:
            print(f"    - {c.nome} ({c.populacao:,} hab.)")


def listar_cidades(s):
    cidades = s.scalars(select(Cidade).order_by(Cidade.nome)).all()
    if not cidades:
        print("Nenhuma cidade cadastrada.")
    for c in cidades:
        print(c)


def excluir_pais(s):
    listar_paises(s)
    p = s.get(Pais, ler_int("ID do país a excluir: "))
    if not p:
        print("País não encontrado.")
        return
    n = len(p.cidades)
    if n and not ler_bool(f"Isso também exclui {n} cidade(s). Continuar?"):
        return
    s.delete(p)
    s.commit()
    print("País excluído.")


def excluir_cidade(s):
    listar_cidades(s)
    c = s.get(Cidade, ler_int("ID da cidade a excluir: "))
    if not c:
        print("Cidade não encontrada.")
        return
    s.delete(c)
    s.commit()
    print("Cidade excluída.")


MENU = """
===== {tipo} =====
1 - Inserir país
2 - Inserir cidade
3 - Listar países (com cidades)
4 - Listar cidades
5 - Excluir país
6 - Excluir cidade
7 - Trocar de banco de dados
0 - Sair
"""


def main():
    conexao = None
    while conexao is None:
        conexao = conectar()
    tipo, engine, sessao = conexao

    acoes = {
        "1": inserir_pais, "2": inserir_cidade,
        "3": listar_paises, "4": listar_cidades,
        "5": excluir_pais, "6": excluir_cidade,
    }

    while True:
        print(MENU.format(tipo=tipo.upper()))
        op = input("Opção: ").strip()
        if op == "0":
            break
        if op == "7":
            nova = conectar()
            if nova:
                sessao.close()
                engine.dispose()
                tipo, engine, sessao = nova
        elif op in acoes:
            try:
                acoes[op](sessao)
            except Exception as e:
                sessao.rollback()
                print(f"Erro: {e}")
        else:
            print("Opção inválida.")

    sessao.close()
    engine.dispose()
    print("Até mais!")


if __name__ == "__main__":
    main()