from django.core.urlresolvers import reverse
from django.views.generic import (
    DetailView, ListView, CreateView, UpdateView, DeleteView)

from geosafe.models import Metadata, Analysis
from geosafe.forms import (
    MetadataUploadForm, MetadataUpdateForm, AnalysisCreationForm)


# Create your views here.

class MetadataListView(ListView):
    model = Metadata
    template_name = 'geosafe/metadata/list.html'
    context_object_name = 'metadata_list'

    def get_context_data(self, **kwargs):
        context = super(MetadataListView, self).get_context_data(**kwargs)
        return context


class MetadataCreate(CreateView):
    model = Metadata
    form_class = MetadataUploadForm
    template_name = 'geosafe/metadata/form.html'
    context_object_name = 'metadata'

    def get_success_url(self):
        return reverse('metadata-list')

    def get_form_kwargs(self):
        kwargs = super(MetadataCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class MetadataDetailView(DetailView):
    model = Metadata
    template_name = 'geosafe/metadata/detail.html'
    context_object_name = 'metadata'

    def get_object(self, queryset=None):
        obj = super(MetadataDetailView, self).get_object(queryset)
        return obj


class MetadataUpdateView(UpdateView):
    model = Metadata
    form_class = MetadataUpdateForm
    template_name = 'geosafe/metadata/update.html'
    context_object_name = 'metadata'
    # fields = ['metadata_file']

    def get_form_kwargs(self):
        kwargs = super(MetadataUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('metadata-detail', kwargs={'pk': self.object.layer.id})


class MetadataDeleteView(DeleteView):
    model = Metadata
    template_name = 'geosafe/metadata/delete.html'
    context_object_name = 'metadata'

    def get_success_url(self):
        return reverse('metadata-list')


class AnalysisCreateView(CreateView):
    model = Analysis
    form_class = AnalysisCreationForm
    template_name = 'geosafe/analysis/create.html'
    context_object_name = 'analysis'

    def get_success_url(self):
        return reverse('metadata-list')

    def get_form_kwargs(self):
        kwargs = super(AnalysisCreateView, self).get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        return kwargs