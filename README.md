# Инструкция к запуску 
1. Создать виртуальную среду:  python -m venv venv 
2. Активировать виртуальную среду:  Linux/Mac: source venv/bin/activate; Windows : venv\Scripts\activate.bat или venv\Scripts\activate 
3. Установить библиотеки в виртуальную среду pip install -r requirements.txt
4. Если не тестовый режим, то поднять докер контейнер с образом mongo db если ее нет на ПК командой docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server
5. Поставить DEBUG_MODE. True если нет датчиков, False если есть.SECONDS_STEP отвечает за интервал мониторинга системы  в секундах. 
6. Запустить команду python main.py из под созданной в п.1 виртуальной среды. Программа запустится на порту 8000.