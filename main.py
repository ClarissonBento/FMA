from util import *
from automato_finito import AutomatoAFD, ler_arquivo_afd
from automato_pilha import AutomatoAPD, ler_arquivo_apd, ler_mensagens_pilha
from mealy import AutomatoMealy, ler_arquivo_mealy
from moore import AutomatoMoore, ler_arquivo_moore

def simular(tipo, arquivo):
    nome = ler_header(arquivo)
    limpar_tela()
    exibir_cabecalho(f"{tipo} - Poção: {nome}")

    if tipo == 'AFD':
        ini, fins, trans = ler_arquivo_afd(arquivo)
        auto = AutomatoAFD(ini, fins, trans)
    elif tipo == 'APD':
        ini, fins, trans = ler_arquivo_apd(arquivo)
        mensagens = ler_mensagens_pilha(arquivo)
        auto = AutomatoAPD(ini, fins, trans, mensagens)
    elif tipo == 'MOORE':
        ini, trans, saida = ler_arquivo_moore(arquivo)
        auto = AutomatoMoore(ini, trans, saida)
    elif tipo == 'MEALY':
        ini, trans = ler_arquivo_mealy(arquivo)
        auto = AutomatoMealy(ini, trans)

    exibir_estado(auto.estado_atual)

    while True:
        s = input('Digite símbolo (ou "fim"): ').strip().lower()
        if s == 'fim':
            break

        limpar_tela()
        exibir_cabecalho(f"{tipo} - Poção: {nome}")
        exibir_ingrediente(s)

        ok = auto.processar(s)

        if tipo == 'APD':
            exibir_pilha(auto.pilha)

        exibir_estado(auto.estado_atual)

        if not ok or auto.estado_atual == 'erro':
            print("💥 Erro na simulação.")
            return

    if tipo in ['AFD', 'APD']:
        if auto.estado_atual in auto.estados_finais:
            efeito_vapor()
            efeito_final()
        else:
            print("❌ A poção falhou! O processo foi interrompido em um estado não final.\n")

        if tipo == 'APD':
            print("⚠ Pilha final:")
            exibir_pilha(auto.pilha)
            simbolos_verificados = set()
            
            for simbolo in auto.pilha:
                if simbolo in auto.mensagens and simbolo not in simbolos_verificados:
                    print(f"⚠ {auto.mensagens[simbolo]}")
                    simbolos_verificados.add(simbolo)


    if tipo == 'MOORE':
        print(f"Saída final: {auto.saida_atual()}")

    if tipo == 'MEALY':
        print("Simulação Mealy concluída.")

if __name__ == '__main__':
    limpar_tela()
    print('[1] AFD  [2] APD  [3] MOORE  [4] MEALY')
    op = input('Opção: ').strip()
    tipos = {'1': 'AFD', '2': 'APD', '3': 'MOORE', '4': 'MEALY'}
    simular(tipos.get(op, 'AFD'), input('Arquivo (.txt): ').strip())
