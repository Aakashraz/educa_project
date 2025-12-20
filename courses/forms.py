from django.forms.models import inlineformset_factory
from .models import Course, Module


ModuleFormSet = inlineformset_factory(
    Course,     # Parent model
    Module,     # Child model - Django creates a ModelForm for this automatically
    fields=['title', 'description'],    # These become form fields
    extra=2,    # Show 2 empty forms for adding new Modules
    can_delete=True     # Add checkboxes to delete existing Modules
)
# Behind the scene for above code ------------
# Django automatically creates something like:
# class ModuleForm(ModelForm):
#     class Meta:
#         model = Module
#         fields = ['title', 'description']
# Then wraps it in a formset

