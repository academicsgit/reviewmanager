#-*- coding: utf-8 -*-
from review.models import *
from review.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.utils import IntegrityError
import csv #para uploads de dados
from django.contrib.auth import login, authenticate
from django.core import serializers #Utilizado para serializacao de modelos diretamente
import json #utilizado para serializacao de qualquer objeto ou tupla
#import de relatorios
from geraldo.generators import PDFGenerator
from review.reports import *
import datetime
from review.utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count, Min, Max

#Graficos 
from review.highcharts import PieChart, ColumnChart, GroupedColumnChart


#Listagens
@login_required
def index(request):
    revisoes = Revisao.objects.filter(revisor=request.user).order_by('-id')
    return render_to_response('home.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def fontes(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    fontes = Fonte.objects.filter(revisao=revisao).order_by('nome')
    return render_to_response('review/fontes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def criterios(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    criterios = Criterio.objects.filter(revisao=revisao).order_by('sigla')
    return render_to_response('review/criterios.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required
def etapas(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    etapas = Etapa.objects.filter(revisao=revisao).order_by('sigla')
    return render_to_response('review/etapas.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required
def questoes(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    questoes = Questao.objects.filter(revisao=revisao).order_by('sigla')
    return render_to_response('review/questoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def publicacoes(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    exibir = 100
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    page = request.GET.get('page')
    if revisao.etapa:
        publicacoes = Publicacao.objects.filter(revisao=revisao,etapa=revisao.etapa).order_by('titulo')
    else:
        publicacoes = Publicacao.objects.filter(revisao=revisao).order_by('titulo')
    
    paginator = Paginator(publicacoes,exibir)
    try:
        publicacoes = paginator.page(page)
    except PageNotAnInteger:
        publicacoes = paginator.page(1)
    except EmptyPage:
        publicacoes = paginator.page(paginator.num_pages)
        
    avaliadas = 0
    for p in publicacoes:
        if p.is_avaliada():
            avaliadas = avaliadas + 1
    
    return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )



@login_required
def filtropublicacao(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    page = request.GET.get('page')
    exibir = 1000
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    if request.method == 'POST':
        form = PublicacaoFiltroForm(request.POST)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        if form.is_valid():
            publicacao = form.cleaned_data['publicacao']
            ano = form.cleaned_data['ano']
            byetapa = form.cleaned_data['byetapa']
            byfonte = form.cleaned_data['byfonte']
            selecionada = form.cleaned_data['selecionada']
            etapa = form.cleaned_data['etapa']
            fonte = form.cleaned_data['fonte']
            #dosomething
            if publicacao:
                publicacoes = Publicacao.objects.filter(revisao=revisao,titulo__icontains=publicacao).order_by('titulo')
                paginator = Paginator(publicacoes,exibir)
                try:
                    publicacoes = paginator.page(page)
                except PageNotAnInteger:
                    publicacoes = paginator.page(1)
                except EmptyPage:
                    publicacoes = paginator.page(paginator.num_pages)
                
                avaliadas = 0
                for p in publicacoes:
                    if p.is_avaliada():
                        avaliadas = avaliadas + 1
                return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            if byetapa:
                if byfonte:
                    publicacoes = Publicacao.objects.filter(revisao=revisao,etapa=etapa,fonte=fonte).order_by('titulo')
                    paginator = Paginator(publicacoes,exibir)
                    try:
                        publicacoes = paginator.page(page)
                    except PageNotAnInteger:
                        publicacoes = paginator.page(1)
                    except EmptyPage:
                        publicacoes = paginator.page(paginator.num_pages)
                
                    avaliadas = 0
                    for p in publicacoes:
                        if p.is_avaliada():
                            avaliadas = avaliadas + 1
                    return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
                else:
                    publicacoes = Publicacao.objects.filter(revisao=revisao,etapa=etapa).order_by('titulo')
                    paginator = Paginator(publicacoes,exibir)
                    try:
                        publicacoes = paginator.page(page)
                    except PageNotAnInteger:
                        publicacoes = paginator.page(1)
                    except EmptyPage:
                        publicacoes = paginator.page(paginator.num_pages)
                    
                    avaliadas = 0
                    for p in publicacoes:
                        if p.is_avaliada():
                            avaliadas = avaliadas + 1
                    return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            if byfonte:
                publicacoes = Publicacao.objects.filter(revisao=revisao,fonte=fonte).order_by('titulo')
                paginator = Paginator(publicacoes,exibir)
                try:
                    publicacoes = paginator.page(page)
                except PageNotAnInteger:
                    publicacoes = paginator.page(1)
                except EmptyPage:
                    publicacoes = paginator.page(paginator.num_pages)
                avaliadas = 0
                for p in publicacoes:
                    if p.is_avaliada():
                        avaliadas = avaliadas + 1
                return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            if selecionada:
                if ano:
                    publicacoes = Publicacao.objects.filter(revisao=revisao,selecionada=True,ano=ano).order_by('titulo')
                else:
                    publicacoes = Publicacao.objects.filter(revisao=revisao,selecionada=True).order_by('titulo')
                paginator = Paginator(publicacoes,exibir)
                try:
                    publicacoes = paginator.page(page)
                except PageNotAnInteger:
                    publicacoes = paginator.page(1)
                except EmptyPage:
                    publicacoes = paginator.page(paginator.num_pages)
                avaliadas = 0
                for p in publicacoes:
                    if p.is_avaliada():
                        avaliadas = avaliadas + 1
                return render_to_response('review/selecionadas.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            
            if ano:
                publicacoes = Publicacao.objects.filter(revisao=revisao,ano=ano).order_by('titulo')
                paginator = Paginator(publicacoes,exibir)
                try:
                    publicacoes = paginator.page(page)
                except PageNotAnInteger:
                    publicacoes = paginator.page(1)
                except EmptyPage:
                    publicacoes = paginator.page(paginator.num_pages)
                
                avaliadas = 0
                for p in publicacoes:
                    if p.is_avaliada():
                        avaliadas = avaliadas + 1
                return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            
            #Método catch all
            publicacoes = Publicacao.objects.filter(revisao=revisao).order_by('titulo')
            paginator = Paginator(publicacoes,exibir)
            try:
                publicacoes = paginator.page(page)
            except PageNotAnInteger:
                publicacoes = paginator.page(1)
            except EmptyPage:
                publicacoes = paginator.page(paginator.num_pages)
            avaliadas = 0
            for p in publicacoes:
                if p.is_avaliada():
                    avaliadas = avaliadas + 1
    
            return render_to_response('review/publicacoes.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    else:
        form = PublicacaoFiltroForm()
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        publicacoes = Publicacao.objects.filter(revisao=revisao).order_by('fonte__sigla','titulo','etapa__sigla','selecionada')
        paginator = Paginator(publicacoes,exibir)
        try:
            publicacoes = paginator.page(page)
        except PageNotAnInteger:
            publicacoes = paginator.page(1)
        except EmptyPage:
            publicacoes = paginator.page(paginator.num_pages)
    return render_to_response('review/filtropublicacao.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def filtroreferencia(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    if request.method == 'POST':
        form = ReferenciaFiltroForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            tags =  tags.split(";")
            referencias = Referencia.objects.filter(publicacao__revisao=revisao,publicacao__tag__in=tags).order_by('referencia')
            referencias =  sorted(referencias)
            return render_to_response('review/filtroreferencia.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    else:
        form = ReferenciaFiltroForm()
        
    return render_to_response('review/filtroreferencia.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )


@login_required
def relatorios(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    return render_to_response('review/relatorios.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )



@login_required
def deletar(request, id=None, classe=None):
    if classe == u'Fonte':
        fonte = get_object_or_404(Fonte, id=id)
        if fonte.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            fonte.delete()
            return HttpResponseRedirect(reverse('review:fontes',kwargs={'revisao':fonte.revisao.id }))
        
    if classe == u'Criterio':
        criterio = get_object_or_404(Criterio, id=id)
        if criterio.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            criterio.delete()
            return HttpResponseRedirect(reverse('review:criterios',kwargs={'revisao':fonte.revisao.id }))
        
    if classe == u'Etapa':
        etapa = get_object_or_404(Etapa, id=id)
        if etapa.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            etapa.delete()
            return HttpResponseRedirect(reverse('review:etapas',kwargs={'revisao':etapa.revisao.id }))
        
    if classe == u'Questao':
        questao = get_object_or_404(Questao, id=id)
        if questao.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            questao.delete()
            return HttpResponseRedirect(reverse('review:questoes',kwargs={'revisao':questao.revisao.id }))
    if classe == u'Publicacao':
        publicacao = get_object_or_404(Publicacao, id=id)
        if publicacao.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            publicacao.delete()
            return HttpResponseRedirect(reverse('review:publicacoes',kwargs={'revisao':publicacao.revisao.id }))
    
    if classe == u'Referencia':
        referencia = get_object_or_404(Referencia, id=id)
        if referencia.publicacao.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            referencia.delete()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':referencia.publicacao.id }))
    
    if classe == u'InfoQuestao':
        infoquestao = get_object_or_404(InfoQuestao, id=id)
        if infoquestao.publicacao.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            infoquestao.delete()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':infoquestao.publicacao.id }))
    
    if classe == u'InfoEtapa':
        infoetapa = get_object_or_404(InfoEtapa, id=id)
        if infoetapa.publicacao.revisao.revisor != request.user:
            mensagens.add("Informações não pertecentes ao usuário logado!");
            return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
        else:
            infoetapa.delete()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':infoetapa.publicacao.id }))
        
        

#Fornularios    
def adduser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u = form.save()
            #Autentica o usuario criado
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('review:index'))
            # Do something else.
            
    else:
        form = UserCreationForm()
    #acao catch all    
    return render_to_response('review/userform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def revisaoform(request):
    if request.method == "POST":
        form = RevisaoForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.revisor = request.user
            r.save()
            return HttpResponseRedirect(reverse('review:index'))
            
    else:
        form = RevisaoForm()
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def changeetaparevisao(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = ChangeEtapaRevisaoForm(request.POST, instance=revisao)
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        if form.is_valid():
            f = form.save()
            publicacoes = Publicacao.objects.filter(revisao=revisao)
            for p in publicacoes:
                if p.is_excluida():
                    pass
                else:
                    p.etapa = f.etapa
                    p.save()
            #fim do for
            return HttpResponseRedirect(reverse('review:publicacoes',kwargs={'revisao':revisao.id }))
            
    else:
        form = ChangeEtapaRevisaoForm(instance=revisao)
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required    
def addfonte(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = FonteForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.revisao = revisao
            f.save()
            return HttpResponseRedirect(reverse('review:fontes',kwargs={'revisao':revisao.id }))
            
    else:
        form = FonteForm()
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editfonte(request,fonte=None):
    fonte = get_object_or_404(Fonte, id=fonte)
    if fonte.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = FonteForm(request.POST, instance=fonte)
        if form.is_valid():
            f = form.save(commit=False)
            f.revisao = fonte.revisao
            f.save()
            return HttpResponseRedirect(reverse('review:fontes',kwargs={'revisao':fonte.revisao.id }))
            
    else:
        form = FonteForm(instance=fonte)
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addcriterio(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = CriterioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.revisao = revisao
            c.save()
            return HttpResponseRedirect(reverse('review:criterios',kwargs={'revisao':revisao.id }))
            
    else:
        form = CriterioForm()
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editcriterio(request,criterio=None):
    criterio = get_object_or_404(Criterio, id=criterio)
    if criterio.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = CriterioForm(request.POST, instance=criterio)
        if form.is_valid():
            c = form.save(commit=False)
            c.revisao = criterio.revisao
            c.save()
            return HttpResponseRedirect(reverse('review:criterios',kwargs={'revisao':criterio.revisao.id }))
            
    else:
        form = CriterioForm(instance=criterio)
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addetapa(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = EtapaForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            e.revisao = revisao
            e.save()
            return HttpResponseRedirect(reverse('review:etapas',kwargs={'revisao':revisao.id }))
            
    else:
        form = EtapaForm()
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editetapa(request,etapa=None):
    etapa = get_object_or_404(Etapa, id=etapa)
    if etapa.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = EtapaForm(request.POST, instance=etapa)
        if form.is_valid():
            e = form.save(commit=False)
            e.revisao = etapa.revisao
            e.save()
            return HttpResponseRedirect(reverse('review:etapas',kwargs={'revisao':etapa.revisao.id }))
            
    else:
        form = EtapaForm(instance=etapa)
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addquestao(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = QuestaoForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.revisao = revisao
            q.save()
            return HttpResponseRedirect(reverse('review:questoes',kwargs={'revisao':revisao.id }))
            
    else:
        form = QuestaoForm()
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editquestao(request,questao=None):
    questao = get_object_or_404(Questao, id=questao)
    if questao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = QuestaoForm(request.POST, instance=questao)
        if form.is_valid():
            q = form.save(commit=False)
            q.revisao = questao.revisao
            q.save()
            return HttpResponseRedirect(reverse('review:questoes',kwargs={'revisao':questao.revisao.id }))
            
    else:
        form = QuestaoForm(instance=questao)
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addpublicacao(request, revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = PublicacaoForm(request.POST)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        
        if form.is_valid():
            p = form.save(commit=False)
            p.revisao = revisao
            p.save()
            return HttpResponseRedirect(reverse('review:publicacoes',kwargs={'revisao':revisao.id }))
            
    else:
        form = PublicacaoForm()
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editpublicacao(request,publicacao=None):
    publicacao = get_object_or_404(Publicacao, id=publicacao)
    if publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = PublicacaoForm(request.POST,request.FILES,instance=publicacao)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        if form.is_valid():
            p = form.save(commit=False)
            p.revisao = publicacao.revisao
            p.tag = publicacao.tag
            #p.arquivo =  request.FILES['arquivo']
            p.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':publicacao.id }))
            
    else:
        form = PublicacaoForm(instance=publicacao)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addreferencia(request, publicacao=None):
    publicacao = get_object_or_404(Publicacao, id=publicacao)
    if publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = ReferenciaForm(request.POST)
        form.fields['publicacao'].required = False
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=publicacao.revisao).order_by('titulo')
        
        if form.is_valid():
            r = form.save(commit=False)
            r.publicacao = publicacao
            r.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':r.publicacao.id }))
            
    else:
        form = ReferenciaForm()
        form.fields['publicacao'].required = False
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=publicacao.revisao).order_by('titulo')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editreferencia(request,referencia=None):
    referencia = get_object_or_404(Referencia, id=referencia)
    if referencia.publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = ReferenciaForm(request.POST, instance=referencia)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=referencia.publicacao.revisao).order_by('titulo')
        if form.is_valid():
            r = form.save(commit=False)
            r.publicacao = referencia.publicacao
            r.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':r.publicacao.id }))
            
    else:
        form = ReferenciaForm(instance=referencia)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=referencia.publicacao.revisao).order_by('titulo')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required    
def addinfoquestao(request, publicacao=None):
    publicacao = get_object_or_404(Publicacao, id=publicacao)
    if publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = InfoQuestaoForm(request.POST)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=publicacao.revisao).order_by('titulo')
        form.fields['questao'].queryset = Questao.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        
        if form.is_valid():
            i = form.save(commit=False)
            i.publicacao = publicacao
            i.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
            
    else:
        form = InfoQuestaoForm()
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=publicacao.revisao).order_by('titulo')
        form.fields['questao'].queryset = Questao.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editinfoquestao(request,infoquestao=None):
    infoquestao = get_object_or_404(InfoQuestao, id=infoquestao)
    if infoquestao.publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = InfoQuestaoForm(request.POST, instance=infoquestao)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=infoquestao.publicacao.revisao).order_by('titulo')
        form.fields['questao'].queryset = Questao.objects.filter(revisao=infoquestao.publicacao.revisao).order_by('sigla')
        if form.is_valid():
            i = form.save(commit=False)
            i.publicacao = infoquestao.publicacao
            i.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
            
    else:
        form = InfoQuestaoForm(instance=infoquestao)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=infoquestao.publicacao.revisao).order_by('titulo')
        form.fields['questao'].queryset = Questao.objects.filter(revisao=infoquestao.publicacao.revisao).order_by('sigla')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def addinfoetapa(request, publicacao=None):
    publicacao = get_object_or_404(Publicacao, id=publicacao)
    if publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    if request.method == "POST":
        form = InfoEtapaForm(request.POST)
        if form.is_valid():
            i = form.save()
            i.publicacao = publicacao
            i.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
        else:
            form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('titulo')
            form.fields['etapa'].queryset = Etapa.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
            form.fields['criterios'].queryset = Criterio.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
            
    else:
        form = InfoEtapaForm()
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=publicacao.revisao).order_by('titulo')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        form.fields['criterios'].queryset = Criterio.objects.filter(revisao=publicacao.revisao).order_by('sigla')
        
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
@login_required    
def editinfoetapa(request,infoetapa=None):
    infoetapa = get_object_or_404(InfoEtapa, id=infoetapa)
    if infoetapa.publicacao.revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    if request.method == "POST":
        form = InfoEtapaForm(request.POST, instance=infoetapa)
        if form.is_valid():
            i = form.save()
            i.publicacao = infoetapa.publicacao
            i.save()
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
        else:
            form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('titulo')
            form.fields['etapa'].queryset = Etapa.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
            form.fields['criterios'].queryset = Criterio.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
            return HttpResponseRedirect(reverse('review:detalhepublicacao',kwargs={'id':i.publicacao.id }))
        
            
            
    else:
        form = InfoEtapaForm(instance=infoetapa)
        form.fields['publicacao'].queryset = Publicacao.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('titulo')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
        form.fields['criterios'].queryset = Criterio.objects.filter(revisao=infoetapa.publicacao.revisao).order_by('sigla')
        
    #acao catch all    
    return render_to_response('review/objectform.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )


@login_required
def importaris(request, revisao=None):
    '''
     Importador de publicações no formato RIS
    '''
    mensagens = []
    contador = 0
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    
    if request.method == 'POST':
        form = ImportaRISForm(request.POST, request.FILES)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        
        if form.is_valid():
            fonte = form.cleaned_data['fonte']
            etapa = form.cleaned_data['etapa']
            arquivo = request.FILES['arquivo']
            informacoes = rsiParser(arquivo)
            obtidos = len(informacoes)
            for info in informacoes:
                autores = ""
                for a in info.autores:
                    autores = a + ";" + autores
                p = Publicacao(revisao=revisao, titulo = info.titulo,
                                   evento = info.evento, ano = info.ano,resumo = info.abstract,
                                   idioma = u'en', fonte = fonte, etapa = etapa,
                                   autores = autores)
                try:
                    p.save()
                    contador =  contador + 1
                except:
                    mensagens.append("Ocorreu um erro de processamento do titulo %s na seguinte linha do arquivo: %s" % (contador,p.titulo))
                    return render_to_response('review/mensagem.html',mensagens,context_instance=RequestContext(request))
                    
                    
            return HttpResponseRedirect(reverse('review:publicacoes',kwargs={'revisao':revisao.id }))
            
            
    else:
        form = ImportaRISForm()
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
    return render_to_response('review/objectform.html', locals(),
                              context_instance=RequestContext(request)
                              )


@login_required
def quantcriterioetapa(request, revisao=None):
    '''
     Quantitativo de criterio por etapa
    '''
    mensagens = []
    contador = 0
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Informações não pertecentes ao usuário logado!");
        return render_to_response('review/mensagem.html',locals(),context_instance=RequestContext(request))
    
    if request.method == 'POST':
        form = QuantCriterioEtapaForm(request.POST)
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
        
        if form.is_valid():
            etapa = form.cleaned_data['etapa']
            fonte = form.cleaned_data['fonte']
            #grafico3 
            series = []
            criterios = list(revisao.criterio_set.all().values_list('sigla', flat=True))
            for c in criterios:
                series.append([
                                c,
                                InfoEtapa.objects.filter(publicacao__revisao=revisao,publicacao__fonte=fonte, etapa=etapa).filter(criterios__sigla=c).count(),
                                ])
            
            grafico = PieChart('grafico', title= u'Aplicação de Critérios de Seleção por fonte/etapa',
                                subtitle=u'Obs: Pode ser aplicado mais de um critério por publicação/etapa', data = series)
            
            return render_to_response('review/quantcriterioetapa.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
            
    else:
        form = QuantCriterioEtapaForm()
        form.fields['fonte'].queryset = Fonte.objects.filter(revisao=revisao).order_by('sigla')
        form.fields['etapa'].queryset = Etapa.objects.filter(revisao=revisao).order_by('sigla')
    return render_to_response('review/objectform.html', locals(),
                              context_instance=RequestContext(request)
                              )




#Detalhamentos
@login_required
def detalherevisao(request,id=None):
    mensagens = []
    revisao = get_object_or_404(Revisao, id=id)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    return render_to_response('review/detalherevisao.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required    
def detalhepublicacao(request,id=None):
    mensagens = []
    publicacao = get_object_or_404(Publicacao, id=id)
    if publicacao.revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    return render_to_response('review/detalhepublicacao.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    

def tagselecionadas(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    publicacoes =  Publicacao.objects.filter(revisao=revisao,selecionada=True).order_by('titulo')
    i = 1
    for p in publicacoes:
        p.tag = "S%s" %(i)
        p.save()
        i = i + 1
    return render_to_response('review/selecionadas.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

#Relatorios
@login_required
def selecionadasreport(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    publicacoes =  Publicacao.objects.filter(revisao=revisao,selecionada=True).order_by('titulo')
    return render_to_response('review/selecionadas.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
@login_required
def charts(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    #Monta uma tabela manualmente
    quantitativos = []
    publicacoes =  Publicacao.objects.filter(revisao=revisao).order_by('titulo')
    for e in revisao.etapas.all():
        for f in revisao.fonte_set.all().order_by('sigla'):
            publicacoesfonte = Publicacao.objects.filter(revisao=revisao,fonte=f)
            quantidade = 0
            excluidas = 0
            info = Quantitativos()
            info.etapa = e.sigla
            info.fonte = f.sigla
            for p in publicacoesfonte:
                inf1,inf2 = p.has_infoetapa(e)
                if inf1:
                    quantidade = quantidade + 1
                if inf2:
                    excluidas = excluidas +1
                info.total = quantidade
                info.excluidas = excluidas
                info.aprovadas = quantidade - excluidas
            quantitativos.append(info)
        #endfor interno
    #endforexterno
    
    #monta a tabela de classificacoes para analise quantitativa
    classificacoes = []
    selecionadas = Publicacao.objects.filter(revisao=revisao,selecionada=True).order_by('titulo')
    questoes = revisao.questao_set.all()
    for q in questoes:
        agrupamentos = list(InfoQuestao.objects.filter(publicacao__revisao=revisao,publicacao__selecionada=True,questao=q).values_list('classificacao', flat=True))
        agrupamentos = set(agrupamentos) #remove duplicatas
        for a in agrupamentos:
            infoquestao = Qualitativos()
            infoquestao.questao = q.sigla
            infoquestao.classificacao = a
            pubs = InfoQuestao.objects.filter(publicacao__revisao=revisao,publicacao__selecionada=True,questao=q,classificacao=a)
            for p in pubs:
                infoquestao.publicacoes.append(p.publicacao.tag)
            classificacoes.append(infoquestao)
        
        
    
    
    #Monta os dados para geracao dos graficos via hightcharts
    #grafico1
    series1 = []
    bases = list(revisao.fonte_set.all().values_list('nome', flat=True))
    for b in bases:
        series1.append([
            b, 
            Publicacao.objects.filter(revisao=revisao,fonte__nome=b).count()])
        
    #grafico2
    series2 = []
    etapas = list(revisao.etapas.all().values_list('sigla', flat=True))
    for e in etapas:
        series2.append([
                e, 
                InfoEtapa.objects.filter(publicacao__revisao=revisao,etapa__sigla=e,excluidanestaetapa=True).count(),
                InfoEtapa.objects.filter(publicacao__revisao=revisao,etapa__sigla=e,excluidanestaetapa=False).count(),
            ])
    
    #grafico3    
    series3 = []
    criterios = list(revisao.criterio_set.all().values_list('sigla', flat=True))
    for c in criterios:
        series3.append([
            c,
            InfoEtapa.objects.filter(publicacao__revisao=revisao).filter(criterios__sigla=c).count(), 
            ])
    
    #grafico4
    series4 = []
    questoes = list(revisao.questao_set.all().values_list('sigla', flat=True))
    for q in questoes:
        series4.append([
            q,
            InfoQuestao.objects.filter(publicacao__revisao=revisao,publicacao__selecionada=True,questao__sigla=q).exclude(classificacao=u'N/A').count(), 
            ])
        
    #grafico5
    series5 = []
    anos = list(Publicacao.objects.filter(revisao=revisao,selecionada=True).values_list('ano', flat=True))
    anos = sorted(set(anos))
    for a in anos:
        series5.append([
            str(a), 
            Publicacao.objects.filter(revisao=revisao,selecionada=True,ano=a).count()])
    
    #Cria o objeto dos graficos
    grafico1 = PieChart('grafico1', title= u'Publicações por fonte de Pesquisa', 
        subtitle=u'Total geral de publicações agrupadas por fonte de pesquisa', data = series1)
    
    
    grafico2 = GroupedColumnChart('grafico2', 
            title=u'Exclusões totais por Etapa',
            subtitle = u'Contabilizando as exclusões por etapa em todas as fontes de pesquisa',
            data = series2, groups=['Excluidas', 'Aprovadas']
        )
    
    grafico3 = PieChart('grafico3', title= u'Aplicação de Critérios de Seleção', 
        subtitle=u'Critérios de Seleção de acordo com Protocolo de Pesquisa', data = series3)
    
    grafico4 = PieChart('grafico4',
        title  = u'Respostas das questões de Pesquisa nas Publicações selecionadas',
        subtitle = u'Contabilizando as publicações que responderam a uma determinada questão de pesquisa',
        data = series4
    )
    
    grafico5 = PieChart('grafico5',
        title  = u'Selecionadas para análise qualitativa por ano de publicação',
        subtitle = u'Contabilizando as publicações selecionadas após filtragens por ano de publicação',
        data = series5
    )
    
    #Monta uma lista de graficos a ser renderizado no template
    graficos = [grafico1,grafico2, grafico3,grafico4,grafico5]
    
    return render_to_response('review/charts.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def allreport(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    publicacoes =  Publicacao.objects.filter(revisao=revisao).order_by('titulo')
    return render_to_response('review/allreport.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )

@login_required
def quantitativoreport(request,revisao=None):
    revisao = get_object_or_404(Revisao, id=revisao)
    quantitativos = []
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    publicacoes =  Publicacao.objects.filter(revisao=revisao)
    for e in revisao.etapas.all():
        for f in revisao.fonte_set.all().order_by('sigla'):
            publicacoesfonte = Publicacao.objects.filter(revisao=revisao,fonte=f)
            quantidade = 0
            excluidas = 0
            info = Quantitativos()
            info.etapa = e.sigla
            info.fonte = f.sigla
            for p in publicacoesfonte:
                inf1,inf2 = p.has_infoetapa(e)
                if inf1:
                    quantidade = quantidade + 1
                if inf2:
                    excluidas = excluidas +1
                info.total = quantidade
                info.excluidas = excluidas
                info.aprovadas = quantidade - excluidas
            quantitativos.append(info)
        #endfor interno
    #endforexterno
    return render_to_response('review/quantitativos.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    

def revisaoreport(request,revisao=None):
    reportpdf = HttpResponse(mimetype='application/pdf')
    revisao = get_object_or_404(Revisao, id=revisao)
    if revisao.revisor != request.user:
        mensagens.add("Revisão não pertecente ao usuário logado!");
        return render_to_response('review/mensagem.html', 
                              locals(),
                              context_instance=RequestContext(request)
                              )
    
    revisoes = Revisao.objects.filter(id=revisao.id)
    report = RevisaoReport(queryset=revisoes)
    report.generate_by(PDFGenerator, filename=reportpdf)
    return reportpdf


    

