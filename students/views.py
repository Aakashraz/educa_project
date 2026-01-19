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
    # Class attribute: stores current course being enrolled in
    course = None
    # Tells FormView which form class to use
    form_class = CourseEnrollForm

    def form_valid(self, form):
        # 1. Extract course from hidden form field
        self.course = form.cleaned_data['course']
        # 2. Add current user to course's students
        #    Many-to-Many relationship: course.students.add(user) -- .add() came from m2m manager
        self.course.students.add(self.request.user)
        # 3. Let parent handle redirect
        #   Parent calls get_success_url() which needs self.course
        #   Must be called AFTER we set self.course!
        return super().form_valid(form)

    def get_success_url(self):
        # Called by super().form_valid()
        # Return URL to redirect to after successful enrollment
        # Uses self.course that we set in form_valid()
        return reverse_lazy('student_course_detail', args=[self.course.id])

