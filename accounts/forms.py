from django import forms
from .models import User, Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Enter your password '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Repeat your password',
                                                                         'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
    #One way to style the form
    # def __init__(self, *args, **kargs):
    #     super(UserForm, self).__init__(*args, **kargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class':'form-control'})
    #Another way can be 
    def __init__(self, *args, **kargs):
        super(UserForm, self).__init__(*args, **kargs)
        self.fields['first_name'].widget.attrs['placeholder'] ='Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] ='Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] ='Enter your email address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match each other!!!")
        


class UserFormProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']
    def __init__(self, *args, **kargs):
        super(UserFormProfile, self).__init__(*args, **kargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, error_messages={'invalid':{"Image Files Only"}}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ('address_line_1', 'address_line_2', 'profile_image', 'city', 'state', 'country')
    def __init__(self, *args, **kargs):
        super(ProfileForm, self).__init__(*args, **kargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

