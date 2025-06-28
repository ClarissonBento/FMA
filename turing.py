# convertendo as palavras para simbolos para facilitar
para_simbolo = {
    'aard': 'a',
    'igni': 'b',
    'yrdden': 'c',
    'quen': 'd',
    'axii': 'e'
}

class MaquinaTuring:
    def __init__(self, fita, estado_inicial, estado_aceitacao, estado_rejeicao, transicoes):
        self.fita = list(fita) + ['␣']
        self.estado = estado_inicial
        self.estado_aceitacao = estado_aceitacao
        self.estado_rejeicao = estado_rejeicao
        self.transicoes = transicoes
        self.pos = 0

    def passo(self):
        simbolo = self.fita[self.pos]
        chave = (self.estado, simbolo)
        if chave in self.transicoes:
            novo_estado, novo_simbolo, direcao = self.transicoes[chave]
            self.fita[self.pos] = novo_simbolo
            self.estado = novo_estado
            if direcao == 'R':
                self.pos += 1
            elif direcao == 'L':
                self.pos -= 1
            return True
        else:
            return False

    def executar(self):
        # Sem prints dos passos — só roda
        while self.estado not in ["q_accept", "q_reject"]:
            if not self.passo():
                self.estado = "q_reject"
                break
        return self.estado == "q_accept"

# Transições da MT
transicoes = {}
alfabeto = 'abcde'

for letra in alfabeto:
    transicoes[('q0', letra)] = (f'q1{letra}', 'X', 'R')

for l in alfabeto + 'X':
    for estado in [f'q1{c}' for c in alfabeto]:
        transicoes[(estado, l)] = (estado, l, 'R')

for c in alfabeto:
    transicoes[(f'q1{c}', '␣')] = (f'q2{c}', '␣', 'L')

for c in alfabeto:
    for l in alfabeto:
        if c == l:
            transicoes[(f'q2{c}', l)] = ('q3', 'X', 'L')
        else:
            transicoes[(f'q2{c}', l)] = ('q_reject', l, 'S')
    transicoes[(f'q2{c}', 'X')] = (f'q2{c}', 'X', 'L')
    transicoes[(f'q2{c}', '␣')] = ('q_accept', '␣', 'S')

for l in alfabeto + 'X':
    transicoes[('q3', l)] = ('q3', l, 'L')
transicoes[('q3', '␣')] = ('q0', '␣', 'R')

transicoes[('q0', 'X')] = ('q0', 'X', 'R')
transicoes[('q0', '␣')] = ('q_accept', '␣', 'S')

entrada_magica = input("Digite suas runas mágicas separadas por espaço (aard igni yrdden quen axii):\n").strip().lower().split()

if all(palavra in para_simbolo for palavra in entrada_magica):
    entrada_convertida = ''.join([para_simbolo[p] for p in entrada_magica])
    mt = MaquinaTuring(
        fita=entrada_convertida,
        estado_inicial="q0",
        estado_aceitacao="q_accept",
        estado_rejeicao="q_reject",
        transicoes=transicoes
    )
    sucesso = mt.executar()
    if sucesso:
        print("\nO feitiço foi lançado com sucesso! Suas runas formam um palíndromo")
    else:
        print("\nA magia falhou, as runas não formam um palíndromo")
else:
    print("Erro: Use apenas as runas permitidas: aard, igni, yrdden, quen, axii.")
