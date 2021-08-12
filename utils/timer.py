from threading import Thread
from time import sleep
from typing import Callable


class CustomTimer:
    """
    Класс CustomTimer - обертка для создания функции, которая будет вызываться в потоке.

    Применение - вызов функции в потоке, которая не блокирует основной поток

    Methods
    _______
    with_timer()
        принимает функцию и вызывает ее повторно

    create_thread()
        создает поток для функции with_timer()

    """

    @staticmethod
    def with_timer(time: int, fn: Callable) -> Callable:
        """
        Возвращает вызываемый объект helper

        Parameters
        __________
        time : int
            время задержки до повторного вызова

        fn : Callable
            сюда передается функция check, которая вызывается для обновления дампа
        """
        def helper():
            fn()
            sleep(time)
            helper()
        return helper

    @staticmethod
    def create_thread(time: int, fn: Callable) -> Thread:
        """
        Принимает функцию и создает для нее поток. Параметры берутся из функции with_timer

        Parameters
        __________
        time : int

        fn : Callable
        """
        return Thread(target=CustomTimer.with_timer(time, fn))
