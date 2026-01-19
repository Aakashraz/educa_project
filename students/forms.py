from django import forms
from courses.models import Course



# To enroll a user into a specific course
class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),     # <- Why empty? - This prevents Django from
        # querying the database when the 'form class' is defined (at module import time).
        widget=forms.HiddenInput            # <- Why hidden? - Because the user doesn't
        # choose the course -- it's passed from the view!
    )

    def __init__(self, *args, **kwargs):    # <- Why override?
        # - To populate the choices only when the form is created, not when the module loads.
        super().__init__(*args, **kwargs)
        # NOW set the queryset (when form is actually being used)
        self.fields['course'].queryset = Course.objects.all()

# Why super().__init__(*args, **kwargs) is mandatory here?
# The parent class (forms.Form) needs those arguments to:
# - Bind POST data
# - Set initial values
# - Handle prefixes
# - Prepare fields