from django import forms

class ApiForm(forms.Form):
    library_id = forms.CharField(label='Library ID', max_length=100)
    # Puedes agregar más campos según sea necesario