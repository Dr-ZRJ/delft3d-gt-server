"""
Views for the ui.
"""
from __future__ import absolute_import

from datetime import datetime
import json

import django_filters
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import View

from json_views.views import JSONDetailView
from json_views.views import JSONListView

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics

from delft3dworker.models import Scenario
from delft3dworker.models import Scene
from delft3dworker.models import Template
from delft3dworker.serializers import ScenarioSerializer
from delft3dworker.serializers import SceneSerializer
from delft3dworker.serializers import TemplateSerializer


#################################### REST

############ Filters


class SceneFilter(filters.FilterSet):
    """
    FilterSet to filter Scenes on complex queries, such as
    template, traversing db relationships.
    """
    strict = True
    template = django_filters.CharFilter(name="scenario__template__name")

    class Meta:
        model = Scene
        fields = ['template',]


############# Views


class ScenarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scenarios to be viewed or edited.
    """

    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class SceneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scenes to be viewed or edited.
    """

    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)

    # Django filter backend
    filter_fields = ('name', 'state')  # Direct equality

    # Our own custom filter
    filter_class = SceneFilter

    # Searchfilter backend
    search_fields = ('^name', '^state', '^scenario__template__name',)

    # Permissions backend
    # permission_classes = (delft3dgtmain.permissions.etc)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Scene.objects.all()

        # Filter on parameter
        parameter = self.request.query_params.get('parameter', None)
        if parameter is not None:
            try:
                p = parameter.split(',')
                if len(p) == 2:
                    key, value = p
                    key = key.encode('ascii', 'ignore')
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                    print((key, value))
                    q = {key: {'value': value}}
                    print(q)
                    queryset = queryset.filter(parameters__contains=q)
            except:
                return Scene.objects.none()
        return queryset


class TemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """

    queryset = Template.objects.all()
    serializer_class = TemplateSerializer






# ###################################
# The code below will be phased out in Sprint 4
#

# ################################### SCENARIO

class ScenarioCreateView(View):

    model = Scenario

    def post(self, request, *args, **kwargs):

        if 'scenariosettings' not in request.POST:
            return JsonResponse(
                {'created': 'false', 'error': 'no scenariosettings found'}
            )

        try:
            scenariosettings = json.loads(request.POST['scenariosettings'])
        except ValueError:
            return JsonResponse(
                {
                    'created': 'false',
                    'error': 'scenariosettings not in json format'
                }
            )

        newscenario = Scenario(
            name="Scene {}".format(datetime.now())
        )
        newscenario.save()  # Before creating children

        newscenario.load_settings(scenariosettings)
        newscenario.createscenes()

        # 25 april '16: Almar, Fedor & Tijn decided that
        # a scenario should be started server-side after creation
        newscenario.start()

        return JsonResponse({'created': 'ok'})

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioCreateView, self).dispatch(*args, **kwargs)


class ScenarioDeleteView(DeleteView):
    model = Scenario

    def get_object(self):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        return Scenario.objects.get(id=scenario_id)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        payload = {'status': 'deleted'}
        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioDeleteView, self).dispatch(*args, **kwargs)


class ScenarioDetailView(JSONDetailView):
    model = Scenario

    def get_object(self):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        scenario = Scenario.objects.get(id=scenario_id)
        return scenario

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioDetailView, self).dispatch(*args, **kwargs)


class ScenarioListView(JSONListView):
    model = Scenario

    def get_queryset(self):
        queryset = Scenario.objects.all().order_by('id')
        return queryset

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioListView, self).dispatch(*args, **kwargs)


class ScenarioStartView(View):
    model = Scenario

    # TODO: remove get
    def get(self, request, *args, **kwargs):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        scenario = get_object_or_404(Scenario, id=scenario_id)
        payload = {'status': scenario.start()}
        return JsonResponse(payload)

    def post(self, request, *args, **kwargs):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        scenario = get_object_or_404(Scenario, id=scenario_id)
        payload = {'status': scenario.start()}
        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioStartView, self).dispatch(*args, **kwargs)


class ScenarioStopView(View):
    model = Scenario

    # TODO: remove get
    def get(self, request, *args, **kwargs):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        scenario = get_object_or_404(Scenario, id=scenario_id)
        payload = {
            'id': scenario_id,
            'status': scenario.stop()
        }
        return JsonResponse(payload)

    def post(self, request, *args, **kwargs):
        scenario_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        scenario = get_object_or_404(Scenario, id=scenario_id)
        payload = {
            'id': scenario_id,
            'status': scenario.stop()
        }
        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ScenarioStopView, self).dispatch(*args, **kwargs)


# ################################### SCENE

class SceneCreateView(CreateView):
    model = Scene
    fields = ['name', 'state', 'info']

    def post(self, request, *args, **kwargs):
        return super(SceneCreateView, self).post(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneCreateView, self).dispatch(*args, **kwargs)


class SceneDeleteView(DeleteView):
    model = Scene

    def get_object(self):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        return Scene.objects.get(id=scene_id)

    def delete(self, request, *args, **kwargs):
        deletefiles = (
            request.GET.get('deletefiles') or request.POST.get('deletefiles')
        )
        self.success_url = reverse_lazy('scene_delete')

        scene = self.get_object()
        deletefiles = (deletefiles is not None) and ("true" in deletefiles)
        scene.delete(deletefiles=deletefiles)

        payload = {'status': 'deleted', 'files_deleted': deletefiles}
        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneDeleteView, self).dispatch(*args, **kwargs)


class SceneDetailView(JSONDetailView):
    model = Scene

    def get_object(self):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = Scene.objects.get(id=scene_id)
        return scene

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneDetailView, self).dispatch(*args, **kwargs)


class SceneListView(JSONListView):
    model = Scene

    def get_queryset(self):
        queryset = Scene.objects.all().order_by('id')
        return queryset

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneListView, self).dispatch(*args, **kwargs)


class SceneStartView(View):
    model = Scene

    # TODO: remove get
    def get(self, request, *args, **kwargs):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = get_object_or_404(Scene, id=scene_id)
        payload = {'status': scene.start()}
        return JsonResponse(payload)

    def post(self, request, *args, **kwargs):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = get_object_or_404(Scene, id=scene_id)
        payload = {'status': scene.start()}

        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneStartView, self).dispatch(*args, **kwargs)


class SceneStopView(View):
    model = Scene

    # TODO: remove get
    def get(self, request, *args, **kwargs):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = get_object_or_404(Scene, id=scene_id)
        payload = {'status': scene.abort()}
        return JsonResponse(payload)

    def post(self, request, *args, **kwargs):
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = get_object_or_404(Scene, id=scene_id)
        payload = {'status': scene.abort()}

        return JsonResponse(payload)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneStopView, self).dispatch(*args, **kwargs)


class SceneExportView(View):
    model = Scene

    def get(self, request, *args, **kwargs):
        """export data into a zip file
        - scene: model run
        - selection: images or log
        """
        scene_id = (self.request.GET.get('id') or self.request.POST.get('id'))
        scene = get_object_or_404(Scene, id=scene_id)

        stream, filename = scene.export()

        resp = HttpResponse(
            stream.getvalue(),
            content_type="application/x-zip-compressed"
        )
        resp[
            'Content-Disposition'] = 'attachment; filename={}'.format(filename)

        # TODO create a test with a django request
        # and test if the file can be read
        return resp

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SceneExportView, self).dispatch(*args, **kwargs)


# ################################### TEMPLATE

class TemplateDetailView(JSONDetailView):
    model = Template

    def get_object(self):
        template_id = (
            self.request.GET.get('id') or self.request.POST.get('id')
        )
        template = Template.objects.get(id=template_id)
        return template

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TemplateDetailView, self).dispatch(*args, **kwargs)


class TemplateListView(JSONListView):
    model = Template

    def get_queryset(self):
        queryset = Template.objects.all().order_by('id')
        return queryset

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(TemplateListView, self).dispatch(*args, **kwargs)
