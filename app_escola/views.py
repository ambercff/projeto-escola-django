from django.shortcuts import render
from hashlib import sha256
from django.db import connection, transaction
from django.contrib.auth import authenticate;
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from app_escola.models import *

# Create your views here.

def initial_population():
    cursor = connection.cursor()

    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()

    insert_sql_professor = "INSERT INTO app_escola_professor (nome, email, senha) VALUES "
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"

    cursor.execute(insert_sql_professor)
    transaction.atomic()


    # Turma

    insert_sql_turma = "INSERT INTO app_escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"

    cursor.execute(insert_sql_turma)
    transaction.atomic()

    # Atividade
    insert_sql_atividade = "INSERT INTO app_escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()

    print("Finish")

def index(request):
    return render(request, 'index.html')

def login(request):

    if request.method == 'POST':
        email = request.POST["email"]
        senha = request.POST["senha"]
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']

            if senha == senha_criptografada:
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_professor = Turma.objects.filter(id_professor=id_logado)
                
                return render(request, "tela_professor.html", {
                    "nome": usuario_logado,
                    "turmas_professor": turmas_professor,
                    "id_logado": id_logado
                })
            else:
                return render(request, "login.html", {
                    "message": "Usuário ou senha incorretos. Tente novamente!"
                })
        return render(request, "cadastro_professor.html", {
            "message": f"Olá {email} seja bem-vindo! Percebemos que você é novo por aqui. Complete seu cadastro.",
            "login": email,
        })
    return render(request, "login.html")
    
def logout_view(request):
    return render(request, "login.html")

def tela_professor(request):
    return render(request, 'tela_professor.html')

def cadastro_turma(request, id_professor):
    if request.method == 'POST':
        nome_turma = request.POST["nome_turma"] 
        professor = Professor.objects.get(id=id_professor)
        with transaction.atomic():
            grava_turma = Turma(nome_turma=nome_turma, id_professor=professor)
            grava_turma.save()
        turmas_professor = Turma.objects.filter(id_professor=id_professor)

        return render(request, "tela_professor.html", {
            "nome": professor,
            "turmas_professor": turmas_professor,
            "id_logado": id_professor
        })
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    return render(request, 'cadastro_turma.html', {
        "usuario_logado": usuario_logado,
        "id_logado": id_professor
    })

def tela_atividades(request, id_turma):
    atividades_turma = Atividade.objects.filter(id_turma_id = id_turma)
    turma = Turma.objects.filter(pk=id_turma).first()
    return render(request, 'tela_atividades.html', {
        "atividades_turma": atividades_turma,
        "turma_id": id_turma,
        "nome_turma": turma.nome_turma,
        "nome": turma.id_professor
    })

def cadastro_atividade(request, id_turma):
    if request.method == 'POST':
        desc_atividade = request.POST["desc_atividade"]
        arquivo = request.FILES.get("arquivo")
        print(f"ARQUIVO: {arquivo}")
        turma = Turma.objects.get(pk=id_turma)
      

        with transaction.atomic():
            grava_atividade = Atividade(nome_atividade=desc_atividade, id_turma=turma, arquivo=arquivo)
            grava_atividade.save()

        return HttpResponseRedirect(reverse("tela_atividades", args=[id_turma]))
    return render(request, 'cadastro_atividade.html', {
        "turma_id": id_turma
    })

def confirmar_cadastro(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["senha"]
        senha_criptografada = sha256(senha.encode()).hexdigest()

        with transaction.atomic():
            grava_professor = Professor(nome=nome, email=email, senha=senha_criptografada)
            grava_professor.save()

        return render(request, "login.html")
    
def excluir_turma(request, id_turma):
    try:
        with transaction.atomic():
            turma = Turma.objects.get(pk=id_turma)
            id_professor = turma.id_professor_id
            turma.delete()

            professor = Professor.objects.get(pk=id_professor)
            turmas_professor = Turma.objects.filter(id_professor=id_professor)

        return render(request, "tela_professor.html", {
            "nome": professor.nome,
            "turmas_professor": turmas_professor,
            "id_logado": id_professor
        })
    except Turma.DoesNotExist:
        # Trate aqui o caso em que a turma não existe
        # Por exemplo, redirecione o usuário para uma página de erro
        pass
    