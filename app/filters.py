import django_filters
from django_filters import CharFilter, ChoiceFilter

from .models import *

class AnnouncementFilter(django_filters.FilterSet):
	title = CharFilter(field_name="title", lookup_expr='icontains',label='Título')
	content = CharFilter(field_name="content", lookup_expr='icontains', label = 'Descrição')
	category = ChoiceFilter(field_name="category", label = 'Categoria', choices = Announcement.CATEGORY)
	class Meta:
		model = Announcement
		fields = ['title','content','category']
		