from util import *
from maquinas.automato_finito import AutomatoAFD, ler_arquivo_afd
from maquinas.automato_pilha import AutomatoAPD, ler_arquivo_apd, ler_mensagens_pilha
from maquinas.mealy import AutomatoMealy, ler_arquivo_mealy
from maquinas.moore import AutomatoMoore, ler_arquivo_moore
from maquinas.turing import MaquinaTuring, ler_arquivo_turing, MAPA_RUNAS


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
    elif tipo == 'MT':
        ini, fins, trans = ler_arquivo_turing(arquivo)
        auto = MaquinaTuring(ini, fins, trans)

        print("Digite a sequência de runas separadas por espaço (ex: aard igni quen):")
        entrada_runas = input("> ").strip().lower().split()

        palavra = ""
        for runa in entrada_runas:
            if runa not in MAPA_RUNAS:
                print(f"⚠ Runa inválida: {runa}")
                return
            palavra += MAPA_RUNAS[runa]

        auto.inicializar_fita(palavra)

        limpar_tela()
        exibir_cabecalho(f"{tipo} - Poção: {nome}")
        print(f"Fita inicial (traduzida): {palavra}")

        aceita = auto.processar()

        if aceita:
            efeito_vapor()
            print('✨✨✨✨✨✨✨✨✨✨✨✨✨')
        else:
            print("❌ A poção falhou! A Máquina parou em estado não final ou sem transições.")
        
        return  # MT não usa o loop de entrada símbolo a símbolo

    exibir_estado_atual(auto.estado_atual)

    saida_total = ""

    while True:
        s = input('Digite símbolo(s) (ou "fim"): ').strip().lower()
        if s == 'fim':
            break

        tokens = s.split() 

        for simbolo in tokens:
            limpar_tela()
            exibir_cabecalho(f"{tipo} - Poção: {nome}")
            exibir_ingrediente(simbolo)

            ok = auto.processar(simbolo)

            if tipo == 'APD':
                exibir_pilha(auto.pilha)

            exibir_estado_atual(auto.estado_atual)

            if not ok or auto.estado_atual == 'erro':
                print("💥 Erro na simulação.")
                return

            saida_atual = auto.saida_atual()
            if saida_atual != 'λ': 
                saida_total += saida_atual

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
        print(f"Saída final acumulada: {saida_total}")

    if tipo == 'MEALY':
        print("Simulação Mealy concluída.")


if __name__ == '__main__':
    limpar_tela()
    print('[1] AFD  [2] APD  [3] MOORE  [4] MEALY  [5] MT')
    op = input('Opção: ').strip()
    tipos = {'1': 'AFD', '2': 'APD', '3': 'MOORE', '4': 'MEALY', '5': 'MT'}
    
    arquivo = input('Arquivo (.txt): ').strip()
    caminho_completo = f"receitas/{arquivo}.txt"
    
    simular(tipos.get(op, 'AFD'), caminho_completo)
