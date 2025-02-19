# Описание Основных деталей реализации интерпретатора

## Типы данных
 - строка
 - регулярное выражение
 - конечный автомат

## Приведение типов
 - строка -> целое число при вычислении арифметических выражений

 При вычислении теоретико-множественных операций с формальными языками
  - строка -> регулярное выражение -> конечный автомат

## Представление данных в интерпретаторе
 - Имеется глобальная память и стек для работы с лямбда выражениями
 - Значения хранятся и передаются в классе MemBox

## Алгоритмы
 - Для выполнения теоретико-множественных операций над языками используются комбинации средств библиотеки pyformlang
 - Для вычисления результатов преобразования конечного автомата используются алгоритмы из задания 11

## Проверка типов и ошибки
 - При возникновении ошибки фиксируется ее текст и собирается "backtrace" до исполняемого statement (оператора). В классе интерпретатора данная информация обрабатывается и выводится на экран
 - Типы подвыражений проверяются на соответствие ожиданиям надвыражений, при несоответствии генерируется исключение
