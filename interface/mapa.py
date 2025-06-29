import os

MAPA_INGREDIENTES_SIMBOLOS = {
    "aconito": "ac", 
    "alcohest": "ah", 
    "cerebroafogador": "caf", 
    "cogumeloesgoto": "ce", 
    "essenciatrevas": "et",
    "folhascicuta": "fpc",
    "gaivotabranca": "gb",
    "olhocorvo": "oc", 
    "pastaalquimica": "pa", 
    "raizmandragora": "rm", 
    "verbena": "vb",
    "petalasmurtabranca": "pmb", 
    "quelidonia": "q",
    "salitre": "sa",
    "vitriol": "vi",
    "cortinarius": "co",
    "bryonia": "br",
    "azufre": "az", 
    }

MAPA_POCOES_ARQUIVOS = {
    #afd
    "Andorinha": os.path.join("receitas", "andorinha.txt"),
    "Coruja do mato": os.path.join("receitas", "corujadomato.txt"),
    "Lua Cheia": os.path.join("receitas", "luacheia.txt"), 

    #apd
    "Trovoada": os.path.join("receitas", "trovoada.txt"),
    "Gato": os.path.join("receitas", "gato.txt"),
    "Pocao de Troll": os.path.join("receitas", "pocaodetroll.txt"),

    #moore
    "Bomba-Fungo Demoniaco": os.path.join("receitas", "bombafungodemoniaco.txt"),
    "Bomba-Samum": os.path.join("receitas", "bombasamum.txt"),

    #mealy
    "Oleo Espectral": os.path.join("receitas", "oleoespectral.txt"),
    "Oleo de Fera": os.path.join("receitas", "oleodefera.txt"),

    #turing
    "MT Runas": os.path.join("receitas", "runas.txt"),
}

#mapeamento de poções por tipo de máquina para o filtro na GUI
MAPA_TIPO_MAQUINA_POCOES = {
    'AFD': ["Andorinha", "Coruja do mato", "Lua Cheia"],
    'APD': ["Trovoada", "Gato", "Pocao de Troll"],
    'MOORE': ["Bomba-Fungo Demoniaco", "Bomba-Samum"],
    'MEALY': ["Oleo Espectral", "Oleo de Fera"],
    'MT': ["MT Runas"]
}

#esta função é chamada pelo interface.py para obter o caminho de um arquivo de poção
def selecionarPocao(nome_pocao: str) -> str:
    """
    Retorna o caminho relativo do arquivo da máquina para a poção selecionada.
    """
    return MAPA_POCOES_ARQUIVOS.get(nome_pocao, None)