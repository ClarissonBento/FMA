class AutomatoMoore:
    def __init__(self, inicial, trans, saidas):
        self.estado_atual = inicial
        self.transicoes = trans
        self.saidas = saidas

    def processar(self, s):
        chave = (self.estado_atual, s)
        if chave in self.transicoes:
            self.estado_atual = self.transicoes[chave]
            return True
        self.estado_atual = 'erro'
        return False

    def saida_atual(self):
        return self.saidas.get(self.estado_atual, '')


def ler_arquivo_moore(caminho):
    with open(caminho, encoding='utf-8') as arq:
        linhas = [l.strip() for l in arq if l.strip() and not l.startswith('NOME:')]

    ini = ''
    trans = {}
    saida = {}

    for l in linhas:
        if l.startswith('I:') and not ini:
            ini = l[2:].strip()

        elif '->' in l and ';' in l and '|' in l:
            parte_transicao, parte_saida = l.split(';')
            
            origem, destino = [x.strip() for x in parte_transicao.split('->')]
            saida_destino, simbolos = [x.strip() for x in parte_saida.split('|')]

            saida[destino] = saida_destino

            for sym in simbolos.split():
                trans[(origem, sym)] = destino
        
        elif l == '---':
            break

    if not ini:
        ini = 'I'  
    return ini, trans, saida

