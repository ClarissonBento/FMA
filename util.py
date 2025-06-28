import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo):
    largura = 42
    print("╔" + "═" * largura + "╗")
    print("║" + " F A B R I C A   D E   P O Ç Õ E S ".center(largura) + "║")
    print("╚" + "═" * largura + "╝")
    print(titulo.center(largura + 2))
    print()

def exibir_estado(estado):
    print(f"Estado atual: [ {estado} ]\n")

def exibir_ingrediente(ing):
    print("╭" + "─" * (len(ing) + 6) + "╮")
    print(f"│ adc:{ing} │")
    print("╰" + "─" * (len(ing) + 6) + "╯")
    time.sleep(0.6)

def exibir_barra(ingr_list):
    barra = "Mistura: [ " + " ═ ".join(ingr_list) + " ]"
    print(barra + "\n")
    time.sleep(0.6)

def exibir_pilha(pilha):
    print("Pilha da Receita:")
    if not pilha:
        print("[ vazia ]\n")
    else:
        for elem in reversed(pilha):
            print(f"| {elem} |")
        print("-----\n")

def efeito_borbulha(): time.sleep(0.6)
def efeito_agitar(): time.sleep(0.6)
def efeito_transformacao(): time.sleep(0.6)
def efeito_vapor():
    time.sleep(0.8)
    print("~ vapores místicos... ~\n")

def efeito_final():
    for simbolo in ["⧫", "◆", "◇", "◇", "◆", "⧫"]:
        print(simbolo, end=" ", flush=True)
        time.sleep(0.5)
    print("\n✨ Poção forjada! ✨\n")

def ler_header(caminho):
    with open(caminho, encoding='utf-8') as f:
        for l in f:
            if l.strip().startswith('NOME:'):
                return l.split(':', 1)[1].strip()
    return os.path.basename(caminho)
