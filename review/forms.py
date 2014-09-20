#-*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import Textarea
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from review.models import *
from captcha.fields import CaptchaField

#FILESIZE
from django.template.defaultfilters import filesizeformat

CONTENT_TYPES = ['pdf','jpeg','png'] #pegar o final ex: application/pdf ou  image/gif
#2.5MB - 2621440
#5MB - 5242880
MAX_UPLOAD_SIZE = 1572864 # 1024 * 1024 * 1.5

class ImportaRISForm(forms.Form):
    fonte = forms.ModelChoiceField(label=u'Fonte',queryset=None,
                               required=False,
                               help_text=u'Fonte de busca.'
                               )
    etapa = forms.ModelChoiceField(label=u'Etapa',queryset=None,
                               required=False,
                               help_text=u'Etapa em que as publicações irão ingressar.'
                               )
    arquivo =  forms.FileField(label=u'Arquivo no formato (ISI - RIS)',max_length=250, help_text='Arquivo RIS contendo publicações.',required=True)


class QuantCriterioEtapaForm(forms.Form):
    fonte = forms.ModelChoiceField(label=u'Fonte',queryset=None,
                               required=True,
                               help_text=u'Fonte de pesquisa.'
                               )
    etapa = forms.ModelChoiceField(label=u'Etapa',queryset=None,
                               required=True,
                               help_text=u'Etapa em que as publicações irão ingressar.'
                               )

class PublicacaoFiltroForm(forms.Form):
    publicacao =  forms.CharField(label=u'Titulo',max_length=100,
                                  required=False,help_text='Titulo ou parte dele, ex: Jur ')
    
    ano = forms.IntegerField(label=u'Ano',required=False,help_text='Filtrar por ano')
    
    byetapa = forms.BooleanField(label=u'Filtrar por etapa ?',
                                   required=False,
                                   help_text=u'Selecione se desejar filtrar por etapa de pesquisa.'
                                   )
    byfonte = forms.BooleanField(label=u'Filtrar por base de pesquisa?',
                                   required=False,
                                   help_text=u'Selecione se desejar filtrar por base de pesquisa.'
                                   )
    selecionada = forms.BooleanField(label=u'Apenas selecionadas após todas as estapas?',
                                   required=False,
                                   help_text=u'Selecione se desejar filtrar apenas as selecionadas após todos os critérios.'
                                   )
    etapa = forms.ModelChoiceField(label=u'Etapa',queryset=None,
                               required=False,
                               help_text=u'Esta seleção só é valida quando primeiro combo, estiver marcado.'
                               )
    fonte = forms.ModelChoiceField(label=u'Fonte de pesquisa',queryset=None,
                               required=False,
                               help_text=u'Esta seleção só é valida quando o segundo combo, estiver marcado.'
                               )


class ReferenciaFiltroForm(forms.Form):
    tags =  forms.CharField(label=u'Identificadores',max_length=250,
                            widget=forms.TextInput(attrs={'size':'100'}),
                            required=True,help_text='Tags identificadoras das publicações separadas por ponto e virgula, Ex: S1; S2;S3 ...')
    
    

#Modelforms
class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_mismatch': u'Os endereços de e-mail devem ser iguais.',
    }
    username = forms.RegexField(label=u'Login ou Email', max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    email = forms.EmailField(label=u'(Repita) Email')
    password1 = forms.CharField(label=u'Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'(Repita) Senha', widget=forms.PasswordInput, help_text = u'Repita a senha')
    captcha = CaptchaField(label=u'Código de verificação')

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","captcha")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
    def clean_email(self):
        username = self.cleaned_data.get("username", "")
        email = self.cleaned_data["email"]
        if username != email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'])
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RevisaoForm(forms.ModelForm):
    class Meta:
        fields = ('titulo','nomereduzido')
        model = Revisao

class ChangeEtapaRevisaoForm(forms.ModelForm):
    class Meta:
        fields = ('titulo','nomereduzido','etapa','revisor')
        model = Revisao
        widgets = {
            'titulo': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'revisor': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'nomereduzido': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }

class FonteForm(forms.ModelForm):
    class Meta:
        fields = ('sigla','nome','url','revisao','expressao')
        model = Fonte
        widgets = {
            'revisao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }

class EtapaForm(forms.ModelForm):
    class Meta:
        fields = ('sigla','descricao','revisao')
        model = Etapa
        widgets = {
            'revisao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }
        
class QuestaoForm(forms.ModelForm):
    class Meta:
        fields = ('sigla','texto','revisao')
        model = Questao
        widgets = {
            'revisao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }

class CriterioForm(forms.ModelForm):
    class Meta:
        fields = ('sigla','descricao','revisao')
        model = Criterio
        widgets = {
            'revisao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }
        
class PublicacaoForm(forms.ModelForm):
    class Meta:
        fields = ('titulo','evento','autores','ano','idioma','fonte','etapa','searchpage','referenciaformatada','selecionada','arquivo','resumo','revisao',)
        model = Publicacao
        widgets = {
            'resumo': forms.Textarea(attrs={'cols': 50, 'rows': 8}),
            'revisao': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        
    '''
    def clean_arquivo(self):
        if self.cleaned_data['arquivo']:
            arquivo = self.cleaned_data['arquivo']
            if arquivo:
                content_type = arquivo.content_type.split('/')[-1]
                if content_type in CONTENT_TYPES:
                    if arquivo._size > MAX_UPLOAD_SIZE:
                        raise forms.ValidationError('Insira um arquivo menor que 1.5 MB')
                    else:
                        raise forms.ValidationError('Sistema só aceita arquivos PDF, PNG e JPEG.')
            return arquivo
    ''' 

class ReferenciaForm(forms.ModelForm):
    class Meta:
        fields = ('referencia','publicacao')
        model = Referencia
        widgets = {
            'publicacao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }
        
class InfoEtapaForm(forms.ModelForm):
    class Meta:
        fields = ('etapa','etapaconcluida','excluidanestaetapa','criterios','publicacao')
        model = InfoEtapa
        widgets = {
            'publicacao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }


class InfoQuestaoForm(forms.ModelForm):
    class Meta:
        fields = ('questao','classificacao','texto','publicacao')
        model = InfoQuestao
        widgets = {
            'texto': forms.Textarea(attrs={'cols': 50, 'rows': 8}),
            'publicacao': forms.HiddenInput(attrs={'readonly':'readonly'}),
             }



        