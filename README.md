# Projeto Decibels

Esta aplicação tem como objetivo apresentar gráficos dos valores coletados por um decibelímetro baseado no Arduino Uno. Ele permite monitorar diferentes locais e estabelecer limites ideais para cada um deles.

Um usuário administrador pode autorizar o registro de novos usuários fornecendo seus e-mails para acesso à aplicação. O novo usuário receberá um código de autorização permitindo-o se registrar.

Um usuário administrador pode autorizar novos usuários fornecendo seus endereços de e-mail para acesso à aplicação. Então, o novo usuário receberá um código de autorização exclusivo que permitirá o registro.

As métricas coletadas pelo decibelímetro podem ser importadas a partir de um arquivo CSV com o seguinte layout:

| ID Locação | Data de Registro | Valor Medido |
|-------------|-------------|-------------|
| 000 | yyyy-mm-dd hh:mm:ss | 00000,0000
| 000 | yyyy-mm-dd hh:mm:ss | 00000,0000

Arquivo Exemplo:

```csv
3,2024-04-10 10:35:18,35.2500
3,2024-04-11 10:38:18,36.1400
3,2024-04-11 12:28:03,63.2500
```

## 📦 Baixando e executando o projeto

Abra um terminal de comandos e proceda conforme abaixo:

```bash
$ cd ~
$ git clone https://github.com/celsovit/decibels.git
$ cd decibels

$ python -m venv venv
$ source venv/bin/activate

$ pip install -r requirements.txt
$ python generate_env.py

$ python manage.py migrate
$ python manage.py populate_db

$ python manage.py runserver
```

 No navegador acesse: [http://localhost:8000](http://localhost:8000)

```text
usuário: user
senha  : user
```


## 📜 Referências
- [Criação de App dentro de pasta específica](https://cursos.alura.com.br/forum/topico-criacao-de-app-dentro-de-pasta-especifica-216392)
- [How to Use Python Decouple](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html)
- [Decloupe Project](https://pypi.org/project/python-decouple/)
- [crispy-bootstrap4](https://pypi.org/project/crispy-bootstrap4/)
- [Django Crispy Forms and Bootstrap 5](https://studygyaan.com/django/how-to-use-bootstrap-forms-with-django-crispy-forms)
- [Django Login, Logout, Signup, Password Change, and Password Reset](https://learndjango.com/tutorials/django-login-and-logout-tutorial)
- [Django Best Practices: Referencing the User Model](https://learndjango.com/tutorials/django-best-practices-referencing-user-model)
- [Vincular Usuário](https://groups.google.com/g/django-users/c/zZWZyGePIEI)
- [Log out via GET requests is deprecated and will be removed in Django 5.0](https://stackoverflow.com/questions/74896216/log-out-via-get-requests-is-deprecated-and-will-be-removed-in-django-5-0)
- [Deprecation of GET method for LogoutView](https://forum.djangoproject.com/t/deprecation-of-get-method-for-logoutview/25533/4)
- [Como fazer upload de arquivos com Django](https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html)
- [What’s the difference between FileField, FilePathField and ImageField?](https://swesadiqul.medium.com/whats-the-difference-between-filefield-filepathfield-and-imagefield-302b2c284418)
- [Matplotlib vs. Seaborn vs. Plotly: A Comparative Guide](https://medium.com/@mohsin.shaikh324/matplotlib-vs-seaborn-vs-plotly-a-comparative-guide-c99a0059c09f#:~:text=Matplotlib%20offers%20extensive%20customization%20but,Matplotlib%20might%20be%20your%20choice.)
- [Arduino HTTP Request](https://arduinogetstarted.com/tutorials/arduino-http-request)
- [Ethernet Shield Web Client](https://docs.arduino.cc/tutorials/ethernet-shield-rev2/web-client/)
- [Como usar com Arduino – Ethernet Shield W5100 (Web server)](https://blogmasterwalkershop.com.br/arduino/arduino-utilizando-o-ethernet-shield-w5100-via-web-server)
- [Full Stack Data Streaming Middleware based on Django for an IoT Use-Case](https://akpolatcem.medium.com/full-stack-data-streaming-middleware-based-on-django-for-an-iot-use-case-5f97c1d941c7)
- [Tutorial Chart.js](https://www.geeksforgeeks.org/chart-js-tutorial/)
- [Adding Charts to Django with Chart.js](https://testdriven.io/blog/django-charts/)
- [chartjs-plugin-datalabels](https://chartjs-plugin-datalabels.netlify.app/guide/getting-started.html#installation)
- [How to Add Datalabels Inside or Outside of The Pie Chart in Chart JS](https://youtu.be/B4ph2g-LqTs)
- [Youtube: Django: Paginação + filtros](https://www.youtube.com/watch?v=eXipSfa-HOQ)
- [Como paginar o Django com outras variáveis ​​get](https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables/62587351#62587351)
- [Tags e filtros de template personalizados](https://django-portuguese.readthedocs.io/en/1.0/howto/custom-template-tags.html)
- [[Free] Deploy Django project to PythonAnywhere](https://medium.com/@4yub1k/free-deploy-django-project-to-pythonanywhere-1f3f08a6447f)



## 📌 Dicas sobre Python/Django


### Começando um projeto
_(Aqui baseado em ambiente Linux)_


#### Instalar Python/Django

```bash
# Habilitando Python
$ sudo apt update && apt upgrade

$ sudo apt install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa

$ sudo apt install python3.12
$ sudo apt install python3-pip
$ sudo apt install python3.12-venv
$ sudo pip install virtualenv

# adicione no arquivo ~/.bashrc
$ alias python='python3.12'
```


#### Criando o projeto

```bash
# cria pasta do projeto (na pasta home)
$ mkdir ~/proj
$ cd ~/proj

# ativa ambiente virtual e atualiza pip
$ source venv/bin/activate
$ python -m pip install --upgrade pip

# instala Django
$ pip install django

# cria o projeto
$ django-admin startproject decibels .

# processa as migrations
$ python manage.py migrate

# cria superusuário (defina username e password)
$ python manage.py createsuperuser

# inicia servidor  (Ctrl+C para interromper)
$ python manage.py runserver 

# confira no navegador se projeto no ar
# Acesse: http://localhost:8000
# INTERROMPA PARA PROSSEGUIR

# criar primeiro app
$ mkdir -p ./apps/core
$ django-admin startapp core ./apps/core

# abre projeto no VS Code
$ code .
```


#### Dependências usadas no projeto Decibels
```bash
$ pip install python-decouple
$ pip install crispy-bootstrap4
$ pip install Pillow
```


#### Configurar projeto no VS Code
https://github.com/hideraldus13/github-emoji
- SELEÇÃO INTERPRETADOR
   - tecle Ctrl+Shift+P (escreva: select interpreter)
   - Selecione: aquele com ('venv':venv)
- CRIAR GITIGNORE
   - Ctrl+Shift+P (escreva: add Gitignore)
   - Selecione: Python


#### Habilitar versionamento (Git/GitHub)
_(crie o repositório remoto no GitHub)_

```bash
$ cd ~/proj- [crispy-bootstrap4](https://pypi.org/project/crispy-bootstrap4/)
- [Django Crispy Forms and Bootstrap 5](https://studygyaan.com/django/how-to-use-bootstrap-forms-with-django-crispy-forms)

$ git init
$ git add .
$ git commit -m "first commit"
$ git branch -M main
$ git remote add origin https://github.com/<seu_usuario>/decibels.git
$ git push -u origin main
```

#### Plugins VSCode Interessantes
- gitignore
- Python IntelliSense
- Auto Rename Tag (Jun Han)
- Dracula Official
- Material Icon Theme
- Prettier - Code formatter
- Tailwind CSS IntelliSense
- IntelliCode (Microsoft)
- Portuguese (Brazil) Language Pack for VS Code
