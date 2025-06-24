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
    print(titulo.center(largura + 2))
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

class AutomatoAPD:
    def __init__(self, estados, inicial, finais, transicoes):
        self.estado_atual = inicial
        self.estados_finais = set(finais)
        self.transicoes = transicoes
        self.pilha = []

    def processar(self, simbolo):
        topo = self.pilha[-1] if self.pilha else '*'

        chave = (self.estado_atual, simbolo, topo)
        if chave not in self.transicoes:
            chave = (self.estado_atual, simbolo, '*')
            if chave not in self.transicoes:
                self.estado_atual = 'erro'
                return False

        prox, empilhar = self.transicoes[chave]
        self.estado_atual = prox
        desempilhar = chave[2]
        if desempilhar != '*' and self.pilha:
            self.pilha.pop()
        if empilhar != '*':
            self.pilha.append(empilhar)

        return True



def ler_arquivo_afd(caminho):
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip()]
    estados, inicial, finais, transicoes = [], '', [], {}
    for l in linhas:
        if l.startswith('Q:'):
            estados = l[2:].split()
        elif l.startswith('I:'):
            inicial = l[2:].strip()
        elif l.startswith('F:'):
            finais.extend(l[2:].split())
        elif '->' in l and '|' in l:
            parte, simb = l.split('|')
            src, dst = [x.strip() for x in parte.split('->')]
            for s in simb.split():
                transicoes[(src, s)] = dst
        elif l == '---':
            break
    return estados, inicial, finais, transicoes

def ler_arquivo_apd(caminho):
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip()]
    estados, inicial, finais, transicoes, mensagens = [], '', [], {}, {}
    for l in linhas:
        if l.startswith('Q:'):
            estados = l[2:].split()
        elif l.startswith('I:'):
            inicial = l[2:].strip()
        elif l.startswith('F:'):
            finais.extend(l[2:].split())
        elif '->' in l and '|' in l and ';' in l:
            parte1, resto = l.split('|', 1)
            src, dst = [x.strip() for x in parte1.split('->')]
            simbolo_lido, resto2 = resto.split(';', 1)
            simbolo_lido = simbolo_lido.strip()
            desempilhar, empilhar = [x.strip() for x in resto2.split('|')]
            transicoes[(src, simbolo_lido, desempilhar)] = (dst, empilhar)
        elif l.startswith('MSG:'):
            _, resto = l.split(':', 1)
            simbolo, mensagem = [x.strip() for x in resto.split('|', 1)]
            mensagens[simbolo] = mensagem
        elif l == '---':
            break
    return estados, inicial, finais, transicoes, mensagens

def carregar_receitas():
    return {
        'afd_luacheia': ('Lua Cheia', ['ac','ac','ah','oc','et','vb']),
        'afd_corujamato': ('Coruja-do-Mato', ['vb','ac','vb','ac','oc','et']),
        'afd_andorinha': ('Andorinha', ['wg','an'] + ['bf']*6 + ['pt']*6 + ['ce']*4 + ['oc']*4 + ['vt']*2),
        'apd_luacheia': ('Lua Cheia', ['ac','ac','ah','oc','et','vb'])
    }

def simular_maquina(tipo, caminho):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    nome_pocao, seq_esperada = carregar_receitas().get(nome, ('Receita Desconhecida', []))

    if tipo == 'AFD':
        _, ini, fins, trans = ler_arquivo_afd(caminho)
        auto = AutomatoAFD(None, ini, fins, trans)
        mensagens = {}
    else:
        _, ini, fins, trans, mensagens = ler_arquivo_apd(caminho)
        auto = AutomatoAPD(None, ini, fins, trans)

    limpar_tela()
    exibir_cabecalho(f"{tipo} - Receita: {nome_pocao}")
    exibir_estado(auto.estado_atual)

    lidos = []
    while True:
        simb = input('Digite ingrediente (ou "fim"): ').strip().lower()
        if simb == 'fim':
            break
        exibir_ingrediente(simb)
        sucesso = auto.processar(simb)
        lidos.append(simb)
        time.sleep(0.5)
        limpar_tela()
        exibir_cabecalho(f"{tipo} - Receita: {nome_pocao}")
        exibir_barra(lidos)
        exibir_estado(auto.estado_atual)

        if tipo == 'APD':
            exibir_pilha(auto.pilha)
            for simb_m in mensagens:
                if simb_m in auto.pilha:
                    print(f"⚠️ Atenção: {mensagens[simb_m]}\n")

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
    opcao = input('Opção: ').strip()
    tipo = 'AFD' if opcao == '1' else 'APD'
    caminho = input('Caminho do arquivo (.txt): ').strip()
    simular_maquina(tipo, caminho)
