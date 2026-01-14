from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm



class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        # Step 1: Save user and get redirect response
        result = super().form_valid(form)
        # At this point:
        # - User exists in database
        # - result = HttpResponseRedirect('student_course_list')

        # Step 2: Get form data
        cd = form.cleaned_data

        # Step 3: Authenticate (verify credentials)
        user = authenticate(
            username=cd['username'],
            password=cd['password1']    # Note usually password1 for UserCreationForm
        )
        # At this point:
        # - user = User objects with backend attribute

        # Step 4: Log user in (create session)
        login(self.request, user)
        # At this point:
        # - Session created
        # - request.user is now this user (not AnonymousUser)

        # Step 5: Return the redirect
        return result
        # Browser redirects to: ('student_course_list')



class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

