class AutomatoAPD:
    def __init__(self, inicial, finais, trans, mensagens=None):
        self.estado_atual = inicial
        self.estados_finais = set(finais)
        self.transicoes = trans
        self.pilha = []
        self.mensagens = mensagens or {}

    def processar(self, s):
        topo = self.pilha[-1] if self.pilha else '*'

        chave = (self.estado_atual, s, topo)
        if chave not in self.transicoes:
            chave = (self.estado_atual, s, '*')
            if chave not in self.transicoes:
                self.estado_atual = 'erro'
                return False

        proximo_estado, empilhar = self.transicoes[chave]
        self.estado_atual = proximo_estado

        if chave[2] != '*' and self.pilha and self.pilha[-1] == chave[2]:
            self.pilha.pop()

        if empilhar != '*':
            for simbolo in reversed(empilhar):
                self.pilha.append(simbolo)

        simbolos_verificados = set()

        for simbolo in self.pilha:
            if simbolo in self.mensagens and simbolo not in simbolos_verificados:
                print(f"⚠ {self.mensagens[simbolo]}")
                simbolos_verificados.add(simbolo)

        return True


def ler_arquivo_apd(caminho):
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip() and not l.startswith('MSG:') and not l.startswith('#')]

    ini = ''
    fins = []
    trans = {}

    for l in linhas:
        if l.startswith('I:'):
            ini = l[2:].strip()
        elif l.startswith('F:'):
            fins += l[2:].split()
        elif '->' in l and ';' in l and '|' in l:
            try:
                esquerda, resto = l.split('->')
                estado_atual = esquerda.strip()
                partes = resto.split('|')

                proximo_estado = partes[0].strip()
                simbolo_lido, desempilhar = [x.strip() for x in partes[1].split(';')]
                empilhar = partes[2].strip()

                chave = (estado_atual, simbolo_lido, desempilhar)
                trans[chave] = (proximo_estado, empilhar)
            except Exception as e:
                print(f"⚠ Erro ao processar linha: {l}\n{e}")
        elif l == '---':
            break

    return ini, fins, trans


def ler_mensagens_pilha(caminho):
    mensagens = {}
    with open(caminho, encoding='utf-8') as f:
        for l in f:
            if l.strip().startswith('MSG:'):
                simbolo, mensagem = l.strip()[4:].split('|', 1)
                mensagens[simbolo.strip()] = mensagem.strip()
    return mensagens
