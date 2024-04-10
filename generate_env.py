import os
from django.core.management.utils import get_random_secret_key

def generate_env_file():

    secret_key = get_random_secret_key()

    env_content = f"SECRET_KEY={secret_key}\nDEBUG=True\n"
    env_file_path = ".env"

    with open(env_file_path, "w") as env_file:
        env_file.write(env_content)

    print(f"Arquivo .env criado com sucesso em: {os.path.abspath(env_file_path)}")

if __name__ == "__main__":
    generate_env_file()
