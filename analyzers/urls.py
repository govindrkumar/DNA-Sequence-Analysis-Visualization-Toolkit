from django.urls import path
from . import views

urlpatterns = [path("", views.index, name = "index"),
path("about/", views.about_view, name = "about_page"),
path("analyse/", views.analyse_view, name = 'analyse_page'),
path("provider/", views.provider_view, name = 'provider_page'),
path("issues/", views.issues_view, name = 'issues_page'),
path(
        'run-analysis/<int:sequence_id>/',
        views.run_analysis,
        name='run_analysis'
    ),]