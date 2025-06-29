import re

class AutomatoMealy:
    def __init__(self, inicial, transicoes):
        self.estado_atual = inicial
        self.transicoes = transicoes

    def processar(self, s):
        chave = (self.estado_atual, s)
        if chave in self.transicoes:
            prox, saida = self.transicoes[chave]
            self.estado_atual = prox
            # String f totalmente fechada
            print(f"Saída: {saida}\n")
            return True
        self.estado_atual = 'erro'
        return False

def ler_arquivo_mealy(caminho):
    ini = None
    trans = {}

    # todas as linhas não vazias
    with open(caminho, encoding='utf-8-sig') as f:
        for raw in f:
            l = raw.strip()
            if not l:
                continue

            # Estado inicial: linha “I: <valor>”
            if l.upper().startswith('I:') and ini is None:
                ini = l.split(':', 1)[1].strip()
                continue

            # separador
            if l == '---':
                break

            # transição: origem -> destino | símbolo ; saída
            if '->' in l and '|' in l and ';' in l:
                left, right = l.split('|', 1)
                origem, destino = [x.strip() for x in left.split('->', 1)]
                simbolo, saida = [x.strip() for x in right.split(';', 1)]
                trans[(origem, simbolo)] = (destino, saida)

    if ini is None:
        raise ValueError("Estado inicial não encontrado no arquivo Mealy.")
    return ini, trans