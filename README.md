# Salary Reporter

Скрипт для формирования отчетов по заработной плате сотрудников на основе CSV-файлов.

## Особенности

- Чтение данных из нескольких CSV-файлов
- Поддержка разных названий колонок для ставки (hourly_rate, rate, salary)
- Формирование отчета `payout` с группировкой по отделам
- Расширяемая архитектура для добавления новых отчетов

## Требования

- Python 3.8+
- Зависимости: `pip install -r requirements.txt`

## Использование

```bash
python3 main.py file1.csv file2.csv file2.csv --report payout


Пример вывода отчета payout
Marketing
------------------Alice Johnson           160        50.0      $8,000.00
------------------Bob Smith               150        40.0      $6,000.00
------------------------------------------300                  $14,000.00


Формат входных файлов


<ul>
Обязательные колонки:
<li>name - имя сотрудника</li>
<li>department - отдел</li>
<li>hours_worked - отработанные часы</li>
<li>Одна из колонок для ставки: hourly_rate, rate или salary</li>
</ul>

Пример CSV:
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50


## Добавление новых отчетов

Создайте класс отчета унаследованный от BaseReport
Реализуйте методы:
1. name - идентификатор отчета
2. generate() - логика формирования отчета
3. Зарегистрируйте отчет в ReportManager

Пример отчета:
class ExampleReport(BaseReport):
    @property
    def name(self) -> str:
        return "example"

    def generate(self, data) -> str:
        return "Пример отчета"


##Тестирование
pytest tests/ -v
