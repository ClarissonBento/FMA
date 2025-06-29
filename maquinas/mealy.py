class AutomatoMealy:
    def __init__(self, inicial, transicoes):
        self.estado_atual = inicial
        self.transicoes = transicoes
        self.saida_total = '' 

    def processar(self, s):
        chave = (self.estado_atual, s)
        if chave in self.transicoes:
            prox, saida = self.transicoes[chave]
            self.estado_atual = prox
            if saida != 'λ':
                self.saida_total += saida  
            return True
        self.estado_atual = 'erro'
        return False

    def saida_atual(self):
        return self.saida_total


def ler_arquivo_mealy(caminho):
    ini = None
    trans = {}

    with open(caminho, encoding='utf-8-sig') as f:
        for raw in f:
            l = raw.strip()
            if not l:
                continue

            if l.upper().startswith('I:') and ini is None:
                ini = l.split(':', 1)[1].strip()
                continue

            if l == '---':
                break

            if '->' in l and '|' in l and ';' in l:
                left, right = l.split('|', 1)
                origem, destino = [x.strip() for x in left.split('->', 1)]
                simbolo, saida = [x.strip() for x in right.split(';', 1)]
                trans[(origem, simbolo)] = (destino, saida)

    if ini is None:
        raise ValueError("Estado inicial não encontrado no arquivo Mealy.")
    return ini, trans
