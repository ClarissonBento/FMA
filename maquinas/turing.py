import os
import time

# Mapeamento das runas para caracter
MAPA_RUNAS = {
    'aard': 'a',
    'igni': 'b',
    'yrdden': 'c',
    'quen': 'd',
    'axii': 'e'
}

# Mapeamento reverso
MAPA_SIMBOLOS = {v: k for k, v in MAPA_RUNAS.items()}


CORES_RUNAS = {
    'aard': '\033[94m',     
    'igni': '\033[91m',   
    'yrdden': '\033[95m',  
    'quen': '\033[93m',     
    'axii': '\033[92m',     
    '_': '\033[90m'        
}
RESET = '\033[0m'

def traduzir_runas(entrada):
    runas = entrada.strip().split()
    return ''.join(MAPA_RUNAS[runa] for runa in runas if runa in MAPA_RUNAS)

class MaquinaTuring:
    def __init__(self, ini, finais, trans):
        self.estado_inicial = ini
        self.estados_finais = finais
        self.transicoes = trans
        self.estado_atual = ini
        self.fita = []
        self.cabecote = 0

    def inicializar_fita(self, palavra):
        self.fita = list(palavra) + ["_"] * 10
        self.cabecote = 0
        self.estado_atual = self.estado_inicial

    def fita_com_runas(self):
        fita_colorida = []
        for s in self.fita:
            runa = MAPA_SIMBOLOS.get(s, s)
            cor = CORES_RUNAS.get(runa, RESET)
            fita_colorida.append(f"{cor}{runa}{RESET}")
        return fita_colorida

    def imprimir_fita(self,  delay=0.5):
        fita_runica = self.fita_com_runas()
        fita_str = ""
        fita_filtrada = [runa for i, runa in enumerate(fita_runica) if self.fita[i] != '_']
        for i, simbolo in enumerate(fita_runica):
            if i == self.cabecote:
                fita_str += f"[{simbolo}]"
            else:
                fita_str += f" {simbolo} "
        #print(f"🧙 Estado do Bruxo: {self.estado_atual}")
        #print(f"🔮 Fita das Runas: {fita_str}\n")
        if self.estado_atual in ['q0']:
            time.sleep(delay)
            print("", ' '.join(fita_filtrada), "\n")

    def processar(self):
        while True:
            self.imprimir_fita()

            simbolo_lido = self.fita[self.cabecote]
            chave = (self.estado_atual, simbolo_lido)

            if chave not in self.transicoes:
                print("⚠️ A magia falhou! Nenhuma runa respondeu ao gesto.")
                return False

            proximo_estado, simbolo_escrito, direcao = self.transicoes[chave]
            self.fita[self.cabecote] = simbolo_escrito

            if direcao == "R":
                self.cabecote += 1
                if self.cabecote >= len(self.fita):
                    self.fita.append("_")
            elif direcao == "L":
                self.cabecote = max(0, self.cabecote - 1)

            self.estado_atual = proximo_estado

            if all(s == "_" for s in self.fita):
                if self.estado_atual in self.estados_finais:
                    print("✨ O feitiço foi concluído com sucesso! As runas brilham na escuridão.")
                    return True
                else:
                    print("💥 A magia falhou! As runas se desfizeram sem efeito.")
                    return False

def ler_arquivo_turing(caminho):
    with open(caminho, 'r') as f:
        linhas = f.readlines()

    transicoes = {}
    ini = ""
    finais = []

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if linha.startswith("I:"):
            ini = linha.split(":", 1)[1].strip()
        elif linha.startswith("F:"):
            finais = linha.split(":")[1].strip().split()
        elif "->" in linha:
            partes = linha.split("|")
            estado_atual, proximo_estado = partes[0].split("->")
            simbolo_lido = partes[1].strip()
            simbolo_escrito = partes[2].strip()
            direcao = partes[3].strip()

            transicoes[(estado_atual.strip(), simbolo_lido)] = (
                proximo_estado.strip(), simbolo_escrito, direcao
            )

    return ini, finais, transicoes
