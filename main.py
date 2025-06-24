#Tema: The Witcher 3 - FTC
import time
import os

# utilitários

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
    time.sleep(0.6)

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

def efeito_borbulha(): time.sleep(0.6)

def efeito_agitar(): time.sleep(0.6)

def efeito_transformacao(): time.sleep(0.6)

def efeito_vapor():
    time.sleep(0.8)
    print("~ vapores místicos... ~\n")

def efeito_final():
    for simbolo in ["⧫","◆","◇","◇","◆","⧫"]:
        print(simbolo, end=" ", flush=True)
        time.sleep(0.5)
    print("\n✨ Poção forjada! ✨\n")

class AutomatoAFD:
    def __init__(self,inicial,finais,trans): self.estado_atual=inicial; self.estados_finais=set(finais); self.transicoes=trans
    def processar(self,s):
        chave=(self.estado_atual,s)
        if chave in self.transicoes: self.estado_atual=self.transicoes[chave]; return True
        self.estado_atual='erro'; return False

class AutomatoAPD:
    def __init__(self,inicial,finais,trans): self.estado_atual=inicial; self.estados_finais=set(finais); self.transicoes=trans; self.pilha=[]
    def processar(self,s):
        topo=self.pilha[-1] if self.pilha else '*'
        chave=(self.estado_atual,s,topo)
        if chave not in self.transicoes:
            chave=(self.estado_atual,s,'*')
            if chave not in self.transicoes: self.estado_atual='erro'; return False
        prox,emp=self.transicoes[chave]; self.estado_atual=prox
        if topo!='*' and self.pilha: self.pilha.pop()
        if emp!='*': self.pilha.append(emp)
        return True

class AutomatoMoore:
    def __init__(self,inicial,trans,saida): self.estado_atual=inicial; self.transicoes=trans; self.saidas=saida
    def processar(self,s):
        chave=(self.estado_atual,s)
        if chave in self.transicoes: self.estado_atual=self.transicoes[chave]; return True
        self.estado_atual='erro'; return False
    def saida_atual(self): return self.saidas.get(self.estado_atual,'')

class AutomatoMealy:
    def __init__(self,inicial,trans): self.estado_atual=inicial; self.transicoes=trans
    def processar(self,s):
        chave=(self.estado_atual,s)
        if chave in self.transicoes:
            prox,saida=self.transicoes[chave]; self.estado_atual=prox; print(f"Saída: {saida}\n"); return True
        self.estado_atual='erro'; return False

# leitura genérica incluindo NOME:

def ler_header(c):
    with open(c,encoding='utf-8') as f:
        for l in f:
            if l.strip().startswith('NOME:'):
                return l.split(':',1)[1].strip()
    return os.path.basename(c)

def ler_arquivo_afd(c):
    linhas=[l.strip() for l in open(c,encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini='';fins=[];trans={}
    for l in linhas:
        if l.startswith('I:'): ini=l[2:].strip()
        elif l.startswith('F:'): fins+=l[2:].split()
        elif '->' in l and '|' in l:
            p,s=l.split('|');a,b=[x.strip() for x in p.split('->')]
            for sym in s.split(): trans[(a,sym)]=b
        elif l=='---': break
    return ini,fins,trans

def ler_arquivo_apd(c):
    linhas=[l.strip() for l in open(c,encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini='';fins=[];trans={}
    for l in linhas:
        if l.startswith('I:'): ini=l[2:].strip()
        elif l.startswith('F:'): fins+=l[2:].split()
        elif '->' in l and '|' in l and ';' in l:
            part,rest=l.split('|',1);src,dst=[x.strip() for x in part.split('->')]
            sym,des,emp=[x.strip() for x in rest.split('|')]
            trans[(src,sym,des)]=(dst,emp)
        elif l=='---': break
    return ini,fins,trans

def ler_arquivo_moore(c):
    linhas=[l.strip() for l in open(c,encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini='';trans={};saida={}
    for l in linhas:
        if l.startswith('I:') and not ini: ini=l[2:].strip()
        elif '->' in l and ';' in l and '|' in l:
            p,r=l.split(';');dst,syms=[x.strip() for x in p.split('->')]
            out,syms2=[x.strip() for x in r.split('|')]
            saida[dst]=out
            for sym in syms2.split(): trans[(p.split('->')[0].strip(),sym)]=dst
        elif l=='---': break
    return ini,trans,saida

def ler_arquivo_mealy(c):
    linhas=[l.strip() for l in open(c,encoding='utf-8') if l.strip() and not l.startswith('NOME:')]
    ini='';trans={}
    for l in linhas:
        if l.startswith('I:') and not ini: ini=l[2:].strip()
        elif '->' in l and ';' in l and '|' in l:
            p,r=l.split('|');src,rest=[x.strip() for x in p.split('->')]
            sym,saida=[x.strip() for x in r.split(';')]
            dst=rest.strip()
            trans[(src,sym)]=(dst,saida)
        elif l=='---': break
    return ini,trans

# simulação unificada

def simular(tipo,arquivo):
    nome=ler_header(arquivo)
    limpar_tela(); exibir_cabecalho(f"{tipo} - Poção: {nome}")
    if tipo=='AFD': ini,fins,trans=ler_arquivo_afd(arquivo);auto=AutomatoAFD(ini,fins,trans)
    if tipo=='APD': ini,fins,trans=ler_arquivo_apd(arquivo);auto=AutomatoAPD(ini,fins,trans)
    if tipo=='MOORE': ini,trans,saida=ler_arquivo_moore(arquivo);auto=AutomatoMoore(ini,trans,saida)
    if tipo=='MEALY': ini,trans=ler_arquivo_mealy(arquivo);auto=AutomatoMealy(ini,trans)
    exibir_estado(auto.estado_atual)
    pila=getattr(auto,'pilha',None)
    while True:
        s=input('Digite símbolo (ou "fim"): ').strip().lower()
        if s=='fim': break
        exibir_ingrediente(s)
        ok=auto.processar(s)
        limpar_tela(); exibir_cabecalho(f"{tipo} - Poção: {nome}")
        if tipo in ['AFD','APD']: exibir_barra(getattr(auto,'pilha',[]) if tipo=='APD' else [] if False else [] )
        exibir_estado(auto.estado_atual)
        if tipo=='APD': exibir_pilha(auto.pilha)
        if not ok or auto.estado_atual=='erro': print("💥 Erro na simulação.");return
    if tipo in ['AFD','APD'] and auto.estado_atual in auto.estados_finais: efeito_vapor();efeito_final()
    if tipo=='MOORE': print(f"Saída final: {auto.saida_atual()}")
    if tipo=='MEALY': print("Simulação Mealy concluída.")

if __name__=='__main__':
    limpar_tela()
    print('[1] AFD  [2] APD  [3] MOORE  [4] MEALY')
    op=input('Opção: ').strip()
    tipos={'1':'AFD','2':'APD','3':'MOORE','4':'MEALY'}
    simular(tipos.get(op,'AFD'),input('Arquivo (.txt): ').strip())
