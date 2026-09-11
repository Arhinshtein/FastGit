#!/usr/bin/env python3

import argparse

def main():
    # 1. Создаем парсер
    parser = argparse.ArgumentParser(description="Пример скрипта с аргументами")

    # 2. Добавляем аргументы
    parser.add_argument("name", type=str, help="Ваше имя (обязательный позиционный аргумент)")
    parser.add_argument("-a", "--age", type=int, default=18, help="Ваш возраст (необязательный аргумент)")

    # 3. Читаем аргументы из консоли
    args = parser.parse_args()

    # 4. Используем полученные данные
    print(f"Привет, {args.name}! Вам {args.age} лет.")

if __name__ == '__main__':
    main()
