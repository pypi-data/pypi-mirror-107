"""Модуль **halstead** содержит функции для расчета метрик Холстеда 
файлов.

Главные функции модуля: :func:`analyze_file`, :func:`analyze_files`. 
Только эти функции должны использоваться для расчета метрик.
"""
from metrics import parser
from enum import Enum
from enum import auto
from clang.cindex import CursorKind
from clang.cindex import TypeKind
from clang.cindex import TokenKind
import clang.cindex
from metrics import filters
import collections
import os

#: Объект BasicHalsteadMetrics, в полях объекта хранятся базовые 
#: метрики Холстеда.
#:
#: Объект BasicHalsteadMetrics - это :func:`collections.namedtuple` c
#: полями для хранения базовых показателей метрик Холстеда. Данный 
#: объект возвращается функциями для расчета метрик.
#:
#: :Поля объекта:
#:    * n1 (*int*) - количество уникальных операторов
#:    * n1 (*int*) - количество уникальных операндов
#:    * N1 (*int*) - общее количество операторов
#:    * N2 (*int*) - общее количество операндов
#:
BasicHalsteadMetrics = collections.namedtuple('BasicHalsteadMetrics',
        ['n1', 'n2', 'N1', 'N2']
)

def _is_operand(node):
    """Функция возвращает признак того, что курсор является операндом.

    :param node: курсор
    :type node: :class:`clang.cindex.Cursor`
    :returns: признак
    :rtype: bool
    """
    # Если курсор является оператором sizeof, привязка возвращает 
    # CursorKind.OBJC_STRING_LITERAL для оператора sizeof по странным 
    # причинам. 
    if node.kind is CursorKind.OBJC_STRING_LITERAL:
        child = next(node.get_children())
        if child.kind is CursorKind.TYPE_REF:
            return True
        return False

    if node.kind in [CursorKind.VAR_DECL, CursorKind.LABEL_STMT,
            CursorKind.DECL_REF_EXPR, CursorKind.MACRO_INSTANTIATION,
            CursorKind.INTEGER_LITERAL, CursorKind.STRING_LITERAL,
            CursorKind.PARM_DECL, CursorKind.STRUCT_DECL, 
            CursorKind.FIELD_DECL, CursorKind.MEMBER_REF_EXPR, 
            CursorKind.FLOATING_LITERAL, CursorKind.CSTYLE_CAST_EXPR,
            CursorKind.GOTO_STMT]:
        return node.type.kind is not TypeKind.FUNCTIONPROTO

    return False


def _get_operand_spelling(node, current_func_name=None):
    """Функция возвращает название операнда для указанного курсора 
    (*node*), если курсор является операндом.

    Параметр *current_func_name* используется для того, чтобы добавить квалификатор перед названием операнда в случае, если операнд является переменной. Это позволяет учитывать переменные для разных функций как уникальные операнды.

    :param node: курсор
    :type node: :class:`clang.cindex.Cursor`
    :param current_func_name: название текущей функции, в которой находимся при прохождении (None, если обходим курсор, который не находится в какой-либо функции)
    :type current_func_name: string
    :returns: название операнда
    :rtype: string
    """
    if current_func_name and node.kind in [CursorKind.VAR_DECL, 
            CursorKind.DECL_REF_EXPR, CursorKind.PARM_DECL]:
        return current_func_name + '::' + node.spelling

    if node.kind is CursorKind.OBJC_STRING_LITERAL:
        child = next(node.get_children())
        return child.spelling

    if node.kind is CursorKind.CSTYLE_CAST_EXPR:
        return node.type.spelling

    if node.kind is CursorKind.GOTO_STMT:
        return list(node.get_tokens())[1].spelling

    if node.kind in [CursorKind.INTEGER_LITERAL, 
            CursorKind.FLOATING_LITERAL]:
        literal_token = list(node.get_tokens())[0]
        return literal_token.spelling
    else:
        return node.spelling


def _is_operator(node):
    """Функция возвращает признак того, что курсор является оператором.

    :param node: курсор
    :type node: :class:`clang.cindex.Cursor`
    :returns: признак
    :rtype: bool
    """
    #print(node.kind, ' ', node.spelling, ' ', node.get_definition())
    if node.kind in [CursorKind.CALL_EXPR, CursorKind.FUNCTION_DECL,
            CursorKind.VAR_DECL, CursorKind.DO_STMT, 
            CursorKind.GOTO_STMT, CursorKind.FOR_STMT,
            CursorKind.WHILE_STMT, CursorKind.BREAK_STMT, 
            CursorKind.CONTINUE_STMT, CursorKind.RETURN_STMT,
            CursorKind.IF_STMT, CursorKind.SWITCH_STMT, 
            CursorKind.CASE_STMT, CursorKind.DEFAULT_STMT, 
            CursorKind.INDIRECT_GOTO_STMT, 
            CursorKind.BINARY_OPERATOR, CursorKind.UNARY_OPERATOR,
            CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.PARM_DECL, 
            CursorKind.STRUCT_DECL, CursorKind.FIELD_DECL,
            CursorKind.MEMBER_REF_EXPR, CursorKind.CSTYLE_CAST_EXPR,
            CursorKind.OBJC_STRING_LITERAL, CursorKind.LABEL_STMT]:
        return True
    return False


class IfKind(Enum):
    """Перечисление, которое хранит вид утверждения (statement) IF.

    Перечисление может хранить одно из следующих значений:

       * **IF** - утверждение вида if-then
       * **IF_ELSE** - утвеждение вида if-then-else
    """
    IF = 'if'
    IF_ELSE = 'if_else'


# Используется функцией _get_operator_spelling, для возврата названия 
# оператора sizeof
SIZEOF = 'sizeof'
# Используется функцией _get_operator_spelling, для возврата названия 
# оператора присваивания
ASSIGN_OPERATOR = '='

def _get_operator_spelling(node):
    """Функция возвращает название оператора для указанного курсора 
    (*node*), если курсор является оператором.

    Возвращает результат разных типов, однако подсчитать уникальные 
    операторы все равно можно, даже если названия будут храниться в 
    разных форматах.

    :param node: курсор
    :type node: :class:`clang.cindex.Cursor`
    :returns: название оператора
    :rtype: string
    """
    # Если курсор является оператором sizeof, привязка возвращает 
    # CursorKind.OBJC_STRING_LITERAL для оператора sizeof по странным 
    # причинам. 
    if node.kind is CursorKind.OBJC_STRING_LITERAL:
        return SIZEOF

    if node.kind is CursorKind.VAR_DECL:
        for t in node.get_tokens():
            if t.kind is TokenKind.PUNCTUATION \
                    and t.spelling == ASSIGN_OPERATOR:
                return (node.type.spelling, ASSIGN_OPERATOR)
        return node.type.spelling

    if node.kind in [CursorKind.VAR_DECL, CursorKind.PARM_DECL, 
            CursorKind.FIELD_DECL]:
        return node.type.spelling

    if node.kind in [CursorKind.INDIRECT_GOTO_STMT, 
            CursorKind.GOTO_STMT]:
        return CursorKind.GOTO_STMT

    if node.kind in [CursorKind.DO_STMT, CursorKind.FOR_STMT,
            CursorKind.WHILE_STMT, CursorKind.BREAK_STMT, 
            CursorKind.CONTINUE_STMT, CursorKind.RETURN_STMT,
            CursorKind.SWITCH_STMT, CursorKind.CASE_STMT, 
            CursorKind.DEFAULT_STMT, 
            CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.STRUCT_DECL,
            CursorKind.CSTYLE_CAST_EXPR, CursorKind.LABEL_STMT]:
        return node.kind

    if node.kind is CursorKind.IF_STMT:
        if len(list(node.get_children())) > 2:
            return IfKind.IF_ELSE
        else:
            return IfKind.IF

    if node.kind is CursorKind.BINARY_OPERATOR:
        children_list = list(node.get_children())
        left_offset = len(list(children_list[0].get_tokens()))
        op = list(node.get_tokens())[left_offset].spelling
        return op

    if node.kind is CursorKind.UNARY_OPERATOR:
        op_format_string = '%s (unary)'
        for t in node.get_tokens():
            if t.kind is TokenKind.PUNCTUATION:
                op = op_format_string % t.spelling
        return op

    if node.kind is CursorKind.MEMBER_REF_EXPR:
        for t in node.get_tokens():
            if t.kind is TokenKind.PUNCTUATION:
                return t.spelling

    return node.spelling


def _add_operators_from_tokens(tokens, operators):
    """Подсчитывает количество различных разделителей по указанному 
    списку токенов.

    Добавляет количество разделителей в словарь *operators*. 
    Разделители (``,``, ``;``, ``{`` (составной оператор)) добавляются в 
    словарь парами ключ:значение (название_разделителя:
    количество_вхождений).

    :param tokens: список токенов, который получается из курсора методом :meth:`clang.cindex.Cursor.get_tokens`
    :type tokens: функция-генератор, которую возвращает :class:`clang.cindex.Token`
    :param operators: словарь операторов
    :type operators: dict
    """
    for t in tokens:
        if t.kind is TokenKind.PUNCTUATION \
                and t.spelling in ['{', ';', ',']:
            if t.spelling in operators:
                operators[t.spelling] += 1
            else:
                operators[t.spelling] = 1


def _analyze(cursor):
    operands = {}
    operators = {}

    # Вспомогательная функция для избежания повторного кода. 
    # Подсчитывает оператор или операнд по его названию. То есть 
    # добавлять +1 к значению в словаре *d* по ключу *spelling*.
    def _add_spelling(spelling, d):
        if spelling in d:
            d[spelling] += 1
        else:
            d[spelling] = 1

    ffilter = filters.FunctionFilter()

    # Функция обратного вызова, которая передается в метод 
    # traverse_ast. Подсчитывает каждый узел как операнд или оператор.
    def _halstead_callback(node, parent):
        nonlocal operands, ffilter
        ffilter.filter(node)

        if _is_operand(node):
            spelling = _get_operand_spelling(node, 
                    ffilter.current_func_name)
            _add_spelling(spelling, operands)
        
        if _is_operator(node):
            spelling = _get_operator_spelling(node)

            if isinstance(spelling, tuple):
                for s in spelling:
                    _add_spelling(s, operators)
            else:
                _add_spelling(spelling, operators)
            
    parser.ClangSingleFileParser.traverse_ast(cursor, 
            _halstead_callback)

    _add_operators_from_tokens(cursor.get_tokens(), operators)

    return BasicHalsteadMetrics(
            len(operators.keys()), len(operands.keys()),
            sum(operators.values()), sum(operands.values())
            )


def analyze_file(source_filepath):
    """Функция подсчитывает базовые метрики Холстеда для файла с 
    указанным путем *source_filepath*.

    Функция возвращает объект :obj:`BasicHalsteadMetrics` с 
    подсчитанными базовыми метриками для указанного файла.

    :param source_filepath: абсолютный путь к файлу
    :type source_filepath: string
    :returns: базовые метрики Холстеда файла
    :rtype: :obj:`BasicHalsteadMetrics`
    """
    # парсить комментарии не требуется
    cparser = parser.ClangSingleFileParser(parser.Option.PARSE_MACROS)
    cursor = cparser.parse(source_filepath)
    return _analyze(cursor)


def analyze_code(filename, source_code):
    """Функция подсчитывает базовые метрики Холстеда для исходного кода, 
    который хранится в памяти.

    Параметр *filename* используется для того, чтобы привязать код из памяти к имени файла.

    Функция возвращает объект :obj:`BasicHalsteadMetrics` с 
    подсчитанными базовыми метриками для исходного кода.

    :param source_filepath: абсолютный путь к файлу
    :type source_filepath: string
    :returns: базовые метрики Холстеда файла
    :rtype: :obj:`BasicHalsteadMetrics`
    """
    # парсить комментарии не требуется
    cparser = parser.ClangSingleFileParser(
            parser.Option.PARSE_MACROS | parser.Option.PARSE_COMMENTS)
    cursor = cparser.parse_from_memory(filename, source_code)
    return _analyze(cursor)


def analyze_files(source_files):
    """Функция подсчитывает базовые метрики Холстеда для нескольких 
    файлов с указанными путями *source_filepath*.

    Функция возвращает словарь (*dict*) 
    объектов :obj:`BasicHalsteadMetrics` с подсчитанными базовыми 
    метриками для указанных файлов.

    :param source_files: список абсолютных путей к файлам
    :type source_files: list
    :returns: словарь базовых метрик Холстеда файлов ({название файла::obj:`BasicHalsteadMetrics`})
    :rtype: dict
    """
    common_prefix = os.path.commonprefix(source_files)
    return { os.path.relpath(fp, common_prefix):analyze_file(fp) 
            for fp in source_files }

