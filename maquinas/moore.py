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
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini = ''; trans = {}; saida = {}
    for l in linhas:
        if l.startswith('I:') and not ini:
            ini = l[2:].strip()
        elif '->' in l and ';' in l and '|' in l:
            p, r = l.split(';')
            dst, syms = [x.strip() for x in p.split('->')]
            out, syms2 = [x.strip() for x in r.split('|')]
            saida[dst] = out
            for sym in syms2.split():
                trans[(p.split('->')[0].strip(), sym)] = dst
        elif l == '---': break
    return ini, trans, saida
