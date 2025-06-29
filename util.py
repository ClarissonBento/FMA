import os, time
import re

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo):
    largura = 42
    print("╔" + "═" * largura + "╗")
    print("║" + " F A B R I C A   D E   P O Ç Õ E S ".center(largura) + "║")
    print("╚" + "═" * largura + "╝")
    print(titulo.center(largura + 2) + "\n")

def exibir_ingrediente(ing):
    print("╭" + "─" * (len(ing) + 6) + "╮")
    print(f"│ adc:{ing} │")
    print("╰" + "─" * (len(ing) + 6) + "╯")
    efeito_borbulha()
    efeito_agitar()
    efeito_transformacao()

def exibir_barra(ingr):
    print("Mistura: [ " + " ═ ".join(ingr) + " ]\n")
    time.sleep(0.6)

def exibir_pilha(p):
    print("Pilha da Receita:")
    if not p:
        print("[ vazia ]\n")
    else:
        for e in reversed(p):
            print(f"| {e} |")
        print("-----\n")

def exibir_estado_atual(estado):
    print(f"Estado atual: [ {estado} ]\n")

def ler_header(caminho):
    """
    Lê o nome da poção:
    1) Procura no arquivo por linha 'nome: Valor'
    2) Se não achar, obtém do nome do arquivo:
       - remove prefixos (afd, apd, mealy, moore)
       - converte underscores e hífens em espaços
    """
    nome = ''
    pattern = re.compile(r'^\s*nome\s*[:=]\s*(.+)$', re.IGNORECASE)
    with open(caminho, encoding='utf-8-sig') as f:
        for raw in f:
            m = pattern.match(raw.strip())
            if m:
                nome = m.group(1).strip()
                break

    if not nome:
        base = os.path.splitext(os.path.basename(caminho))[0]
        base = re.sub(r'^(afd|apd|mealy|moore)[ _\-]+', '', base, flags=re.IGNORECASE)
        nome = re.sub(r'[ _\-]+', ' ', base).strip()

    return nome

def efeito_borbulha():
    print("✨ ~ borbulhas cintilantes sobem... ~ ✨")
    time.sleep(0.6)

def efeito_agitar():
    print("🔮 ~ agitando o caldeirão com leveza... ~ 🔮")
    time.sleep(0.6)

def efeito_transformacao():
    print("🌙 ~ reações etéreas acontecem... ~ 🌙")
    time.sleep(0.6)

def efeito_vapor():
    print("💨 ~ vapor ascende em espirais místicas... ~ 💨")
    time.sleep(0.6)

def efeito_final():
    print("🌟 ~ o elixir brilha com energia suprema... ~ 🌟")
    time.sleep(0.6)