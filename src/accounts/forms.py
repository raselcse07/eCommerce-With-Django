from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


User = get_user_model()



class GuestForm(forms.Form):
    email    = forms.EmailField()



class Register(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email',)

    def clean_password2(self):

        # Check that the two password entries match

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format

        user = super(Register, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send email confirmation
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')

        qs_exists = User.objects.filter(username=username).exists()
        if qs_exists:
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        qs_exists = User.objects.filter(email=email).exists()
        if qs_exists:
            raise forms.ValidationError('Email already exists.')
        return email



class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username','email', 'password', 'is_active', 'is_staff','is_admin')

    def clean_password(self):

        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value

        return self.initial["password"]




class LoginForm(forms.Form):

	username        = forms.CharField(label="Username")
	password 		= forms.CharField(label='Password', widget=forms.PasswordInput)


	def clean(self,*args,**kwargs):

		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user_obj = User.objects.filter(username=username).first()

		if not user_obj:
			raise  forms.ValidationError("Invalid Username or Password !")
		else:
			if not user_obj.check_password(password):
				raise forms.ValidationError("Invalid Username or Password !")
                
		return super(LoginForm,self).clean(*args,**kwargs)
