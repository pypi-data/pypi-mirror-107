"""Модуль **filters** содержит классы-фильтры, которые используются
функциями модуля :mod:`metrics.raw` для фильтрации курсоров по
названиям функций.
"""
from enum import Enum, auto
from clang.cindex import CursorKind

class CursorFilterInterface:
    """Интерфейс для классов-фильтров. Содержит общие методы для этих
    классов.

    """
    def filter(self, node):
        """Метод, который возвращает признак принадлежности курсора 
        какому-то критерию.

        :param node: курсор
        :type node: :class:`clang.cindex.Cursor`
        :returns: признак того, что курсор подходит критерию
        :rtype: bool
        """
        pass


class FunctionFilter(CursorFilterInterface):
    """Класс-фильтр, который фильтрует курсоры по названиям функций.

    Реализация данного класса - это машина конечных состояний (finite
    state machine), который принимает два состояния: функция не
    найдена (NO_FUNC_FOUND), функций найдена (FUNC_FOUND). От данного
    состояния зависит поведение метода *filter*.

    Помимо общего метода *filter*, в классе реализованы различные
    вспомогательные (utility) методы для получения информации об 
    фильтруемых функциях.
    """
    class State(Enum):
        """Перечисление (Enum) состояний машины конечных состояний 
        (finite state machine)"""
        NO_FUNC_FOUND = auto()
        FUNC_FOUND = auto()

    def __init__(self, func_list = None):
        """Конструктор класса, принимает *func_list*. Если не 
        передавать параметр *func_list*, то фильтр будет 
        отфильтровывать все возможные функции.

        :param list func_list: список названий функций
        """
        self._flist = func_list

        if self._flist:
            self._flist_cache = self._flist.copy()

        self._state = FunctionFilter.State.NO_FUNC_FOUND
        self._func_map = {
                FunctionFilter.State.NO_FUNC_FOUND: 
                    self._no_func_found,
                FunctionFilter.State.FUNC_FOUND: self._func_found
        }
        self._current_func_name = None
        self._is_new_func_found = False

    def _no_func_found(self, node):
        """Метод, который отвечает за поведение машины конечных 
        состояний, когда она находиться в состоянии NO_FUNC_FOUND.

        :param node: фильтруемый курсор
        :type node: :class:`clang.cindex.Cursor`
        :returns: признак того, что курсор принадлежит телу функции
        :rtype: bool
        """
        if node.kind is CursorKind.FUNCTION_DECL:
            if self._flist and node.spelling not in self._flist_cache:
                return False

            if self._flist and node.spelling in self._flist_cache:
                self._flist_cache.remove(node.spelling)

            self._current_func_name = node.spelling
            self._state = FunctionFilter.State.FUNC_FOUND
            self._is_new_func_found = True
            return True

        return False

    def _func_found(self, node):
        """Метод, который отвечает за поведение машины конечных 
        состояний, когда она находиться в состоянии FUNC_FOUND.

        :param node: фильтруемый курсор
        :type node: :class:`clang.cindex.Cursor`
        :returns: признак того, что курсор принадлежит телу функции
        :rtype: bool
        """
        if node.lexical_parent is not None \
                and node.lexical_parent.kind \
                is CursorKind.TRANSLATION_UNIT:
            self._current_func_name = None
            self._state = FunctionFilter.State.NO_FUNC_FOUND
            return self._no_func_found(node)

        self._is_new_func_found = False
        return True

    def filter(self, node):
        """Метод, который возвращает признак принадлежности курсора 
        телу функции.

        :param node: курсор
        :type node: :class:`clang.cindex.Cursor`
        :returns: признак того, что курсор принадлежит телу функции
        :rtype: bool
        """
        return self._func_map[self._state](node)

    @property
    def current_func_name(self):
        """Свойство (*string*), которое возвращает текущую фильтруемую
         функцию"""
        return self._current_func_name

    @property
    def is_new_func_found(self):
        """Признак (bool) того, что была найдена новая функция.

        Возвращаем True, если был найден курсор с объявлением функции.
        Иначе False.
        """
        return self._is_new_func_found

    def reset(self):
        """Сбрасывает фильтр в начальное состояние."""
        self._state = FunctionFilter.State.NO_FUNC_FOUND
        self._flist_cache = self._flist.copy()

