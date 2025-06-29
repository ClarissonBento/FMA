import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from util import * 
from maquinas.automato_finito import AutomatoAFD, ler_arquivo_afd
from maquinas.turing import MaquinaTuring, ler_arquivo_turing
import mapa

class AplicativoDePocoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Fabricação de Poções")
        self.base_path = os.path.dirname(__file__)  
        self.root.configure(bg='white') 

        #lista de arquivos de imagem dos ingredientes
        self.ingredientes_arquivos = [
            "aconito.webp", "alcohest.webp", "azufre.webp", "bryonia.webp", "cerebroafogador.webp", "cogumeloesgoto.webp", "cortinarius.webp", "essenciatrevas.webp", "folhascicuta.webp", "gaivotabranca.webp", "olhocorvo.webp", "petalasmurtabranca.webp", "quelidonia.webp", "raizmandragora.webp", "verbena.webp", "salitre.webp", "vitriol.webp", "pastaalquimica.webp"
        ]
        self.ingredientes = [os.path.join(self.base_path, 'img_ingredientes', img) for img in self.ingredientes_arquivos]

        self.ingredientes_selecionados = [] #pra AFD
        self.entrada_mt_texto = tk.StringVar() #pra MT
        
        self.tipo_maquina = None  #armazena o tipo de máquina
        self.pocao = None  #armazena o nome da poção
        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        self.limpar_tela()

        #configura o grid da janela principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        #inicio
        self.rotulo_mensagem = tk.Label(self.root, text="Vamos iniciar a fabricação de poções! Clique em INICIAR para começar", font=("Arial", 16), bg='white')
        self.rotulo_mensagem.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        self.botao_iniciar = tk.Button(self.root, text="INICIAR", command=self.criar_tela_selecao_maquina)
        self.botao_iniciar.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

    def criar_tela_selecao_maquina(self):
        self.limpar_tela()

        #configura o grid da janela principal imediatamente após limpar
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        #mensagem sobre escolher o tipo de máquina
        tk.Label(self.root, text="Escolha o tipo de máquina:", font=("Arial", 14), bg='white').grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        #botões para selecionar tipo de máquina (foi melhor deixar só AFD e MT)
        self.botao_af = tk.Button(self.root, text="AFD", command=self.selecionar_tipo_maquina_afd)
        self.botao_af.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.botao_mt = tk.Button(self.root, text="MT", command=self.selecionar_tipo_maquina_mt)
        self.botao_mt.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def selecionar_tipo_maquina_afd(self):
        self.tipo_maquina = 'AFD'
        self.criar_tela_selecao_pocao()
    
    def selecionar_tipo_maquina_mt(self):
        self.tipo_maquina = 'MT'
        self.criar_tela_selecao_pocao()
    
    def criar_tela_selecao_pocao(self):
        self.limpar_tela()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        frame_botao_pocoes = tk.Frame(self.root, bg='white')
        frame_botao_pocoes.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        tk.Label(frame_botao_pocoes, text=f"Escolha a poção desejada para {self.tipo_maquina}:", font=("Arial", 14), bg='white').grid(row=0, column=0, columnspan=3, pady=20, padx=20)

        #filtra as poções com base no tipo de máquina selecionado
        nomes_pocoes_filtradas = mapa.MAPA_TIPO_MAQUINA_POCOES.get(self.tipo_maquina, [])

        #calcula o número de linhas e colunas necessárias
        num_pocoes = len(nomes_pocoes_filtradas)
        colunas = 3
        linhas = (num_pocoes + colunas - 1) // colunas

        #adiciona botões ao grid
        for i, nome_pocao in enumerate(nomes_pocoes_filtradas):
            row = i // colunas
            col = i % colunas
            botao = tk.Button(frame_botao_pocoes, text=nome_pocao, command=lambda p=nome_pocao: self.decidir_proxima_tela_por_maquina(p), width=20)
            botao.grid(row=row + 1, column=col, padx=10, pady=10, sticky="ew")

        for i in range(colunas):
            frame_botao_pocoes.grid_columnconfigure(i, weight=1)
        for i in range(linhas + 1):
            frame_botao_pocoes.grid_rowconfigure(i, weight=1)

        btn_voltar_maquina = tk.Button(self.root, text="VOLTAR", command=self.criar_tela_selecao_maquina, font=("Arial", 14), bg='#D3D3D3')
        btn_voltar_maquina.grid(row=linhas + 1, column=0, columnspan=2, pady=20)

    #função que decide a próxima tela
    def decidir_proxima_tela_por_maquina(self, nome_pocao):
        self.pocao = nome_pocao
        if self.tipo_maquina == 'MT':
            self.criar_tela_entrada_mt()
        elif self.tipo_maquina == 'AFD':
            self.criar_tela_selecao_ingredientes()
        

    #tela da Máquina de Turing
    def criar_tela_entrada_mt(self):
        self.limpar_tela()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)

        tk.Label(self.root, text=f"Máquina de Turing: {self.pocao}", font=("Arial", 16, "bold"), bg='white').grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        tk.Label(self.root, text="Digite a palavra (caracteres do alfabeto da MT):", font=("Arial", 12), bg='white').grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.entrada_mt_entry = tk.Entry(self.root, textvariable=self.entrada_mt_texto, font=("Arial", 14), width=40)
        self.entrada_mt_entry.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        # Frame para os botões
        frame_botoes_mt = tk.Frame(self.root, bg='white')
        frame_botoes_mt.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")
        frame_botoes_mt.grid_columnconfigure(0, weight=1)
        frame_botoes_mt.grid_columnconfigure(1, weight=1)
        frame_botoes_mt.grid_columnconfigure(2, weight=1) # Para o botão de encerrar

        tk.Button(frame_botoes_mt, text="PROCESSAR PALAVRA", command=self.processar_entrada_mt, bg='lightgreen').grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        tk.Button(frame_botoes_mt, text="VOLTAR", command=self.criar_tela_selecao_pocao, bg='lightgrey').grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        tk.Button(frame_botoes_mt, text="ENCERRAR FABRICAÇÃO", command=self.encerrar_fabricacao, bg='salmon').grid(row=0, column=2, padx=5, pady=10, sticky="ew")

    #processa a entrada da Máquina de Turing
    def processar_entrada_mt(self):
        entrada_palavra = self.entrada_mt_texto.get().strip()


        simbolos_permitidos_mt = set("abcde")

        if entrada_palavra:
            if not all(char.lower() in simbolos_permitidos_mt for char in entrada_palavra):
                messagebox.showwarning("Entrada Inválida", f"A palavra para a Máquina de Turing contém símbolos não permitidos.\nPermitidos (exemplo): {list(simbolos_permitidos_mt)}")
                return
        
        #finalizar_pocao passando a string da entrada da MT
        self.finalizar_pocao(entrada_mt_string=entrada_palavra)
        self.entrada_mt_texto.set("")


    def criar_tela_selecao_ingredientes(self):
        #tela só para AFD
        self.limpar_tela()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        frame_superior = tk.Frame(self.root, bg='white')
        frame_superior.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.frame_ingrediente_atual = tk.Frame(frame_superior, bg='lightgrey', borderwidth=2, relief='solid', width=100, height=100)
        self.frame_ingrediente_atual.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_lista = tk.Frame(frame_superior, bg='lightgrey', borderwidth=2, relief='solid', width=140, height=100)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lista_ingredientes = tk.Listbox(self.frame_lista, width=20, height=8, bg='white', borderwidth=2, relief='sunken')
        self.lista_ingredientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_lista_ingredientes = tk.Scrollbar(self.frame_lista, orient=tk.VERTICAL, command=self.lista_ingredientes.yview)
        scroll_lista_ingredientes.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_ingredientes.config(yscrollcommand=scroll_lista_ingredientes.set)

        self.frame_inventario = tk.Frame(self.root, bg='white')
        self.frame_inventario.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.frame_inventario.grid_rowconfigure(list(range(2)), weight=1) 
        for i in range(11): 
            self.frame_inventario.grid_columnconfigure(i, weight=1)

        frame_botoes = tk.Frame(self.root, bg='white')
        frame_botoes.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")


        self.botao_adicionar = tk.Button(frame_botoes, text="ADICIONAR INGREDIENTE", command=self.adicionar_ingrediente_selecionado, bg='lightblue')
        self.botao_adicionar.grid(row=0, column=0, pady=10, padx=5, sticky="ew")

        #estado inicial do botão FINALIZAR POÇÃO
        self.botao_finalizar = tk.Button(frame_botoes, text="FINALIZAR POÇÃO", command=self.finalizar_pocao, state=tk.DISABLED, bg='lightgreen')
        self.botao_finalizar.grid(row=0, column=1, pady=10, padx=5, sticky="ew")

        self.botao_encerrar = tk.Button(frame_botoes, text="ENCERRAR FABRICAÇÃO", command=self.encerrar_fabricacao, bg='salmon')
        self.botao_encerrar.grid(row=0, column=2, pady=10, padx=5, sticky="ew")

        self.botao_voltar = tk.Button(frame_botoes, text="VOLTAR", command=self.criar_tela_selecao_pocao, bg='lightgrey')
        self.botao_voltar.grid(row=0, column=3, pady=10, padx=5, sticky="ew")

        self.recarregar_inventario()

        frame_superior.grid_columnconfigure(0, weight=1)
        frame_superior.grid_columnconfigure(1, weight=1)
        frame_superior.grid_rowconfigure(0, weight=1)

        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)
        frame_botoes.grid_columnconfigure(2, weight=1)
        frame_botoes.grid_columnconfigure(3, weight=1)

        for ingrediente_nome in self.ingredientes_selecionados:
            self.lista_ingredientes.insert(tk.END, ingrediente_nome)
        
        self.botao_finalizar.config(state=tk.NORMAL if len(self.ingredientes_selecionados) >= 1 else tk.DISABLED) 

    def recarregar_inventario(self):
        for widget in self.frame_inventario.winfo_children():
            widget.destroy()
        
        for i, ingrediente_path in enumerate(self.ingredientes):
            img = Image.open(ingrediente_path)
            img = img.resize((80, 80), Image.LANCZOS) 
            tk_img = ImageTk.PhotoImage(img)
            btn = tk.Button(self.frame_inventario, image=tk_img, command=lambda i_path=ingrediente_path: self.exibir_ingrediente_atual(i_path), relief='flat')
            btn.image = tk_img  
            btn.grid(row=i // 11, column=i % 11, padx=5, pady=5)

    def exibir_ingrediente_atual(self, ingrediente_path):
        for widget in self.frame_ingrediente_atual.winfo_children():
            widget.destroy()

        img = Image.open(ingrediente_path)
        img = img.resize((80, 80), Image.LANCZOS) 
        tk_img = ImageTk.PhotoImage(img)
        rotulo = tk.Label(self.frame_ingrediente_atual, image=tk_img)
        rotulo.image = tk_img  
        rotulo.pack(padx=10, pady=10)

        self.ingrediente_atual = ingrediente_path

    def adicionar_ingrediente_selecionado(self):
        if hasattr(self, 'ingrediente_atual') and self.ingrediente_atual: 
            caminho_ingrediente = self.ingrediente_atual
            nome_ingrediente = os.path.splitext(os.path.basename(caminho_ingrediente))[0]
            
            #adiciona o nome do ingrediente à lista de selecionados
            self.ingredientes_selecionados.append(nome_ingrediente)
            self.lista_ingredientes.insert(tk.END, nome_ingrediente)
            
            self.limpar_espaco_ingrediente()
            self.botao_finalizar.config(state=tk.NORMAL if len(self.ingredientes_selecionados) >= 1 else tk.DISABLED) 
            
            self.ingrediente_atual = None
        else:
            messagebox.showwarning("Nenhum Ingrediente Selecionado", "Por favor, selecione um ingrediente no inventário abaixo.")

    def limpar_espaco_ingrediente(self):
        for widget in self.frame_ingrediente_atual.winfo_children():
            widget.destroy()

    def finalizar_pocao(self, entrada_mt_string=None):
        self.limpar_tela() 

        resultado_simulacao = "falhou" 
        nome_pocao_final = self.pocao 

        try:
            caminho_arquivo_maquina = mapa.MAPA_POCOES_ARQUIVOS.get(nome_pocao_final)
            if not caminho_arquivo_maquina:
                raise ValueError(f"Receita para a poção '{nome_pocao_final}' não encontrada no mapeamento em mapa.py.")
            
            caminho_arquivo_maquina = os.path.join(self.base_path, caminho_arquivo_maquina)

            print(f"\n--- INICIANDO SIMULAÇÃO ---") #DEBUG
            print(f"Tipo de Máquina Selecionada: {self.tipo_maquina}") #DEBUG
            print(f"Poção Selecionada: {nome_pocao_final}") #DEBUG
            print(f"Caminho absoluto do arquivo da máquina: {caminho_arquivo_maquina}") #DEBUG

            simbolos_para_simulacao = []
            if self.tipo_maquina == 'AFD':
                if self.ingredientes_selecionados:
                    for ingrediente_nome in self.ingredientes_selecionados:
                        simbolo_maquina = mapa.MAPA_INGREDIENTES_SIMBOLOS.get(ingrediente_nome.lower())
                        if simbolo_maquina:
                            simbolos_para_simulacao.append(simbolo_maquina)
                        else:
                            raise ValueError(f"Ingrediente '{ingrediente_nome}' não possui um símbolo de máquina correspondente no mapeamento (mapa.MAPA_INGREDIENTES_SIMBOLOS). Simulação abortada.")
                else:
                    print("Nenhum ingrediente selecionado para AFD. Verificando se a máquina pode processar entrada vazia.")
                
                print(f"Ingredientes selecionados (GUI): {self.ingredientes_selecionados}") #DEBUG
                print(f"Símbolos traduzidos para simulação: {simbolos_para_simulacao}") #DEBUG
            elif self.tipo_maquina == 'MT':
                simbolos_para_simulacao = list(entrada_mt_string)
                print(f"Palavra de entrada para MT: '{entrada_mt_string}' (traduzida para lista: {simbolos_para_simulacao})") #DEBUG


            #lógica de simulação baseada no tipo de máquina
            if self.tipo_maquina == 'AFD':
                ini, fins, trans = ler_arquivo_afd(caminho_arquivo_maquina)
                maquina = AutomatoAFD(ini, fins, trans)
                
                print(f"AFD: Estado Inicial: {ini}, Estados Finais: {fins}, Transições: {trans}") #DEBUG
                
                aceita = True
                for simbolo in simbolos_para_simulacao:
                    if not maquina.processar(simbolo): 
                        aceita = False
                        break
                
                if aceita and maquina.estado_atual in maquina.estados_finais: 
                    resultado_simulacao = "aceita"
                else:
                    resultado_simulacao = "falhou"
                
                print(f"AFD: Resultado final: {'Aceita' if resultado_simulacao == 'aceita' else 'Rejeita'}") #DEBUG
                print(f"AFD: Estado final da máquina: {maquina.estado_atual}") #DEBUG

            elif self.tipo_maquina == 'MT':
                ini, fins, trans = ler_arquivo_turing(caminho_arquivo_maquina)
                maquina = MaquinaTuring(ini, fins, trans) 

                print(f"MT: Estado Inicial: {ini}, Estados Finais: {fins}, Transições: {trans}") #DEBUG

                palavra_mt_str = entrada_mt_string 
                
                maquina.inicializar_fita(palavra_mt_str) 
                
                print(f"MT: Fita inicializada: {list(maquina.fita)}, Cabeçote: {maquina.cabecote}, Estado: {maquina.estado_atual}") #DEBUG
                
                aceita = maquina.processar() 
                
                print(f"MT: Resultado final do processamento: {aceita}, Estado final: {maquina.estado_atual}, Fita final: {list(maquina.fita)}") #DEBUG
                
                resultado_simulacao = "aceita" if aceita else "falhou"
                
                print(f"MT: Resultado final: {'Aceita' if resultado_simulacao == 'aceita' else 'Rejeita'}") #DEBUG

            else:
                messagebox.showerror("Erro de Tipo de Máquina", f"Tipo de máquina '{self.tipo_maquina}' não reconhecido para simulação.")
                resultado_simulacao = "falhou"

        except FileNotFoundError as e:
            messagebox.showerror("Erro de Arquivo", f"Arquivo da máquina não encontrado ou caminho incorreto: {e}\nVerifique o mapeamento em mapa.py e a existência do arquivo.")
            resultado_simulacao = "falhou"
            print(f"ERRO: Arquivo não encontrado: {e}") #DEBUG
        except ValueError as e:
            messagebox.showerror("Erro de Configuração", str(e))
            resultado_simulacao = "falhou"
            print(f"ERRO: Erro de configuração/mapeamento: {e}") #DEBUG
        except Exception as e:
            messagebox.showerror("Erro de Simulação", f"Ocorreu um erro inesperado durante a simulação: {e}\nTipo: {type(e).__name__}\nVerifique a implementação da classe da máquina.")
            resultado_simulacao = "falhou"
            import traceback
            traceback.print_exc() 
            print(f"ERRO INESPERADO DURANTE SIMULAÇÃO: {e} (Tipo: {type(e).__name__})") #DEBUG


        #EXIBIÇÃO FINAL DO RESULTADO como texto
        if resultado_simulacao == "aceita":
            detalhes = f"Resultado: SUCESSO!"
            print(f"\nPOÇÃO ACEITA: {nome_pocao_final} (Máquina: {self.tipo_maquina})")
        else:
            detalhes = f"Resultado: FALHA!"
            print(f"\nPOÇÃO REJEITADA: {nome_pocao_final} (Máquina: {self.tipo_maquina})")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0) 
        self.root.grid_columnconfigure(0, weight=1)

        resultado_label = tk.Label(self.root, text=detalhes, font=("Arial", 24, "bold"), bg='white',
                                     fg='green' if resultado_simulacao == "aceita" else 'red')
        resultado_label.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        btn_voltar = tk.Button(self.root, text="VOLTAR", command=self.criar_tela_selecao_maquina, font=("Arial", 14), bg='#D3D3D3')
        btn_voltar.grid(row=1, column=0, pady=20, padx=20) 

        #limpa ingredientes selecionados APENAS se for AFD
        if self.tipo_maquina == 'AFD':
            self.limpar_ingredientes_selecionados() 
        #para MT, a entrada é apagada na função processar_entrada_mt, então não precisamos limpar aqui

    def limpar_ingredientes_selecionados(self):
        self.ingredientes_selecionados = []
        if hasattr(self, 'lista_ingredientes') and self.lista_ingredientes.winfo_exists():
            self.lista_ingredientes.delete(0, tk.END)

    def encerrar_fabricacao(self):
        self.mostrar_opcao_nova_pocao()

    def mostrar_opcao_nova_pocao(self):
        resposta = messagebox.askyesno("Finalizar Poção", "Deseja criar uma nova poção?")
        if resposta:
            self.criar_tela_selecao_maquina()
        else:
            self.root.destroy()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoDePocoes(root)
    root.mainloop()