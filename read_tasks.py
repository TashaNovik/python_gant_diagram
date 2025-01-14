import json
import csv
from typing import List, Dict, Any

from task import Task
def load_tasks(filepath: str) -> List[Task]:
    """
    Определяет формат файла (CSV или JSON) по расширению и вызывает соответствующую функцию чтения.

    Args:
        filepath: Путь к файлу с задачами.

    Returns:
        Список объектов Task.

    Raises:
        ValueError: Если формат файла не поддерживается.
        FileNotFoundError: Если файл не найден.
        Exception:  В случае прочих ошибок при чтении файла
    """
    if filepath.endswith('.csv'):
        return read_tasks_from_csv(filepath)
    elif filepath.endswith('.json'):
        return read_tasks_from_json(filepath)
    else:
        raise ValueError("Неподдерживаемый формат файла. Используйте CSV или JSON.")

def _create_task_from_dict(data: Dict[str, Any]) -> Task:
    """
    Вспомогательная функция для создания объекта Task из словаря.

    Args:
        data: Словарь с данными задачи.

    Returns:
        Объект Task.

    Raises:
        ValueError: Если данные не корректны.
    """
    try:
        # Проверяем типы данных
        name = str(data['name'])
        start_date = float(data['start_date'])
        duration = int(data['duration'])

        # Получаем и обрабатываем зависимости
        dependencies_str = data.get('dependencies', '')
        if isinstance(dependencies_str, list):
          dependencies = [str(dep).strip() for dep in dependencies_str]
        elif isinstance(dependencies_str, str):
          dependencies = [dep.strip() for dep in dependencies_str.split(';') if dependencies_str]
        else:
          dependencies = []

        return Task(name=name, start_date=start_date, duration=duration, dependencies=dependencies)
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Некорректные данные для задачи: {data}. Ошибка: {e}")

def read_tasks_from_csv(filepath: str) -> List[Task]:
    """
    Читает задачи из CSV файла и возвращает список объектов Task.

    Args:
        filepath: Путь к CSV файлу.

    Returns:
        Список объектов Task.

    Raises:
        FileNotFoundError: Если файл не найден.
        csv.Error: Если возникла ошибка при чтении CSV файла.
        ValueError: Если данные в файле не корректны.
    """
    tasks: List[Task] = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            try:
                task = _create_task_from_dict(row)
                tasks.append(task)
            except ValueError as e:
                print(f"Ошибка при обработке строки: {row}. {e}")
    return tasks

def read_tasks_from_json(filepath: str) -> List[Task]:
    """
    Читает задачи из JSON файла и возвращает список объектов Task.

    Args:
        filepath: Путь к JSON файлу.

    Returns:
        Список объектов Task.

    Raises:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: Если возникла ошибка при чтении JSON файла.
        ValueError: Если данные в файле не корректны.
    """
    tasks: List[Task] = []
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON файл должен содержать список задач.")
            for item in data:
                task = _create_task_from_dict(item)
                tasks.append(task)
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении JSON файла: {e}")
        except ValueError as e:
            print(f"Ошибка при обработке данных из JSON файла: {e}")
    return tasks

if __name__ == '__main__':
    # Пример использования:
    try:
        tasks = load_tasks("tasks.csv")  # Или tasks.json
        print(tasks[0].name)
        print(tasks[0].start_date)
        print(tasks[0].duration)
        print(tasks[0].dependencies)
    except FileNotFoundError:
        print("Файл не найден.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")