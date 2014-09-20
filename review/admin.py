#-*- coding: utf-8 -*-
from django.contrib import admin
from review.models import *

class RevisaoAdmin(admin.ModelAdmin):
    pass
    
class CriterioAdmin(admin.ModelAdmin):
    list_display = ('sigla','descricao','revisao')
    list_filter = ('revisao__nomereduzido',)
    search_fields = ['sigla','revisao__nomereduzido']
    
class FonteAdmin(admin.ModelAdmin):
    list_display = ('sigla','nome','revisao')
    list_filter = ('sigla','revisao__nomereduzido',)
    search_fields = ['sigla','nome','revisao__nomereduzido']
    
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('sigla','descricao','revisao')
    list_filter = ('revisao__nomereduzido',)
    search_fields = ['sigla','revisao__nomereduzido']
    
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('sigla','revisao')
    list_filter = ('revisao__nomereduzido',)
    search_fields = ['sigla','texto','revisao__nomereduzido']
    
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo','selecionada','revisao')
    list_filter = ('revisao__nomereduzido','selecionada','etapa__sigla','ano')
    search_fields = ['autores','titulo','revisao__nomereduzido','selecionada']
    
class ReferenciaAdmin(admin.ModelAdmin):
    list_filter = ('publicacao__revisao__nomereduzido',)
    search_fields = ['referencia','publicacao__revisao__nomereduzido','publicacao__autores']
    
class InfoQuestaoAdmin(admin.ModelAdmin):
    list_filter = ('publicacao__revisao__nomereduzido','questao__sigla')
    search_fields = ['publicacao__revisao__nomereduzido','publicacao__autores']

class InfoEtapaAdmin(admin.ModelAdmin):
    list_filter = ('publicacao__revisao__nomereduzido','etapa__sigla')
    search_fields = ['publicacao__revisao__nomereduzido','etapa__sigla']


admin.site.register(Revisao, RevisaoAdmin)
admin.site.register(Criterio, CriterioAdmin)
admin.site.register(Fonte, FonteAdmin)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(InfoQuestao, InfoQuestaoAdmin)
admin.site.register(InfoEtapa, InfoEtapaAdmin)
