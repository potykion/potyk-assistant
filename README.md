# `kys_in_rest`

> Телеграм бот, показывающий где поесть в Москве

- [Бот](https://t.me/kys_in_rest_bot)
- [Github](https://github.com/potykion/kys_in_rest)

## Сетап 

### Серв

```sh
ssh -l leybovich-nikita 84.201.131.244
git clone https://github.com/potykion/kys_in_rest.git
cd kys_in_rest
# Пишем туда TG_TOKEN=...
nano .env
# sudo apt install python3.12-venv
python3 -m venv ".venv"
source ./.venv/bin/activate
pip install -r requirements.txt
# Запуск в режиме демона
nohup python main.py > output.log 2>&1 &
# Выводит pid
```

#### Обновление

```sh
ssh -l leybovich-nikita 84.201.131.244
cd kys_in_rest
git pull
source ./.venv/bin/activate
# pgrep -f "python main.py" + kill
pkill -f "python main.py" 
nohup python main.py > output.log 2>&1 &
```

#### Грохнуть сервис

```sh
ssh -l leybovich-nikita 84.201.131.244
cd kys_in_rest
source ./.venv/bin/activate
pkill -f "python main.py" 
```

[Сурс](https://chat.deepseek.com/a/chat/s/783c3446-773e-4482-80da-bf83c91a7b74)