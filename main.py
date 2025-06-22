# Tema: The Witcher 3 - FTC
import time
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_cabecalho(titulo):
    largura = 42
    print("╔" + "═" * largura + "╗")
    print("║" + " F A B R I C A   D E   P O Ç Õ E S ".center(largura) + "║")
    print("╚" + "═" * largura + "╝")
    print(titulo.center(largura+2))
    print()

def exibir_estado(estado):
    print(f"Estado atual: [ {estado} ]\n")


def exibir_ingrediente(ing):
    print("╭" + "─" * (len(ing) + 6) + "╮")
    print(f"│ adc:{ing} │")
    print("╰" + "─" * (len(ing) + 6) + "╯")
    efeito_borbulha()
    efeito_agitar()
    efeito_transformacao()


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


def efeito_borbulha():
    print("borbulhas cintilantes sobem...")
    time.sleep(0.6)


def efeito_agitar():
    print("agitando o caldeirão com leveza...")
    time.sleep(0.6)


def efeito_transformacao():
    print("reações etéreas acontecem...")
    time.sleep(0.6)


def efeito_vapor():
    print("🔮 nuvens místicas emanam vapores... 🔮")
    time.sleep(0.8)
    print("🔮 um aroma arcano preenche o ar! 🔮\n")


def efeito_final():
    print("\nFinalizando a criação...") 
    for simbolo in ["⧫", "◆", "◇", "◇", "◆", "⧫"]:
        print(simbolo, end=" ", flush=True)
        time.sleep(0.5)
    print("\n✨✨✨ Poção forjada com maestria! ✨✨✨\n")

class AutomatoAFD:
    def __init__(self, estados, inicial, finais, transicoes):
        self.estado_atual = inicial
        self.estados_finais = set(finais)
        self.transicoes = transicoes

    def processar(self, simbolo):
        chave = (self.estado_atual, simbolo)
        if chave in self.transicoes:
            self.estado_atual = self.transicoes[chave]
            return True
        self.estado_atual = 'erro'
        return False

class AutomatoPilha:
    def __init__(self, estados, inicial, finais, transicoes):
        self.estado_atual = inicial
        self.estados_finais = set(finais)
        self.transicoes = transicoes
        self.pilha = []

    def processar(self, simbolo):
        topo = self.pilha[-1] if self.pilha else 'λ'
        chave = (self.estado_atual, simbolo, topo)
        if chave in self.transicoes:
            prox, acao = self.transicoes[chave]
            self.estado_atual = prox
            if acao.startswith('push:'):
                _, val = acao.split(':')
                self.pilha.append(val)
            elif acao == 'pop' and self.pilha:
                self.pilha.pop()
            return True
        self.estado_atual = 'erro'
        return False

def ler_arquivo_afd(caminho):
    linhas = [l.strip() for l in open(caminho) if l.strip()]
    estados, inicial, finais, transicoes = [], '', [], {}
    for l in linhas:
        if l.startswith('Q:'): estados = l[2:].split()
        elif l.startswith('I:'): inicial = l[2:].strip()
        elif l.startswith('F:'): finais.append(l[2:].strip())
        elif '->' in l and '|' in l:
            parte, simb = l.split('|')
            src, dst = [x.strip() for x in parte.split('->')]
            for s in simb.split(): transicoes[(src, s)] = dst
        elif l == '---': break
    return estados, inicial, finais, transicoes


def ler_arquivo_apd(caminho):
    linhas = [l.strip() for l in open(caminho) if l.strip()]
    estados, inicial, finais, transicoes = [], '', [], {}
    for l in linhas:
        if l.startswith('Q:'): estados = l[2:].split()
        elif l.startswith('I:'): inicial = l[2:].strip()
        elif l.startswith('F:'): finais.append(l[2:].strip())
        elif '->' in l and '|' in l:
            parte, info = l.split('|')
            src, dst = [x.strip() for x in parte.split('->')]
            simb, topo, acao = info.split()
            transicoes[(src, simb, topo)] = (dst, acao)
        elif l == '---': break
    return estados, inicial, finais, transicoes

def carregar_receitas():
    return {
        'afd_luacheia': ('Lua Cheia', ['AC','AC','AH','OC','ET','VB']),
        'afd_corujamato': ('Coruja-do-Mato', ['VB','AC','VB','AC','OC','ET']),
        'afd_andorinha': ('Andorinha', ['WG','AN'] + ['BF']*6 + ['PT']*6 + ['CE']*4 + ['OC']*4 + ['VT']*2),
        'apd_luacheia': ('Lua Cheia', ['AC','AC','AH','OC','ET','VB'])
    }

def simular_maquina(tipo, caminho):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    nome_pocao, seq_esperada = carregar_receitas().get(nome, ('Receita Desconhecida', []))
    if tipo == 'AFD':
        _, ini, fins, trans = ler_arquivo_afd(caminho)
        auto = AutomatoAFD(None, ini, fins, trans)
    else:
        _, ini, fins, trans = ler_arquivo_apd(caminho)
        auto = AutomatoPilha(None, ini, fins, trans)

    limpar_tela()
    exibir_cabecalho(f"{tipo} - Receita: {nome_pocao}")
    exibir_estado(auto.estado_atual)

    lidos = []
    while True:
        simb = input('Digite ingrediente (ou "fim"): ').strip().lower()
        if simb == 'FIM': break
        exibir_ingrediente(simb)
        sucesso = auto.processar(simb)
        lidos.append(simb)
        limpar_tela()
        exibir_cabecalho(f"{tipo} - Receita: {nome_pocao}")
        exibir_barra(lidos)
        exibir_estado(auto.estado_atual)
        if tipo == 'APD': exibir_pilha(auto.pilha)
        if not sucesso or auto.estado_atual == 'erro':
            print("💥 Receita falhou: mistura corrompida. 💥")
            return

    if auto.estado_atual in auto.estados_finais:
        efeito_vapor()
        efeito_final()
    else:
        print("💥 Receita inválida: não terminou em estado final. 💥")

if __name__ == '__main__':
    limpar_tela()
    print('Escolha a máquina: [1] AFD  [2] APD')
    tipo = 'AFD' if input('Opção: ') == '1' else 'APD'
    simular_maquina(tipo, input('Caminho do arquivo (.txt): '))

