class AutomatoAFD:
    def __init__(self, inicial, finais, trans):
        self.estado_atual = inicial
        self.estados_finais = set(finais)
        self.transicoes = trans

    def processar(self, s):
        chave = (self.estado_atual, s)
        if chave in self.transicoes:
            self.estado_atual = self.transicoes[chave]
            return True
        self.estado_atual = 'erro'
        return False


def ler_arquivo_afd(caminho):
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini = ''; fins = []; trans = {}
    for l in linhas:
        if l.startswith('I:'): ini = l[2:].strip()
        elif l.startswith('F:'): fins += l[2:].split()
        elif '->' in l and '|' in l:
            p, s = l.split('|')
            a, b = [x.strip() for x in p.split('->')]
            for sym in s.split(): trans[(a, sym)] = b
        elif l == '---': break
    return ini, fins, trans
