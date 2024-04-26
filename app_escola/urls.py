from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('tela_professor', views.tela_professor, name='tela_professor'),
    path('cadastro_turma/<int:id_professor>', views.cadastro_turma, name='cadastro_turma'),
    path('tela_atividades/<int:id_turma>', views.tela_atividades, name='tela_atividades'),
    path('cadastro_atividade/<int:id_turma>', views.cadastro_atividade, name='cadastro_atividade'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('excluir_turma/<int:id_turma>', views.excluir_turma, name="excluir_turma"),
    path('atividade_arquivos/<str:nome_arquivo>', views.exibir_arquivo, name='exibir_arquivo'),
    path('exportar_excel_turma/', views.exportar_para_excel_turmas, name='exportar_excel_turma'),
    path('exportar_excel_atividade', views.exportar_para_excel_atividades, name='exportar_excel_atividade')
]