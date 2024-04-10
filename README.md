


## Dependências do projeto
```bash
$ pip install python-decouple
$ pip install crispy-bootstrap4
```

## Começando um projeto
_(Aqui baseado em ambiente Linux)_

### Instalar do zero

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

### Criando o projeto

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
$ mkdir ./apps/core
$ django-admin startapp core ./apps/core

# abre projeto no VS Code
$ code .
```

### Configurar projeto no VS Code

- SELEÇÃO INTERPRETADOR
   - tecle Ctrl+Shift+P (escreva: select interpreter)
   - Selecione: aquele com ('venv':venv)
- CRIAR GITIGNORE
   - Ctrl+Shift+P (escreva: add Gitignore)
   - Selecione: Python

### Habilitar versionamento (Git/GitHub)
_(crie o repositório remoto no GitHub)_

```bash
$ cd ~/proj
$ git init
$ git add .
$ git commit -m "first commit"
$ git branch -M main
$ git remote add origin https://github.com/<seu_usuario>/decibels.git
$ git push -u origin main
```

### Plugins VSCode Interessantes
- gitignore
- Python IntelliSense
- Auto Rename Tag (Jun Han)
- Dracula Official
- Material Icon Theme
- Prettier - Code formatter
- Tailwind CSS IntelliSense
- IntelliCode (Microsoft)
- Portuguese (Brazil) Language Pack for VS Code


## Referências
- [Criação de App dentro de pasta específica](https://cursos.alura.com.br/forum/topico-criacao-de-app-dentro-de-pasta-especifica-216392)
- [How to Use Python Decouple](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html)
- [Decloupe Project](https://pypi.org/project/python-decouple/)
