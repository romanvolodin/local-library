# local-library

## Создаем виртуальное окружение

```bash
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
```

## Добавляем .gitignore

В корне проекта выполняем команду:

```bash
curl https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore > .gitignore
```

## Install Django

```bash
pip install django
```

## Format code

Remove the default Django comments and then

```bash
isort .
black .
```

## VS Code config

In project_root/.vscode/settings.json:

```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    },
    "python.analysis.typeCheckingMode": "basic"
}
```
