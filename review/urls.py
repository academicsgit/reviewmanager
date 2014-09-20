#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('review.views',
                       url(r'^$', 'index', name='index'),
                       #detalhamentos
                       url(r'^detalherevisao/(?P<id>\d+)/$', 'detalherevisao', name='detalherevisao'),
                       url(r'^detalhepublicacao/(?P<id>\d+)/$', 'detalhepublicacao', name='detalhepublicacao'),
                       
                       #Formularios
                       url(r'^deletar/(?P<id>\d+)/(?P<classe>\w+)/$', 'deletar', name='deletar'),
                       url(r'^adduser/$', 'adduser', name='adduser'),
                       url(r'^revisaoform/$', 'revisaoform', name='revisaoform'),
                       url(r'^addfonte/(?P<revisao>\d+)/$', 'addfonte', name='addfonte'),
                       url(r'^editfonte/(?P<fonte>\d+)/$', 'editfonte', name='editfonte'),
                       url(r'^addcriterio/(?P<revisao>\d+)/$', 'addcriterio', name='addcriterio'),
                       url(r'^editcriterio/(?P<criterio>\d+)/$', 'editcriterio', name='editcriterio'),
                       url(r'^addetapa/(?P<revisao>\d+)/$', 'addetapa', name='addetapa'),
                       url(r'^editetapa/(?P<etapa>\d+)/$', 'editetapa', name='editetapa'),
                       url(r'^addquestao/(?P<revisao>\d+)/$', 'addquestao', name='addquestao'),
                       url(r'^editquestao/(?P<questao>\d+)/$', 'editquestao', name='editquestao'),
                       url(r'^addpublicacao/(?P<revisao>\d+)/$', 'addpublicacao', name='addpublicacao'),
                       url(r'^editpublicacao/(?P<publicacao>\d+)/$', 'editpublicacao', name='editpublicacao'),
                       url(r'^addreferencia/(?P<publicacao>\d+)/$', 'addreferencia', name='addreferencia'),
                       url(r'^editreferencia/(?P<referencia>\d+)/$', 'editreferencia', name='editreferencia'),
                       url(r'^addinfoquestao/(?P<publicacao>\d+)/$', 'addinfoquestao', name='addinfoquestao'),
                       url(r'^editinfoquestao/(?P<infoquestao>\d+)/$', 'editinfoquestao', name='editinfoquestao'),
                       url(r'^importaris/(?P<revisao>\d+)/$', 'importaris', name='importaris'),
                       url(r'^filtropublicacao/(?P<revisao>\d+)/$', 'filtropublicacao', name='filtropublicacao'),
                       url(r'^filtroreferencia/(?P<revisao>\d+)/$', 'filtroreferencia', name='filtroreferencia'),
                       url(r'^addinfoetapa/(?P<publicacao>\d+)/$', 'addinfoetapa', name='addinfoetapa'),
                       url(r'^editinfoetapa/(?P<infoetapa>\d+)/$', 'editinfoetapa', name='editinfoetapa'),
                       url(r'^changeetaparevisao/(?P<revisao>\d+)/$', 'changeetaparevisao', name='changeetaparevisao'),
                       url(r'^quantcriterioetapa/(?P<revisao>\d+)/$', 'quantcriterioetapa', name='quantcriterioetapa'),
                       
                       
                       
                       
                       #Listagens
                       url(r'^fontes/(?P<revisao>\d+)/$', 'fontes', name='fontes'),
                       url(r'^criterios/(?P<revisao>\d+)/$', 'criterios', name='criterios'),
                       url(r'^etapas/(?P<revisao>\d+)/$', 'etapas', name='etapas'),
                       url(r'^questoes/(?P<revisao>\d+)/$', 'questoes', name='questoes'),
                       url(r'^publicacoes/(?P<revisao>\d+)/$', 'publicacoes', name='publicacoes'),
                       url(r'^relatorios/(?P<revisao>\d+)/$', 'relatorios', name='relatorios'),
                       url(r'^tagselecionadas/(?P<revisao>\d+)/$', 'tagselecionadas', name='tagselecionadas'),
                       
                       #Relatorios
                       url(r'^revisaoreport/(?P<revisao>\d+)/$', 'revisaoreport', name='revisaoreport'),
                       url(r'^quantitativoreport/(?P<revisao>\d+)/$', 'quantitativoreport', name='quantitativoreport'),
                       url(r'^selecionadasreport/(?P<revisao>\d+)/$', 'selecionadasreport', name='selecionadasreport'),
                       url(r'^allreport/(?P<revisao>\d+)/$', 'allreport', name='allreport'),
                       url(r'^charts/(?P<revisao>\d+)/$', 'charts', name='charts'),
                       
                       
                       )

