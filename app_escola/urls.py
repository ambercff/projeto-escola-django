from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('tela_professor', views.tela_professor, name='tela_professor'),
    path('cadastro_turma', views.cadastro_turma, name='cadastro_turma'),
    path('tela_atividades', views.tela_atividades, name='tela_atividades'),
    path('cadastro_atividade', views.cadastro_atividade, name='cadastro_atividade'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro')
]