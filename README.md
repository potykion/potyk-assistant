## Сетап 

### Серв

```sh
git clone https://github.com/potykion/kys_in_rest.git
cd kys_in_rest
# Пишем туда TG_TOKEN=...
nano .env
# sudo apt install python3.12-venv
python3 -m venv ".venv"
source /.venv/bin/activate
pip install -r requirements.txt
# Запуск в режиме демона
nohup python main.py > output.log 2>&1 &
# Выводит pid
```

#### Перезагрузка

```sh
kill {pid}
nohup python main.py > output.log 2>&1 &
```