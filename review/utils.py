import re 

class PublicacaoRSI(object):
    def __init__(self):
        self.titulo = ''
        self.evento = ''
        self.ano = ''
        self.autores = []
        self.abstract = ''

class Quantitativos(object):
    def __init__(self):
        self.etapa = ''
        self.fonte = ''
        self.total = 0
        self.excluidas = 0
        self.aprovadas = 0

class Qualitativos(object):
    def __init__(self):
        self.questao = ''
        self.classificacao = ''
        self.publicacoes = []
        

def spaces(palavra):
    palavra = palavra.rstrip()
    palavra = palavra.lstrip()
    return palavra
    


def rsiParser(arquivo=None):
    dados = []
    info = PublicacaoRSI()
    tagtitulo = [u'TI',u'T1']
    tagevento =  [u'JO',u'JA',u'BT',u'SO']
    tagano =  [u'PY',]
    tagautor = [u'A1',u'AU']
    tagabstract = [u'AB',u'N2']
    
    regspace = "\\s"    
    linhas =  arquivo.readlines()
    for linha in linhas:
        v = linha.split('-',1)
        tag = spaces(v[0])
        if tag == u'TY' or tag == u'PT': #marca o inicio de uma publicacao
             info = PublicacaoRSI()
        if tag in tagtitulo: #tags de titulo
            info.titulo = spaces(v[1])
        if tag in tagevento: #tags de envetos
            evento = spaces(v[1])
            info.evento = (evento[:150] + '..') if len(evento) > 152 else evento
        if tag in tagano: #tags de ano de publicacao
            ano = spaces(v[1])
            if len(ano.split('/')) > 1:
                ano = ano.split('/')[0]
            if ano:
                info.ano = ano
            else:
                info.ano = 0 #caso o ano de publicacao nao esteja registrado
        if tag in tagautor: #tags de autores
            if len(info.autores) < 5:
                info.autores.append(spaces(v[1]))
        if tag in tagabstract: #tags contendo o abstract
            info.abstract = spaces(v[1])
        if tag == u'ER': #marca o final de uma publicacao
            info.autores.reverse()
            dados.append(info) #adiciona os dados de uma publicacao na lista e reinicia o loop
            info = None
    return dados
                    
        
        
        
        
    