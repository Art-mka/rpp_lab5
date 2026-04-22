import csv
import os

class Animal:
    # Базовый класс животного
    total = 0

    def __init__(self, id, name, breed, age):
        self.__setattr__('id', id)
        self.__setattr__('name', name)
        self.__setattr__('breed', breed)
        self.__setattr__('age', age)
        Animal.total += 1

    def __setattr__(self, name, value):
        # Контроль доступа к атрибутам с проверкой корректности
        if name == 'age' and value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if name == 'id' and value <= 0:
            raise ValueError("ID должен быть положительным")
        super().__setattr__(name, value)

    def __repr__(self):
        # Представление объекта в виде строки
        return f"{self.id}. {self.name} ({self.breed}, {self.age} лет)"

    @staticmethod
    def is_valid_age(age):
        # Проверка допустимости возраста
        return 0 <= age <= 30

class Dog(Animal):
    # Класс собаки (наследуется от Animal)
    def __init__(self, id, name, breed, age, trained=False):
        super().__init__(id, name, breed, age)
        self.trained = trained

    def sound(self):
        return f"{self.name} гавкает!"

    def __repr__(self):
        status = "дрессирована" if self.trained else "не дрессирована"
        return f"{super().__repr__()} - Собака ({status})"

class Cat(Animal):
    # Класс кошки (наследуется от Animal)
    def __init__(self, id, name, breed, age, vaccinated=False):
        super().__init__(id, name, breed, age)
        self.vaccinated = vaccinated

    def sound(self):
        return f"{self.name} мяукает!"

    def __repr__(self):
        status = "вакцинирована" if self.vaccinated else "не вакцинирована"
        return f"{super().__repr__()} - Кошка ({status})"

class Shelter:
    # Приют для животных - контейнер для хранения объектов Animal
    def __init__(self):
        self.animals = []
        self.index = 0

    def add_animal(self, animal):
        # Добавление нового животного в приют
        self.animals.append(animal)

    def load_from_csv(self, filename):
        # Заполнение приюта данными из файла
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                id = int(row["№"])
                name = row["Кличка"]
                breed = row["Порода"]
                age = int(row["Возраст"])

                # Определяем тип животного по породе
                if "овчарка" in breed.lower() or "доберман" in breed.lower():
                    animal = Dog(id, name, breed, age, age > 3)  # Дрессирована если старше 3 лет
                elif "сиамская" in breed.lower() or "персидский" in breed.lower() or "симбирская" in breed.lower():
                    animal = Cat(id, name, breed, age, age >= 2)  # Вакцинирована если 2 года или старше
                else:
                    animal = Animal(id, name, breed, age)

                self.animals.append(animal)
        print(f"Загружено {len(self.animals)} животных из {filename}")

    def save_to_csv(self, filename):
        # Экспорт данных в файл
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write("№,Кличка,Порода,Возраст,Тип\n")
            for a in self.animals:
                typ = "Собака" if isinstance(a, Dog) else "Кошка" if isinstance(a, Cat) else "Животное"
                f.write(f"{a.id},{a.name},{a.breed},{a.age},{typ}\n")
        print(f"Сохранено в {filename}")

    def __iter__(self):
        # Организация перебора животных в цикле
        self.index = 0
        return self

    def __next__(self):
        # Возврат следующего животного при переборе
        if self.index < len(self.animals):
            animal = self.animals[self.index]
            self.index += 1
            return animal
        raise StopIteration

    def __getitem__(self, i):
        # Доступ к животному по индексу (как к списку)
        return self.animals[i]

    def __len__(self):
        # Количество животных в приюте
        return len(self.animals)

    def older_than(self, min_age):
        # Генератор: возвращает животных старше указанного возраста
        for a in self.animals:
            if a.age > min_age:
                yield a

    def by_breed(self, search):
        # Генератор: возвращает животных по части названия породы
        for a in self.animals:
            if search.lower() in a.breed.lower():
                yield a

def create_test_file():
    # Создание файла с примером данных
    if not os.path.exists("data_lab4.csv"):
        with open("data_lab4.csv", "w", encoding="utf-8") as f:
            f.write("№,Кличка,Порода,Возраст\n")
            f.write("1,Барсик,Симбирская,3\n")
            f.write("2,Мурка,Сиамская,5\n")
            f.write("3,Шарик,Овчарка,2\n")
            f.write("4,Рекс,Доберман,4\n")
            f.write("5,Пушок,Персидский,1\n")
        print("Создан файл data_lab4.csv с данными из таблицы")

def main():
    # Подготовка данных
    create_test_file()
    shelter = Shelter()
    shelter.load_from_csv("data_lab4.csv")

    # Демонстрация работы итератора (перебор в цикле)
    print("\n=== ПЕРЕБОР ЖИВОТНЫХ С ПОМОЩЬЮ ИТЕРАТОРА ===")
    for i, a in enumerate(shelter):
        print(f"  {i + 1}. {a}")

    # Демонстрация переопределенного __repr__
    print("\n=== СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ ОБЪЕКТОВ ===")
    for i in range(min(3, len(shelter))):
        print(f"  {repr(shelter[i])}")

    # Демонстрация наследования (разные классы животных)
    print("\n=== РАБОТА НАСЛЕДОВАННЫХ КЛАССОВ ===")
    for a in shelter:
        if hasattr(a, 'sound'):
            print(f"  {a.sound()}")

    # Демонстрация контроля доступа через __setattr__
    print("\n=== КОНТРОЛЬ ДОСТУПА К АТРИБУТАМ ===")
    print("  При создании животных проверяется корректность возраста и ID")

    # Демонстрация доступа по индексу
    print("\n=== ДОСТУП К ЖИВОТНЫМ ПО ИНДЕКСУ ===")
    if len(shelter) > 0:
        print(f"  Первое животное: {shelter[0]}")
    if len(shelter) > 2:
        print(f"  Третье животное: {shelter[2]}")

    # Демонстрация статического метода
    print("\n=== ИСПОЛЬЗОВАНИЕ СТАТИЧЕСКОГО МЕТОДА ===")
    print(f"  Если ли животные, которым 5 лет? {Animal.is_valid_age(5)}")
    print(f"  Если ли животные, которым больше 5 лет? {Animal.is_valid_age(-1)}")

    # Демонстрация работы генераторов
    print("\n=== ГЕНЕРАТОРЫ ДЛЯ ФИЛЬТРАЦИИ ДАННЫХ ===")
    print("  Животные старше 2 лет:")
    for a in shelter.older_than(2):
        print(f"    {a}")

    print("\n  Животные с породой 'сиамская':")
    for a in shelter.by_breed("сиамская"):
        print(f"    {a}")

    # Сохранение результатов
    print("\n=== СОХРАНЕНИЕ ДАННЫХ В НОВЫЙ ФАЙЛ ===")
    shelter.save_to_csv("animals_export.csv")

if __name__ == "__main__":
    main()