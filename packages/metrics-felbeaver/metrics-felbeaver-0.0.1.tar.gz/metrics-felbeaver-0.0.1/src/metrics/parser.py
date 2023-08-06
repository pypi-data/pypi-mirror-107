"""Модуль **parser** содержит классы парсеров исходного кода. Классы
являются обертками для функций привязки Clang из модуля 
:mod:`clang.cindex`
"""
import clang.cindex
from enum import IntFlag

class Option(IntFlag):
    """Перечисление флагов для установки опций парсера."""
    PARSE_MACROS = 0b01
    PARSE_COMMENTS = 0b10


class ClangSingleFileParser:    
    """Класс парсера, который может парсить только один файл исходного кода.

    Опции парсера можно задать при помощи флагов :class:`Option`. Взаимодействие с файлом происходит при помощи статического метода :meth:`traverse_ast`, который обходит абстрактного синтаксическое дерево и вызывает функцию обратного вызова для каждого узла.
     """
    def __init__(self, options = Option(0)):
        """Конструктор класса, опции парсера задаются при помощи 
        параметра *options*.

        :param options: параметра парсера (Option.PARSE_MACROS - позволяет парсить объявления макросов, Option.PARSE_COMMENTS - позволяет получать комментарии для узлов AST)
        :type options: :class:`Option`
        """
        self._idx = clang.cindex.Index.create()
        self._opts = 0
        self._args = ['--std=c99']

        self.macros_parsing_enabled = Option.PARSE_MACROS in options
        self.comments_parsing_enabled = Option.PARSE_COMMENTS in options

    def _add_argument(self, arg):
        if arg not in self._args:
            self._args.append(arg)

    def _remove_argument(self, arg):
        try:
            self._args.remove(arg)
        except ValueError:
            pass

    @property
    def comments_parsing_enabled(self):
        """Свойство (bool), возвращает признак того, что опция 
        парсинга комментариев включена.
        """
        return self._is_comments_parsing_enabled

    @comments_parsing_enabled.setter
    def comments_parsing_enabled(self, value):
        """Сеттер для свойства, позволяет включать (True) и выключать
         (False) опцию парсинга комметариев.
         """
        self._is_comments_parsing_enabled = bool(value) 

        if self._is_comments_parsing_enabled:
            self._opts |= clang.cindex.TranslationUnit \
                        .PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION
            for arg in ['-Wdocumentation', '-fparse-all-comments']:
                self._add_argument(arg)
        else:
            self._opts &= ~clang.cindex.TranslationUnit \
                        .PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION
            for arg in ['-Wdocumentation', '-fparse-all-comments']:
                self._remove_argument(arg)

    @property
    def macros_parsing_enabled(self):
        """Свойство (bool), возвращает признак того, что опция 
        парсинга макросов включена."""
        return self._is_macros_parsing_enabled

    @macros_parsing_enabled.setter
    def macros_parsing_enabled(self, value):
        """Сеттер для свойства, позволяет включать (True) и выключать
         (False) опцию парсинга макросов.
         """
        self._is_macros_parsing_enabled = bool(value)

        if self._is_macros_parsing_enabled:
            self._opts |= clang.cindex.TranslationUnit \
                            .PARSE_DETAILED_PROCESSING_RECORD
        else:
            self._opts &= ~clang.cindex.TranslationUnit \
                            .PARSE_DETAILED_PROCESSING_RECORD

    def parse_from_memory(self, filename, source_code):
        """Метод, который позволяет получить курсор корневого узла
        абстрактного синтаксического дерева (AST) для указанного 
        исходного кода, который хранится в памяти. Параметр *filename* 
        используется для того, чтобы привязать код к имени.

        :param str source_code: исходный код в памяти
        :param str filename: имя файла исходного кода
        :returns: курсор
        :rtype: :class:`clang.cindex.Cursor`
        """
        self._tu = self._idx.parse(filename, args=self._args, 
                unsaved_files=[(filename, source_code)],
                options=self._opts)
        self._cursor = self._tu.cursor

        return self._cursor

    def parse(self, source_file_path):
        """Метод, который позволяет получить курсор корневого узла
        абстрактного синтаксического дерева (AST) для указанного 
        файла с исходным кодом.

        :param source_file_path: абсолютный путь к файлу
        :type source_file_path: string
        :returns: курсор
        :rtype: :class:`clang.cindex.Cursor`
        """
        self._tu = self._idx.parse(source_file_path, args=self._args,
                options=self._opts)
        self._cursor = self._tu.cursor

        return self._cursor

    @staticmethod
    def traverse_ast(cursor, callback, parent=None):
        """Статический метод, который обходит абстрактное 
        синтаксическое дерево (AST) и вызывает функцию обратного 
        вызова (callback) для каждого узла.

        Метод делает рекурсивный проход дерева в глубину. Изначально
        в метод необходимо передать курсор, который является корнем 
        абстрактного синтаксического дерева.

        :param cursor: корень AST
        :type cursor: :class:`clang.cindex.Cursor`
        :param callback: функция обратного вызова
        :param parent: необходим для рекурсивного обхода, в данный параметр передается родительский узел
        :type parent: :class:`clang.cindex.Cursor`
        """
        callback(cursor, parent)

        for c in cursor.get_children():
            if clang.cindex.conf.lib.clang_Location_isFromMainFile(
                    c.location):
                ClangSingleFileParser.traverse_ast(
                        c, callback, cursor)


class ClangMultipleFilesParser(ClangSingleFileParser):
    """Класс парсера, который может парсить несколько файлов исходного кода.

    Опции парсера можно задать при помощи флагов :class:`Option`. Взаимодействие с файлом происходит при помощи метода :meth:`traverse_ast`, который обходит абстрактного синтаксическое дерево для каждого файла и вызывает функцию обратного вызова для каждого узла.
     """
    def __init__(self, options = Option(0)):
        """Конструктор класса, опции парсера задаются при помощи 
        параметра *options*.

        :param options: параметра парсера (Option.PARSE_MACROS - позволяет парсить объявления макросов, Option.PARSE_COMMENTS - позволяет получать комментарии для узлов AST)
        :type options: :class:`Option`
        """
        self._tus = []
        self._paths = []
        ClangSingleFileParser.__init__(self, options)
        
    def parse(self, source_files):
        """Метод, который позволяет запомнить курсоры корневых узлов 
        AST для каждого указанного файла с исходным кодом.

        :param source_file_path: список абсолютных путей к файлу
        :type source_file_path: list
        """
        for fp in source_files:
            if fp not in self._paths:
                self._paths.append(fp)
                ClangSingleFileParser.parse(self, fp)
                self._tus.append(self._tu)

    def traverse_ast(self, callback):
        """Метод, который обходит абстрактное синтаксическое дерево 
        (AST) для каждого запомненого курсора и вызывает функцию 
        обратного вызова (callback) для каждого узла. Метод делает 
        рекурсивный проход дерева в глубину. 

        :param callback: функция обратного вызова
        """
        for tu in self._tus:
            ClangSingleFileParser.traverse_ast(tu.cursor, callback)

