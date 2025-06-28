class AutomatoMealy:
    def __init__(self, inicial, trans):
        self.estado_atual = inicial
        self.transicoes = trans

    def processar(self, s):
        chave = (self.estado_atual, s)
        if chave in self.transicoes:
            prox, saida = self.transicoes[chave]
            self.estado_atual = prox
            print(f"Saída: {saida}\n")
            return True
        self.estado_atual = 'erro'
        return False

def ler_arquivo_mealy(caminho):
    linhas = [l.strip() for l in open(caminho, encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini = ''; trans = {}
    for l in linhas:
        if l.startswith('I:') and not ini:
            ini = l[2:].strip()
        elif '->' in l and ';' in l and '|' in l:
            p, r = l.split('|')
            src, rest = [x.strip() for x in p.split('->')]
            sym, saida = [x.strip() for x in r.split(';')]
            dst = rest.strip()
            trans[(src, sym)] = (dst, saida)
        elif l == '---': break
    return ini, trans
