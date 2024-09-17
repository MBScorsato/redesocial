import random
from django.contrib.auth import authenticate, login, get_user_model
import traceback  # Para capturar o stack trace completo
from index.models import ImagemIndex, ImagemIndex2
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages


def cadastro(request):
    if request.method == 'GET':
        title_img = ImagemIndex.objects.all()
        title_img2 = ImagemIndex2.objects.all()
        return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if password2 != password:
            print('são diferentes')
            messages.error(request, 'as senhas são diferentes!')
            title_img = ImagemIndex.objects.all()
            title_img2 = ImagemIndex2.objects.all()
            return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

        # Verificar se todos os campos foram preenchidos
        if not username or not password or not email:
            title_img = ImagemIndex.objects.all()
            title_img2 = ImagemIndex2.objects.all()
            messages.error(request, 'Preencha todos os campos!')
            return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

        # Verificar se o email já existe
        if User.objects.filter(email=email).exists():
            title_img = ImagemIndex.objects.all()
            title_img2 = ImagemIndex2.objects.all()
            messages.error(request, 'Email já cadastrado!')
            return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

        # Verificar se o username já existe
        if User.objects.filter(username=username).exists():
            title_img = ImagemIndex.objects.all()
            title_img2 = ImagemIndex2.objects.all()
            messages.error(request, 'Nome de usuário já existe!')
            return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

        try:

            # Criar o usuário se as verificações passarem
            user = User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')

        except:
            title_img = ImagemIndex.objects.all()
            title_img2 = ImagemIndex2.objects.all()
            messages.error(request, 'Erro ao criar o usuário. Tente novamente.')
            return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})

    else:
        title_img = ImagemIndex.objects.all()
        title_img2 = ImagemIndex2.objects.all()
        return render(request, 'cadastro.html', {'title_img': title_img, 'title_img2': title_img2})


def login_(request):
    if request.method == 'GET':
        title_img = ImagemIndex.objects.all()
        title_img2 = ImagemIndex2.objects.all()
        return render(request, 'login.html', {'title_img': title_img, 'title_img2': title_img2})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(username=username, password=password)

        if user is not None:
            # Se a autenticação foi bem-sucedida, faz login do usuário
            login(request, user)
            return redirect('plataforma')  # Redireciona para a plataforma após login
        else:
            # Se a autenticação falhar, retorna à página de cadastro ou exibe uma mensagem de erro
            messages.error(request, 'Usuário ou senha incorretos. Tente novamente ou cadastre-se.')
            return redirect('cadastro')


def enviar_email(request):
    if request.method == 'GET':
        title_img2 = ImagemIndex2.objects.all()
        return render(request, 'recuperar_senha.html', {'title_img2': title_img2})

    if request.method == 'POST':
        email_ = request.POST.get('email_recuperar').strip()
        print(f"Email recebido: {email_}")

        User = get_user_model()
        try:
            user = User.objects.get(email=email_)
            print('Usuário encontrado:', user)
            messages.success(request, 'Email enviado com SUCESSO!')
        except User.DoesNotExist:
            print('Usuário não encontrado')
            print(traceback.format_exc())  # Imprime o stack trace completo
            messages.warning(request, 'Email não encontrado!')
            title_img2 = ImagemIndex2.objects.all()
            return render(request, 'recuperar_senha.html', {'title_img2': title_img2})
        except Exception as e:
            print('Erro inesperado:', e)
            print(traceback.format_exc())  # Imprime o stack trace completo para outros erros
            messages.warning(request, 'Digite o Email!')
            title_img2 = ImagemIndex2.objects.all()
            return render(request, 'recuperar_senha.html', {'title_img2': title_img2})

        # Sorteio de nova senha
        nova_senha = str(random.randint(1000000, 9999999))
        print(f"Nova senha gerada: {nova_senha}")

        # substitui a senha velha pela senha nova
        user.set_password(nova_senha)
        user.save()

        # Envio do email com a nova senha
        assunto = "Recuperação de senha"
        corpo = f"Sua nova senha é: {nova_senha}. Lembre-se de alterá-la o quanto antes."
        de = 'gramline.recuperacao.de.senha@gmail.com'
        senha = 'eibrutfknhhwjxbi'

        msg = MIMEMultipart()
        msg['From'] = de
        msg['To'] = email_
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'html'))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(de, senha)
        s.sendmail(de, email_, msg.as_string())  # Corrigi a variável email para email_
        s.quit()

        title_img2 = ImagemIndex2.objects.all()
        return render(request, 'recuperar_senha.html', {'title_img2': title_img2})
