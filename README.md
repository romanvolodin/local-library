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
    "python.analysis.typeCheckingMode": "basic",
    "cSpell.words": [
        "isort",
        "venv"
    ],
    "emmet.includeLanguages": {
        "django-html": "html"
    }
}
```

## Тестирование

Важно из какой папки запускается команда `./manage.py test`.

Чтобы запустить тесты для всех приложений сразу, нужно перейти в папку, где лежит `manage.py`. В данном случае это `src`:

```bash
$ cd src/
$ manage.py test
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
-----------------------------------------------
Ran 6 tests in 0.008s

OK
```

Иначе, если запускать команду из корня проекта, то Django не может обнаружить тесты. Выполняем в корне команду:

```bash
src/manage.py test
```

получаем вывод, что выполнено 0 тестов

```bash
Found 0 test(s).
System check identified no issues (0 silenced).

-----------------------------------------------
Ran 0 tests in 0.000s

OK
```

При этом, если запустить тесты для конкретного приложения, то всё отработает как надо:

```bash
$ src/manage.py test catalog
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
-----------------------------------------------
Ran 6 tests in 0.008s

OK
```
