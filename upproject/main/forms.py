from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post, PostImage, Tag
from django.contrib.auth.forms import SetPasswordForm
from django.forms import inlineformset_factory


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'resume', 'age', 'profile_image', 'verification_image', 'country', 'interest')

    interest = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Write your interest', 'id': 'q'}))
    age = forms.DateField(input_formats=["%Y-%m-%d"], widget=forms.DateInput(attrs={'placeholder': 'Age', 'type': 'date'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'resume', 'profile_image', 'country', 'interest')
    
    interest = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Write your interest', 'id': 'q'}))



class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('slug', 'published', 'author', 'status', 'tags')

#tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(),queryset=Tag.objects.all())

#PostImageFormSet = inlineformset_factory(Post, PostImage, form=PostCreationForm, extra=1, fields=('images', ), can_delete=False)

'''
PostInlineFormset = inlineformset_factory(
    Post,
    PostImage,
    form=PostImage,
    extra=5,
    #fields = '__all__'
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)'''