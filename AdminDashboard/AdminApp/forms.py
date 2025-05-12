from django import forms
from .models import User, Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'status', 'manager_comment', 'screenshot']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Report.objects.filter(title=title).exists():
            raise forms.ValidationError("A report with this title already exists.")
        return title

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status == 'approved' and not self.cleaned_data.get('manager_comment'):
            raise forms.ValidationError("Manager comment is required for approved reports.")
        return status

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'manager', 'is_staff', 'is_superuser']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        is_superuser = cleaned_data.get('is_superuser')
        
        # Ensure only admins can be superusers
        if role != 'admin' and is_superuser:
            raise forms.ValidationError("Only Admin users can be superusers.")

        return cleaned_data
