from util import *
from maquinas.automato_finito import AutomatoAFD, ler_arquivo_afd
from maquinas.automato_pilha import AutomatoAPD, ler_arquivo_apd, ler_mensagens_pilha
from maquinas.mealy import AutomatoMealy, ler_arquivo_mealy
from maquinas.moore import AutomatoMoore, ler_arquivo_moore
from maquinas.turing import MaquinaTuring, ler_arquivo_turing, MAPA_RUNAS


def simular(tipo, arquivo):
    try:
        nome = ler_header(arquivo)
    except Exception as e:
        limpar_tela()
        print(f"Erro ao ler nome da poção: {e}")
        return

    limpar_tela()
    exibir_cabecalho(f"{tipo} - Poção: {nome}")

    try:
        if tipo == 'AFD':
            ini, fins, trans = ler_arquivo_afd(arquivo)
            auto = AutomatoAFD(ini, fins, trans)
        elif tipo == 'APD':
            ini, fins, trans = ler_arquivo_apd(arquivo)
            mensagens = ler_mensagens_pilha(arquivo)
            auto = AutomatoAPD(ini, fins, trans, mensagens)
        elif tipo == 'MOORE':
            ini, trans, saidas = ler_arquivo_moore(arquivo)
            auto = AutomatoMoore(ini, trans, saidas)
        elif tipo == 'MEALY':
            ini, trans = ler_arquivo_mealy(arquivo)
            auto = AutomatoMealy(ini, trans)
        else:
            raise ValueError(f"Tipo desconhecido: {tipo}")
    except Exception as e:
        print(f"Erro ao ler autômato do arquivo: {e}")
        return

    ingredientes = []
    sucesso = True

    while True:
        s = input('Digite símbolo (ou "fim"): ').strip()
        if s.lower() == 'fim':
            break

        ingredientes.append(s)
        limpar_tela()
        exibir_cabecalho(f"{tipo} - Poção: {nome}")
        exibir_ingrediente(s)
        exibir_barra(ingredientes)
        print(f"Estado atual: {auto.estado_atual}\n")

        try:
            ok = auto.processar(s)
        except Exception as e:
            print(f"Erro na transição: {e}")
            sucesso = False
            break

        if not ok or getattr(auto, 'estado_atual', '') == 'erro':
            print("\n💥 Erro na simulação.")
            sucesso = False
            break

    limpar_tela()
    exibir_cabecalho(f"{tipo} - Poção: {nome}")

    if sucesso:
        if tipo in ['AFD', 'APD']:
            if auto.estado_atual in auto.estados_finais:
                efeito_vapor()
                efeito_final()
                print(f"\n✨ Poção {nome} criada com sucesso! ✨")
            else:
                print("\n❌ A poção falhou! Estado final inválido.\n")
            if tipo == 'APD':
                print("⚠ Pilha final:")
                exibir_pilha(auto.pilha)
                simbolos_verificados = set()
                for simbolo in auto.pilha:
                    if simbolo in auto.mensagens and simbolo not in simbolos_verificados:
                        print(f"⚠ {auto.mensagens[simbolo]}")
                        simbolos_verificados.add(simbolo)

        elif tipo == 'MOORE':
            efeito_vapor()
            efeito_final()
            print(f"\n✨ Poção {nome} criada com sucesso! ✨")

        elif tipo == 'MEALY':
            efeito_vapor()
            efeito_final()
            print(f"\n✨ Poção {nome} criada com sucesso! ✨")

if __name__ == '__main__':
    limpar_tela()
    print('[1] AFD  [2] APD  [3] MOORE  [4] MEALY')
    op = input('Opção: ').strip()
    tipos = {'1': 'AFD', '2': 'APD', '3': 'MOORE', '4': 'MEALY'}
    escolha = tipos.get(op)
    if not escolha:
        print('Opção inválida.')
    else:
        caminho = input('Arquivo (.txt): ').strip()
        simular(escolha, caminho)