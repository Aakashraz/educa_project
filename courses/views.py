from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course, Module, Content
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.apps import apps
from django.forms.models import modelform_factory


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
                slef.model, id=id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )