# -*- coding: utf-8 -*-
from geraldo import Report, ReportGroup, SubReport, ReportBand, landscape, Label, ObjectValue, SystemField, \
FIELD_ACTION_SUM, FIELD_ACTION_COUNT, FIELD_ACTION_SUM, BAND_WIDTH, Line, Image
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import navy, red
from reportlab.lib.pagesizes import A4, A5

import os
cur_dir = os.path.dirname(os.path.abspath(__file__))


class RevisaoReport(Report):
         title = u'REVISÃO SISTEMÁTICA - PROTOCOLO DE PESQUISA'
         author = u'Mestrado Profissional em Engenharia de Software - CESAR'
         print_if_empty = True
         # page_size = landscape(A4)
         margin_left = 2 * cm
         margin_top = 0.5 * cm
         margin_right = 0.5 * cm
         margin_bottom = 0.5 * cm
     
         class band_page_header(ReportBand):
             height = 1 * cm
             elements = [
                 SystemField(expression='%(report_title)s', top=0.2 * cm, left=0, width=BAND_WIDTH,
                     style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
                 SystemField(expression='Page # %(page_number)d of %(page_count)d', top=0.2 * cm,
                     width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
             ]
             borders = {'bottom': Line(stroke_color=navy, stroke_width=1)}
     
         class band_page_footer(ReportBand):
             height = 0.5*cm
             elements = [
                         Label(text=u'Mestrado Profissional em Engenharia de Software - C.E.S.A.R', top=0.1*cm,left=0.2*cm,width=BAND_WIDTH, style={'alignment': TA_CENTER}),
                         ]
             borders = {'top': Line(stroke_color=navy)}
     
         class band_detail(ReportBand):
             height = 2.5 * cm
             elements = [
                 Label(text=u"Título", top=0, left=0, style={'fontName': 'Helvetica-Bold', 'fontSize': 14}),
                 Label(text="Abreviação", top=1 * cm, left=0.2*cm, style={'fontName': 'Helvetica-Bold'}),
                 Label(text="Revisor", top=1.5 * cm, left=0.2 * cm, style={'fontName': 'Helvetica-Bold'}),
                 ObjectValue(attribute_name='titulo', top=0, left=4 * cm,width=14.0*cm, style={'fontName': 'Helvetica'}),
                 ObjectValue(attribute_name='nomereduzido', top=1 * cm, left=4 * cm,width=10.0*cm, style={'fontName': 'Helvetica'}),
                 ObjectValue(attribute_name='revisor.get_full_name', top=1.5 * cm, left=4 * cm,width=10.0*cm, style={'fontName': 'Helvetica'}),
             ]
             borders = {'bottom': Line(stroke_color=navy)}
     
         subreports = [
             SubReport(
                 queryset_string='%(object)s.fonte_set.all()',
                 band_header=ReportBand(
                         height=0.8 * cm,
                         elements=[
                             Label(text='FONTES', top=0*cm, left=0*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold','alignment': TA_CENTER}),
                             Label(text='Sigla', top=0.3*cm, left=0.2 * cm, style={'fontName': 'Helvetica-Bold'}),
                             Label(text=u'Nome', top=0.3*cm, left=2.5 * cm, style={'fontName': 'Helvetica-Bold'}),
                             Label(text=u'Link', top=0.3*cm, left=6.5 * cm, style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'top': True, 'left': True, 'right': True},
                     ),
                 band_detail=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='sigla', top=0*cm,width=14*cm, left=0.2 * cm),
                             ObjectValue(attribute_name='nome', top=0*cm,width=14*cm, left=2.5 * cm),
                             ObjectValue(attribute_name='url', top=0*cm,width=14*cm, left=6.5 * cm),
                         ],
                         borders={'left': True, 'right': True},
                     ),
                 band_footer=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='id', top=0.1*cm,left=4 * cm,action=FIELD_ACTION_COUNT, display_format='%s fontes(s) encontrada(s).',
                                 style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'bottom': True, 'left': True, 'right': True},
                     ),
             ),
            SubReport(
                 queryset_string='%(object)s.etapas.all()',
                 band_header=ReportBand(
                         height=0.8 * cm,
                         elements=[
                             Label(text='ETAPAS', top=0, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold','alignment': TA_CENTER}),
                             Label(text='Sigla', top=0.2*cm, left=0.2 * cm, style={'fontName': 'Helvetica-Bold'}),
                             Label(text=u'Descrição', top=0.2*cm, left=2.5 * cm, style={'fontName': 'Helvetica-Bold','wordWrap':True}),
                         ],
                         borders={'top': True, 'left': True, 'right': True},
                     ),
                 band_detail=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='sigla', top=0,width=14*cm, left=0.2 * cm),
                             ObjectValue(attribute_name='descricao', top=0,width=16*cm, left=2.5 * cm, style={'wordWrap':True}),
                         ],
                         borders={'left': True, 'right': True},
                     ),
                 band_footer=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='id', left=4 * cm, \
                                 action=FIELD_ACTION_COUNT, display_format='%s etapa(s) encontrada(s).',
                                 style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'bottom': True, 'left': True, 'right': True},
                     ),
             ),
            SubReport(
                 queryset_string='%(object)s.criterio_set.all()',
                 band_header=ReportBand(
                         height=0.8 * cm,
                         elements=[
                             Label(text=u'CRITÉRIOS DE SELEÇÃO', top=0, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold','alignment': TA_CENTER}),
                             Label(text='Sigla', top=0.2*cm, left=0.2 * cm, style={'fontName': 'Helvetica-Bold'}),
                             Label(text=u'Descrição', top=0.2*cm, left=2.5 * cm, style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'top': True, 'left': True, 'right': True},
                     ),
                 band_detail=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='sigla', top=0,width=14*cm, left=0.2 * cm),
                             ObjectValue(attribute_name='descricao', top=0,width=16*cm, left=2.5 * cm, style={'wordWrap':True}),
                         ],
                         borders={'left': True, 'right': True},
                     ),
                 band_footer=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='id', left=4 * cm, \
                                 action=FIELD_ACTION_COUNT, display_format='%s Criterio(s) encontrado(s).',
                                 style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'bottom': True, 'left': True, 'right': True},
                     ),
             ),
            SubReport(
                 queryset_string='%(object)s.questao_set.all()',
                 band_header=ReportBand(
                         height=0.8 * cm,
                         elements=[
                             Label(text=u'QUESTÕES', top=0, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold','alignment': TA_CENTER}),
                             Label(text='Sigla', top=0.2*cm, left=0.2 * cm, style={'fontName': 'Helvetica-Bold'}),
                             Label(text=u'Texto', top=0.2*cm, left=2.5 * cm, style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'top': True, 'left': True, 'right': True},
                     ),
                 band_detail=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='sigla', top=0,width=14*cm, left=0.2 * cm),
                             ObjectValue(attribute_name='texto', top=0,width=16*cm, left=2.5 * cm, style={'wordWrap':True}),
                         ],
                         borders={'left': True, 'right': True},
                     ),
                 band_footer=ReportBand(
                         height=0.5 * cm,
                         elements=[
                             ObjectValue(attribute_name='id', left=4 * cm, \
                                 action=FIELD_ACTION_COUNT, display_format='%s item(s) encontrado(s).',
                                 style={'fontName': 'Helvetica-Bold'}),
                         ],
                         borders={'bottom': True, 'left': True, 'right': True},
                     ),
             ),
         ]
                
                
