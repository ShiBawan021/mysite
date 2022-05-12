from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import BlogType, Blog

class ContributionForm(forms.Form):
    blog_type = forms.ChoiceField(
        choices=BlogType.objects.values_list("id", "type_name"),
        label='类型',
        widget=forms.Select,
    )
    title = forms.CharField(
        label='标题',
        widget=forms.TextInput(
            attrs={ 'placeholder': '标题'}
        )
    )
    text = forms.CharField(
        label='',
        widget=CKEditorWidget(config_name='contribution_ckeditor'),
        error_messages={'required': '内容不能为空'}
    )

    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:
             self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户数是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')


    def clear_type(self):
        blog_type = self.cleaned_data['blog_type']
        if blog_type != '----':
            raise forms.ValidationError('请选择类型')

        return blog_type

    def clear_title(self):
        title = self.cleaned_data['title'].strip()
        if title == '':
            raise forms.ValidationError('标题不能为空')

        return title

    def clear_text(self):
        text = self.cleaned_data['text'].strip()
        if text == '':
            raise forms.ValidationError('内容不能为空')

        return text

class EditForm(forms.Form):
    blog_type = forms.ChoiceField(
        choices=BlogType.objects.values_list("id", "type_name"),
        label='类型',
        widget=forms.Select,
    )
    title = forms.CharField(
        label='标题',
        widget=forms.TextInput(
        attrs={'placeholder': '标题'}
        )
    )
    text = forms.CharField(
        label='',
        widget=CKEditorWidget(config_name='contribution_ckeditor'),
        error_messages={'required': '内容不能为空'}
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户数是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')

    def clear_type(self):
        blog_type = self.cleaned_data['blog_type']
        if blog_type != '----':
            raise forms.ValidationError('请选择类型')

        return blog_type

    def clear_title(self):
        title = self.cleaned_data['title'].strip()
        if title == '':
            raise forms.ValidationError('标题不能为空')

        return title

    def clear_text(self):
        text = self.cleaned_data['text'].strip()
        if text == '':
            raise forms.ValidationError('内容不能为空')

        return text