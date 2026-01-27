from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course, Module, Content, Subject
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from .forms import ModuleFormSet
from django.apps import apps
from django.forms.models import modelform_factory
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from students.forms import CourseEnrollForm
from django.core.cache import cache



class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(LoginRequiredMixin, PermissionRequiredMixin, OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManagerCourseListView(OwnerCourseMixin,ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'course.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'course.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'course.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'course.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    # TemplateResponseMixin: This mixin takes charge of rendering templates and returning an HTTP response.
    # It requires a template_name attribute that indicates the template to be rendered and provides the
    # render_to_response() method to pass it a context and render the template.
    # View: The basic class-based view provided by Django.

    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    # get_formset(): You define this method to avoid repeating the code to build the formset. You
    # create a ModuleFormSet object for the given Course object with optional data.

    def dispatch(self, request, pk):
        self.course = get_object_or_404(
            Course, id=pk, owner=self.request.user
        )
        return super().dispatch(request, pk)
    # dispatch(): This method is provided by the View class. It takes an HTTP request and its parameters
    # and attempts to delegate to a lowercase method that matches the HTTP method used. A GET request
    # is delegated to the get() method and a POST request to post(), respectively. In this method, you
    # use the get_object_or_404() shortcut function to get the Course object for the given id parameter
    # that belongs to the current user. You include this code in the dispatch() method because you need to
    # retrieve the course for both GET and POST requests. You save it into the course attribute of the view
    # to make it accessible to other methods.

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset':formset}
        )
    # get(): Executed for GET request. You build an empty ModuleFormSet formset and render it to the template
    # together with the current Course object, using the render_to_response() method provided by TemplateResponseMixin.

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset':formset}
        )
    # post(): Executed for POST requests. In this method, you perform the following actions:
    # - You build a ModuleFormSet instance using the submitted data.
    # - You execute the is_valid() method of the formset to validate all of its forms.
    # - If the formset is valid, you save it by calling the save() method. At this point, any
    #   changes made, such as adding, updating, or making modules for deletion, are applied to the
    #   database. Then, you redirect users to the manage_course_list URL. If the formset is
    #   not valid, you render the template to display any errors instead.


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses', model_name=model_name
            )
        return None

        # modelform_factory - dynamically creates a ModelForm class at runtime from a specified Django model,
        # saving you from manually defining a forms.ModelForm in forms.py for simple cases, letting you configure
        # fields, widgets, labels, and validation rules directly, and it's the foundation for more
        # tools like modelformset_factory.
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model= self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model, instance=self.obj, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(
                    module=self.module,     # Which module this content belongs to
                    item=obj    # The actual content object (Text/Video/Image/File)
                )
            return redirect('module_content_list', self.module.id)
        # Always redirect after successful POST - Prevents duplicate submissions

        # This line never executed when form is valid.
        return self.render_to_response(
            {'form':form, 'object':self.obj}
        )
        # If execution reaches here directly if there are validation errors.
        # Result:
        # - Nothing is saved to database
        # - Form re-displayed with:
            # - User's input preserved
            # - Error messages shown
            # - User can fix and re-submit


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        return self.render_to_response({'module': module})


# Re-ordering modules and their contents
# JsonRequestResponseMixin: A mixin that attempts to parse the request as JSON. If the request is properly formatted,
# the JSON is saved to self.request_json as a Python object. request_json will be 'None' for unparseable requests.
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved':'OK'})
# Key Takeaway:
# The reorder view only updates numbers.
# The display views sort by those numbers, usually via Meta.ordering of the 'Module' model class.


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved':'OK'})
    

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, subject=None):
        # # ALWAYS get all subjects with counts (for sidebar)
        # subjects = Subject.objects.annotate(
        #     total_courses=Count('courses')
        # )
        # These above line is replaced by the caching 'all_subjects'.
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('courses')
            )
            cache.set('all_subjects', subjects)
            # Here, the cache.set() enforces the evaluation of the queryset before
            # storing into the cache.
            # WHY?
            # - Memcached cannot store database connections
            # - Lazy DB cursors cannot be serialized
            # - Django ensures the queryset is fully materialized. So, internally it behaves like:
            # subjects = list(subjects)     # evaluation happens
            # cache.set('all_subjects', subjects)
            # What is actually stored:
            # - A list of Subject objects
            # - Each object already has total_courses calculated
        # One-sentence takeaway
        # - Django finishes talking to the database, collects the data and only then gives
        # Memcached something simple enough to store.

        # ALWAYS start with all courses
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        # IF subject provided, filter down
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)   # <- Narrow down!
        # ELSE courses stays as "all courses"

        return self.render_to_response(
            {
            'subjects': subjects,   # Always show all subjects (for navigation)
            'subject': subject,     # Currently selected subject (or None)
            'courses': courses      # All courses OR filtered courses
            }
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the enrollment form to context
        context['enroll_form'] = CourseEnrollForm(
            initial={'course':self.object}  # Pre-fill the hidden course field with the current course.
        )
        return context


