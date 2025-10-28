# Аналіз логів банківських систем з використанням ELK Stack

Практична робота для студентів з налаштування та використання ELK Stack (Elasticsearch, Logstash, Kibana) для аналізу логів банківських систем.

## Опис проекту

Цей проект створено для навчання студентів роботі з ELK Stack в контексті банківських систем. Включає:

- Повністю налаштований ELK Stack в Docker
- Генератор реалістичних логів банківських транзакцій
- Конфігурацію Logstash для обробки логів
- Приклади візуалізацій та дашбордів Kibana
- Детальний лабораторний посібник

## Особливості

- **Реалістичні дані**: Генерація різних типів банківських транзакцій (платежі, автентифікація, ATM, перекази)
- **Виявлення шахрайства**: Симуляція підозрілих транзакцій та brute force атак
- **Географічні дані**: Моніторинг транзакцій по країнах
- **Аналіз продуктивності**: Відстеження response time та метрик системи
- **Готові приклади**: Запити, візуалізації та дашборди

## Структура проекту

```
bi_log_analysis/
├── docker-compose.yml           # Конфігурація Docker для ELK Stack
├── logstash/
│   ├── config/
│   │   └── logstash.yml         # Конфігурація Logstash
│   └── pipeline/
│       └── banking-logs.conf    # Pipeline для обробки логів
├── elasticsearch/
│   └── index_template.json      # Шаблон індексу
├── logs/                        # Згеновані логи (створюється автоматично)
├── generate_logs.py             # Генератор логів
├── setup_elasticsearch.py       # Налаштування Elasticsearch
├── setup.sh / setup.bat         # Скрипти налаштування
├── cleanup.sh / cleanup.bat     # Скрипти очищення
├── practical_elk_stack.html     # Практична робота для студентів (HTML)
├── QUICK_REFERENCE.md           # Швидкий довідник
└── README.md                    # Цей файл
```

## Швидкий старт

### Вимоги

- Docker Desktop (Windows/Mac) або Docker + Docker Compose (Linux)
- Python 3.7 або новіше
- 4GB вільної RAM
- 10GB вільного місця на диску

### Встановлення та запуск

**Windows:**
```bash
# 1. Встановити залежності Python
pip install -r requirements.txt

# 2. Запустити автоматичне налаштування
setup.bat
```

**Linux/Mac:**
```bash
# 1. Встановити залежності Python
pip install -r requirements.txt

# 2. Зробити скрипт виконуваним
chmod +x setup.sh

# 3. Запустити автоматичне налаштування
./setup.sh
```

### Доступ до сервісів

Після запуску відкрийте у браузері:

- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200
- **Logstash**: http://localhost:9600

## Ручне налаштування (альтернатива)

Якщо автоматичний скрипт не спрацював:

```bash
# 1. Запустити Docker Compose
docker-compose up -d

# 2. Дочекатися запуску Elasticsearch (30-60 секунд)
# Перевірити: curl http://localhost:9200

# 3. Застосувати index template
python setup_elasticsearch.py

# 4. Згенерувати тестові логи
python generate_logs.py -n 10000

# 5. Відкрити Kibana
# http://localhost:5601
```

## Використання

### Генерація додаткових логів

```bash
# Згенерувати 10000 записів (за замовчуванням)
python generate_logs.py

# Згенерувати 50000 записів
python generate_logs.py -n 50000

# Вказати інший файл
python generate_logs.py -o logs/custom.log -n 20000
```

### Типи даних у логах

Генератор створює такі типи подій:

1. **Транзакції** (40%): Оплати через POS-термінали, онлайн-банкінг
2. **Автентифікація** (25%): Входи в систему, 2FA, біометрія
3. **ATM операції** (20%): Зняття, депозити, перевірка балансу
4. **Перекази** (10%): Внутрішні, зовнішні, міжнародні
5. **Запити балансу** (5%): Перевірка стану рахунку

### Приклади аномалій у даних

- 5% транзакцій позначені як підозрілі
- 3% спроб автентифікації - brute force атаки
- Великі транзакції (>10000)
- Невдалі високовартісні операції

## Лабораторна робота для студентів

Детальний посібник знаходиться у файлі **[practical_elk_stack.html](practical_elk_stack.html)**

**Відкрийте цей файл у браузері** - це повністю самодостатній HTML-документ з усіма необхідними інструкціями, прикладами коду та завданнями.

### Основні розділи практичної роботи:

1. **Налаштування середовища** - Docker, ELK Stack, генерація логів
2. **Розуміння даних** - структура логів, типи транзакцій
3. **Discover та KQL** - 10 запитів для пошуку та фільтрації
4. **Візуалізації** - створення 5 різних типів візуалізацій
5. **Dashboard** - побудова інтерактивного дашборду
6. **Аналітичні завдання** - виявлення шахрайства, brute force, аналіз продуктивності

**Система оцінювання:** 100 балів + 25 бонусних

## Приклади запитів KQL

```kql
# Невдалі транзакції
status: "failed"

# Підозрілі операції
suspicious: true OR is_fraud: true

# Транзакції більше 5000 USD
currency: "USD" AND amount > 5000

# Brute force атаки
is_brute_force: true

# Повільні операції
response_time_ms > 1000

# ATM операції у Києві
transaction_type: "atm" AND atm_location: "Kyiv Central"
```

## Корисні команди

### Керування Docker

```bash
# Запуск сервісів
docker-compose up -d

# Зупинка сервісів
docker-compose down

# Перегляд логів
docker-compose logs -f

# Перегляд логів конкретного сервісу
docker-compose logs -f logstash

# Перезапуск сервісу
docker-compose restart kibana

# Статус контейнерів
docker-compose ps
```

### Робота з Elasticsearch

```bash
# Перевірка здоров'я кластера
curl http://localhost:9200/_cluster/health?pretty

# Список індексів
curl http://localhost:9200/_cat/indices?v

# Статистика індексу
curl http://localhost:9200/banking-logs-*/_stats?pretty

# Видалення всіх даних
curl -X DELETE http://localhost:9200/banking-logs-*
```

## Очищення

**Windows:**
```bash
cleanup.bat
```

**Linux/Mac:**
```bash
chmod +x cleanup.sh
./cleanup.sh
```

Скрипт очищення запитає:
- Зупинити контейнери
- Видалити volumes (дані Elasticsearch)
- Видалити згеновані логи

## Архітектура

```
┌─────────────────┐
│  Banking App    │
│  (Log Generator)│
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │  Logs  │ (JSON files)
    └───┬────┘
        │
        ▼
┌───────────────┐
│   Logstash    │ ◄── Parse, Filter, Transform
│   Pipeline    │     - Geo IP lookup
└───────┬───────┘     - Anomaly detection
        │             - Field enrichment
        ▼
┌───────────────┐
│ Elasticsearch │ ◄── Index, Store, Search
│               │     - Full-text search
└───────┬───────┘     - Aggregations
        │
        ▼
┌───────────────┐
│    Kibana     │ ◄── Visualize, Analyze
│               │     - Dashboards
└───────────────┘     - Alerts
```

## Технології

- **Elasticsearch 8.11.0**: Пошук та аналітика
- **Logstash 8.11.0**: Обробка логів
- **Kibana 8.11.0**: Візуалізація
- **Docker & Docker Compose**: Контейнеризація
- **Python 3**: Генерація даних

## Troubleshooting

### Kibana не запускається

```bash
# Перевірте логи
docker-compose logs kibana

# Перезапустіть
docker-compose restart kibana
```

### Дані не відображаються

1. Перевірте, чи створено data view
2. Встановіть правильний time range (Last 7 days)
3. Перевірте індекси: `curl http://localhost:9200/_cat/indices?v`

### Недостатньо пам'яті

Зменшіть виділену пам'ять у `docker-compose.yml`:

```yaml
environment:
  - "ES_JAVA_OPTS=-Xms256m -Xmx256m"  # Замість 512m
```

### Логи не обробляються Logstash

```bash
# Перевірте логи Logstash
docker-compose logs logstash

# Перевірте наявність файлів
ls -la logs/

# Перезапустіть Logstash
docker-compose restart logstash
```

## Розширення проекту

Ідеї для покращення:

1. **Інтеграція з реальними додатками**: Підключити логування з реального банківського додатку
2. **Machine Learning**: Використати Elastic ML для виявлення аномалій
3. **Alerts**: Налаштувати email/Slack нотифікації
4. **Security**: Додати аутентифікацію та SSL
5. **Масштабування**: Налаштувати Elasticsearch кластер з кількома нодами
6. **Beats**: Використати Filebeat замість прямого читання файлів

## Додаткові ресурси

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [ELK Stack Tutorial](https://www.elastic.co/what-is/elk-stack)
- [KQL Query Syntax](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)

## Ліцензія

Цей проект створено для освітніх цілей.

## Автор

Створено для курсу "Banking Information Technology"

## Підтримка

Для питань та проблем створіть issue у репозиторії.
