from typing import List, Literal

class Task:
    """
    Класс, представляющий задачу в диаграмме Ганта.
    """
    name: str
    start_date: float
    duration: int
    dependencies: List[str]
    end_date: float
    is_critical: bool
    status: Literal["Не начата", "В процессе", "Завершена"]

    def __init__(self, name, start_date, duration, dependencies=None):
        """
        Инициализирует объект задачи.

        Args:
            name: Название задачи.
            start_date: Дата начала задачи.
            duration: Продолжительность задачи.
            dependencies: Список зависимостей (названия задач-предшественников).
        """
        self.name = name
        self.start_date = start_date
        self.duration = duration
        self.dependencies = dependencies if dependencies is not None else []
        self.end_date = 0
        self.is_critical = False
        self.status = "Не начата"

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        """
        Проверяет и устанавливает дату окончания задачи.
        :param value:
        :return:
        """
        if value is not None and value < self.start_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        self._end_date = value