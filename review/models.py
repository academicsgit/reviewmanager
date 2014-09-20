#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.admin.models import User
import os


IDIOMA_CHOICES = (
             ('pt-br', u'Portugues Brasil'),
             ('en', u'Ingles'),
             ('ol',u'Outras'),
             )   

def get_publicacao_file_path(instance, filename):
    return os.path.join('publicacoes', str(instance.revisao.id), filename)


class Revisao(models.Model):
    titulo = models.CharField(u'Titulo',max_length=240, help_text=u'Titulo ou tema da revisão')
    nomereduzido = models.CharField(u'Nome reduzido',max_length=30, help_text=u'Abreviação para exibição')
    revisor = models.ForeignKey(User , null=True,blank=True)
    etapa = models.ForeignKey('Etapa' , null=True,blank=True,verbose_name=u'Etapa atual',related_name=u'revisoes')
    
    class Meta:
        abstract = False
        db_table= u'revisao'
        app_label = u'review'
        verbose_name_plural = u'Revisões'
        permissions = (
            ("pode_administrar", "Pode realizar  tarefas administrativas e gerenciais"),
        )
        
    def get_absolute_url(self):
        return '/review/revisao/%s/' % self.id
    
    def __unicode__(self):
        return u'%s' % (self.nomereduzido)
    

class Criterio(models.Model):
    sigla = models.CharField(u'Sigla',max_length=15)
    descricao = models.CharField(u'Descrição',max_length=140)
    revisao = models.ForeignKey(Revisao,null=True,blank=True)
    class Meta:
        abstract = False
        db_table= u'criterio'
        app_label = u'review'
    
    def __unicode__(self):
        return u'%s' % (self.sigla)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)

class Fonte(models.Model):
    sigla = models.CharField(u'Sigla',max_length=30)
    nome = models.CharField(u'Nome',max_length=140)
    url = models.URLField(u'Endereço', null=True,blank=True,help_text=u'Link para a base de pesquisa quando disponível')
    expressao = models.TextField(u'Expressão de busca',null=True,blank=True)
    revisao = models.ForeignKey(Revisao, null=True,blank=True)
    
    class Meta:
        abstract = False
        db_table= u'fonte'
        app_label = u'review'
    
    def __unicode__(self):
        return u'%s' % (self.nome)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)
    
class Etapa(models.Model):
    sigla = models.CharField(u'Sigla',max_length=15)
    descricao = models.CharField(u'Descrição',max_length=140)
    revisao = models.ForeignKey(Revisao ,null=True,blank=True, related_name=u'etapas')
    
    class Meta:
        abstract = False
        db_table= u'etapa'
        app_label = u'review'
    
    
    def __unicode__(self):
        return u'%s' % (self.sigla)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)
    
class Questao(models.Model):
    sigla = models.CharField(u'Sigla',max_length=15)
    texto = models.CharField(u'Texto',max_length=140)
    revisao = models.ForeignKey('Revisao',null=True,blank=True)
    
    class Meta:
        abstract = False
        db_table= u'questao'
        app_label = u'review'
        verbose_name_plural = u'Questões'
    
    def __unicode__(self):
        return u'%s' % (self.sigla)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)

class Publicacao(models.Model):
    tag = models.CharField(u'Tag',max_length=5 , help_text=u'Identificados visual da publicação',editable=False,null=True,blank=True)
    revisao = models.ForeignKey(Revisao, help_text=u'Revisão a qual esta publicação pertence',null=True,blank=True)
    titulo = models.CharField(u'Titulo',max_length=280 , help_text=u'Titulo da publicação')
    evento = models.CharField(u'Evento',max_length=280 , help_text=u'Evento onde ocorreu a publicação')
    ano = models.IntegerField(u'Ano', help_text=u'Ano de publicação')
    idioma = models.CharField(u'Idioma',max_length=50,choices=IDIOMA_CHOICES, help_text=u'Idioma da publicação')
    searchpage = models.IntegerField(u'Paginação ou índice exibido na base', default=1, help_text=u'Pagina na listagem da busca digital')
    referenciaformatada = models.CharField(u'Referência no formato ABNT',max_length=380 ,null=True,blank=True,help_text=u'Apenas revisões aprovadas para leitura completa devem ter este campo preenchido')
    resumo = models.TextField(u'Resumo',help_text=u'Durante a leitura completoa adiciona-se um resumo geral da publicação.',null=True,blank=True)
    autores = models.CharField(u'Autor(es)',max_length=380,help_text=u'Lista de autores separados por virgula')
    fonte = models.ForeignKey(Fonte ,help_text=u'Trabalhos repetidos devem ter sua fonte novamente cadastrada para fins de relatórios.')
    etapa = models.ForeignKey(Etapa ,null=True,blank=True, help_text=u'Etapa da pesquisa em que a publicação se encontra.')
    selecionada = models.BooleanField(u'Selecionada para análise qualitativa?',default=False, help_text=u'Publicações que foram selecionadas para análise detalhada')
    arquivo = models.FileField(upload_to=get_publicacao_file_path,null=True,blank=True)
    #Os objetos e relacionamentos estao acessiveis através de
    # instancia.referencia_set.all()
    # instancia.infoquestao_set.all()
    # instancia.infoetapa_set.all()
    
    class Meta:
        abstract = False
        db_table= u'publicacao'
        app_label = u'review'
        verbose_name_plural = u'Publicações'
    
    def __unicode__(self):
        return u'%s ,%s ,%s' % (self.titulo, self.ano, self.fonte)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)
    
    def is_avaliada(self):
        return self.infoetapa_set.filter(etapa=self.etapa,etapaconcluida=True).count()
    def is_excluida(self):
        return self.infoetapa_set.filter(excluidanestaetapa=True).count()
    def has_infoetapa(self,etapa):
        '''
            Retorna o par Boolean, Boolean  informando se existe infoetapa 
            sobre o parametro e se a pub. foi excluida nesta etapa
        '''
        if self.infoetapa_set.filter(etapa=etapa).count():
            info = self.infoetapa_set.filter(etapa=etapa)
            return True,info[0].excluidanestaetapa
        else:
            return False,False
            
    
class Referencia(models.Model):
    referencia = models.CharField(u'Referência',max_length=380 , help_text=u'Referência formatada contida na publicação')
    publicacao = models.ForeignKey(Publicacao ,null=True, blank=True)
    
    class Meta:
        abstract = False
        db_table= u'referencia'
        app_label = u'review'
        ordering = ['referencia']
    
    
    def __unicode__(self):
        return u'%s' % (self.referencia)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)

class InfoEtapa(models.Model):
    etapa = models.ForeignKey(Etapa ,null=True,blank=True, help_text=u'Etapa da pesquisa em que a publicação se encontra.')
    publicacao = models.ForeignKey(Publicacao ,null=True, blank=True)
    etapaconcluida = models.BooleanField(u'Etapa concluída?',default=False,help_text=u'Todas as tarefas da etapa ja foram concluídas para esta pubblicação?')
    excluidanestaetapa=models.BooleanField(u'Publicação removida da pesquisa?',default=False,help_text=u'Todas as tarefas da etapa ja') 
    criterios = models.ManyToManyField(Criterio,null=True,blank=True, help_text=u'Criterio(s) de seleção utilizado(s) na etapa')
        
    class Meta:
        abstract = False
        unique_together = (('etapa','publicacao'),) #permite apenas uma info por etapa/publicacao
        db_table= u'infoetapa'
        app_label = u'review'
        verbose_name_plural = u'Informações sobre uma etapa nesta publicação'
        verbose_name = u'Informação sobre uma etapa nesta publicação'
        ordering = ['etapa__sigla']
    
    
    def __unicode__(self):
        return u'%s' % (self.etapa.sigla)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)

    
class InfoQuestao(models.Model):
    publicacao = models.ForeignKey(Publicacao ,null=True, blank=True)
    questao = models.ForeignKey(Questao)
    classificacao = models.CharField(u'Classificação',max_length=180, help_text=u'Palavra para agrupamento nos relatórios.')
    texto = models.TextField(u'Texto')
    
    class Meta:
        abstract = False
        db_table= u'infoquestao'
        app_label = u'review'
        verbose_name_plural = u'Informações de questões por publicação'
        verbose_name = u'Informação de questões por publicação'
        ordering = ['questao__sigla']
        unique_together = (('questao','publicacao'),) #permite apenas uma info por etapa/publicacao
    
    def __unicode__(self):
        return u'%s , %s ' % (self.questao, self.publicacao)
    
    def get_class(self):
        return u'%s' % (self.__class__.__name__)
    
    
