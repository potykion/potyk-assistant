# `potyk_assistant` ex `kys_in_rest`

> Телеграм бот, показывающий где поесть в Москве, а также пивко заносить, и вес вводить, и вообще все, что мне в голову
> взбредет

- [Бот](https://t.me/kys_in_rest_bot)
- [Github](https://github.com/potykion/kys_in_rest)

## Операции

### Серв Первая установка

```sh
ssh -l leybovich-nikita 84.201.131.244
git clone https://github.com/potykion/kys_in_rest.git
cd kys_in_rest
# Пишем туда TG_TOKEN=... и другие переменные из .env.example
nano .env
# sudo apt install python3.12-venv
python3 -m venv ".venv"
source ./.venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt_tab')"
cp ./db.sqlite ./db_prod.sqlite
# Далее флоу деплоя .github/workflows/deploy.yml
```

### Обновление

[.github/workflows/deploy.yml](.github/workflows/deploy.yml)

### Грохнуть сервис

[stop-tgbot.yml](.github/workflows/stop-tgbot.yml)

[Сурс](https://chat.deepseek.com/a/chat/s/783c3446-773e-4482-80da-bf83c91a7b74)

### Стянуть бд дамп

```shell
scp leybovich-nikita@84.201.131.244:./kys_in_rest/db_prod.sqlite .
```