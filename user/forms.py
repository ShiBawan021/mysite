from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from reply_card.models import MessageNum
from ckeditor.widgets import CKEditorWidget
from blog.models import BlogType, Blog

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名/邮箱 '}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='', max_length=20, min_length=3, widget=forms.TextInput(attrs={'id': 'username-control', 'class': 'form-control', 'placeholder': '请输入3-30位用户名'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'id': 'email-control', 'class': 'form-control', 'placeholder': '请输入邮箱'}), )
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '验证码'}))
    password = forms.CharField(label='',  max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'id': 'register-control', 'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='',  max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'id': 'password_again-control', 'class': 'form-control', 'placeholder': '请再输入一次密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('400')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('401')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('402')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='', max_length=8, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入新的名称'}))

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
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空')
        return nickname_new

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('400')

        # 判断用户是否已绑定邮箱
        # if self.request.user.email != '':
        #     raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('change_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        email = self.cleaned_data.get('email', '')
        blog_type = self.cleaned_data.get('blog_type', '')
        if not (code != '' and code == verification_code and email == ''):
            raise forms.ValidationError(blog_type)
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('402')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}
        )
    )
    new_password_again = forms.CharField(
        label='请再次输入新的密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code

class DelReplyCardForm(forms.Form):
    num = forms.CharField(
        label='标题',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clear_num(self):
        num = self.cleaned_data['num']
        if not num:
            raise forms.ValidationError('error')

        return num

class DelBlogForm(forms.Form):
    blog_id = forms.CharField(
        label='标题',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(DelBlogForm,self).__init__(*args, **kwargs)


    def clear_blog_id(self):
        blog_id = self.cleaned_data['blog_id']
        if not blog_id:
            raise forms.ValidationError('error')

        return blog_id

class DelCollectForm(forms.Form):
    collect_record_id = forms.CharField(
        label='标题',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clear_collect_record_id(self):
        collect_record_id = self.cleaned_data['collect_record_id']
        if not collect_record_id:
            raise forms.ValidationError('error')

        return collect_record_id

class RemindMessageFORM(forms.Form):
    remind_message = forms.CharField(
        label='标题',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clear_messages_num(self):
        messages_num = MessageNum.objects.get(user=self.user)
        if not messages_num:
            return forms.ValidationError('error')

        return messages_num
