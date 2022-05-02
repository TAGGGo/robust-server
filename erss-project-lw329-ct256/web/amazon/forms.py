from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Customer


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ('address', 'phone', 'country', 'state', 'ups_name')
	
	def save(self, commit=True):
		customer = super(CustomerForm, self).save(commit=False)
		customer.address = self.cleaned_data['address']
		customer.country = self.cleaned_data['country']
		customer.ups_name = self.cleaned_data['ups_name']
		customer.state = self.cleaned_data['state']
		if commit:
			customer.save()
		return customer
