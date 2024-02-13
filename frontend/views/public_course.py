"""Purpose of this file

This file describes the frontend views related to course.
"""

import json

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Course, CourseStructureEntry, Topic, Favorite
from base.utils import check_owner_permission

from frontend.forms import AddCourseForm, EditCourseForm, FilterAndSortForm
from frontend.forms.course import TopicChooseForm, CreateTopicForm

from frontend.views.history import Reversion
from frontend.views.json import JsonHandler


class CourseViewPublic(LoginRequiredMixin, DetailView, FormMixin):
    """Course list view

    Displays the course detail page.

    :attr CourseView.model: The model of the view
    :type CourseView.model: Model
    :attr CourseView.template_name: The path to the html template
    :type CourseView.template_name:str
    :attr CourseView.form_class: The form class of the view
    :type CourseView.form_class: Form
    :attr CourseView.context_object_name: The context object name
    :type CourseView.context_object_name: str
    """

    template_name = 'frontend/course/view.html'
    model = Course
    form_class = FilterAndSortForm
    context_object_name = "public_course"

    def __init__(self):
        """Initializer

        Initialize the course view with pre configuration for the sort and filter options
        with default values.
        """
        self.sorted_by = 'None'
        self.filtered_by = 'None'
        super().__init__()

    def get_success_url(self):
        """Success url

        Returns the url to return to after successful deletion.

        :return: the success url
        :rtype: __proxy__
        """
        return reverse_lazy('frontend:index')

    '''def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        # Add/remove favourite
        if request.POST.get('save') is not None:
            # Identify the profile and the course
            profile = get_user(request).profile
            course = get_object_or_404(Course, pk=request.POST.get('course_pk'))
            if request.POST.get('save') == 'true':
                profile.stared_courses.add(course)
            else:
                profile.stared_courses.remove(course)
            return HttpResponse()
        if request.POST.get('course_pk') is not None:
            # Identify the profile and the course
            profile = get_user(request).profile
            course = get_object_or_404(Course, pk=request.POST.get('course_pk'))
            return JsonResponse(data={'save': course in profile.stared_courses.all()})

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        # Edit course structure cancel/save
        if request.is_ajax():
            check = True
            # Update course structure
            topic_list = request.POST.get('topic_list')
            if topic_list:
                json_obj = json.loads(topic_list)
                try:
                    JsonHandler.validate_topics(json_data=json_obj)
                except ValidationError:
                    check = False
                if check:
                    JsonHandler.json_to_topics_structure(self.object, json_obj)

            # Clean unused topics
            ids = request.POST.getlist('ids[]')
            if ids:
                JsonHandler.clean_topics(ids)

            if not check:
                return HttpResponseBadRequest()
            return HttpResponse()

        return self.form_invalid(form) '''

    def form_valid(self, form):
        """Form validation

        Saves the filters and sorting from the form.

        :param form: The form that contains the filter and the sorting
        :type form: FilterAndSortForm

        :return: Itself rendered to a response
        :rtype: HttpResponse
        """
        self.sorted_by = form.cleaned_data['sort']
        self.filtered_by = form.cleaned_data['filter']
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        
        course_id = self.get_object().id
        favorite_list = [] # Favorite.objects.filter(course=course_id, user=get_user(self.request).profile)
        context = super().get_context_data(**kwargs)
        structure_entries = CourseStructureEntry. \
            objects.filter(course=context["course"]).order_by('index')
        topics_recursive = []
        current_topic = None
        for favorite in Favorite.objects.filter(course=course_id, user=get_user(self.request).profile):
            favorite_list.append(favorite.content)

        for entry in structure_entries:
            index_split = entry.index.split('/')
            # Topic
            if len(index_split) == 1:
                current_topic = {'topic': entry.topic, 'subtopics': [],
                                 'topic_contents': entry.topic.get_contents(self.sorted_by,
                                                                            self.filtered_by)}
                topics_recursive.append(current_topic)
            # Subtopic
            # Only handle up to one subtopic level
            else:
                current_topic["subtopics"].append({'topic': entry.topic,
                                                   'topic_contents':
                                                       entry.topic.
                                                  get_contents(self.sorted_by, self.filtered_by)})


        context["structure"] = topics_recursive
        context['isCurrentUserOwner'] = self.request.user.profile in context['course'].owners.all()
        context['user'] = self.request.user
        context['favorite'] = favorite_list
        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by

        """# create a list of topics ordered by (sub-)topic and index
        flat_topic_list = create_topic_and_subtopic_list(topics, super().get_object())
        print(flat_topic_list)
        context['topics'] = flat_topic_list
        # create a list of files for each (sub-)topic
        files = []
        for _, topic, _ in flat_topic_list:
            files.append(topic.get_contents(self.sorted_by, self.filtered_by))
    
        context['files'] = files
        # context['Content'] = Content
        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by
        
        if self.request.user.is_authenticated:
            context['coursebook_length'] = models.get_coursebook_length(user=get_user(self.request), course=self.object)
            context['coursebook'] = models.get_coursebook(get_user(self.request), self.object)
            missing_topics = [x.title for x in self.object.topic_list.order_by('child_topic__index')
                              if Favourite.objects.filter(user=get_user(self.request),
                                                          course=self.object, topic=x).count() == 0
                              or Favourite.objects.get(user=get_user(self.request),
                                                       course=self.object,
                                                       topic=x).content_list.all().count() == 0]
            context['missing_topics'] = ", ".join(missing_topics)
        """

        return context