import mysql.connector
from helper import read_db_config


#два класи ексепшинів ікі викликаються при спробах додати учня/ робітника які вже зараховані/у штаті школи
class AlreadyInSchoolStaffError(Exception):
    pass

class AlreadyInSchoolError(Exception):
    pass


#Оголошуємо клас Person який буде батьківським для класу шкільного робітника та учня
class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


#Оголошуємо клас шкільний робітник який успадкував від класу Person init метод плюс отримав кілька нових атрибутів і методів
class School_Worker(Person):
    def __init__(self, name, surname, position: str, salary: int):
        super().__init__(name, surname)
        self.position = position
        self.salary = salary



    def __repr__(self):
        return f"{self.name} {self.surname} {self.position} {self.salary}"
        # .format(self.name,self.surname, self.position, self.salary)

#Оголошуємо клас Учень Школи який успадкував від класу Person init метод
class School_Student(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __repr__(self):
        return f"{self.name} {self.surname} "


#клас школа
class School():
    def __init__(self, school_name: str, school_capacity: int, school_payment: int) :
        self.school_name = school_name
        self.school_capacity = school_capacity
        self.school_payment = school_payment


    # метод класу школа що описує прийом робітників на роботу
    def hire_school_worker(self, worker: School_Worker):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()

        sqlquery = (f'''SELECT * FROM school_workers WHERE NAME = '{worker.name}'AND SURNAME = '{worker.surname}'AND POSITION = '{worker.position}' AND SALARY = '{worker.salary}' ''')
        cursor.execute(sqlquery)
        res = cursor.fetchone()
        if res == None:
            cursor.execute(f'''INSERT INTO school_workers(
                           NAME, SURNAME, POSITION, SALARY)
                           VALUES ('{worker.name}', '{worker.surname}', '{worker.position}', '{worker.salary}')''')
            db_connector.commit()
        else:
            raise AlreadyInSchoolStaffError("Worker already in school stuff")


        db_connector.close()

    # метод класу школа що описує звільнення робітників зі школи
    def fire_school_worker(self, worker: School_Worker):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()
        cursor.execute(f'''DELETE FROM school_workers WHERE NAME = '{worker.name}'AND SURNAME = '{worker.surname}'AND POSITION = '{worker.position}' AND SALARY ='{worker.salary}' ''')
        db_connector.commit()
        db_connector.close()

    # метод класу школа що описує прийом учнів у школу
    def accept_school_student(self, student: School_Student, class_id : int, class_name: str):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()
        sqlquery = (f'''SELECT * FROM school_students WHERE NAME = '{student.name}'AND SURNAME = '{student.surname}' ''')
        cursor.execute(sqlquery)
        res = cursor.fetchone()
        if res == None:
            cursor.execute(f'''INSERT INTO school_students(
                   NAME, SURNAME, CLASS_ID, CLASS_NAME)
                   VALUES ('{student.name}', '{student.surname}', '{class_id}', '{class_name}')''')
            db_connector.commit()
        else:
            raise AlreadyInSchoolError("Student is already in school")

        db_connector.close()

    # метод класу школа що описує відрахування учнів зі школи
    def exclude_student(self, student: School_Student, class_id : int, class_name: str):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()
        cursor.execute(f'''DELETE FROM school_students WHERE NAME = '{student.name}'AND SURNAME = '{student.surname}' AND CLASS_ID = '{class_id}' AND CLASS_NAME = '{class_name}' ''')
        db_connector.commit()
        db_connector.close()

    # описуємо додаткову пропертю зі значенням зарплатного бюджету школи
    @property
    def school_salary_budget(self):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()
        cursor.execute(f'''SELECT SUM(SALARY) FROM school_workers''')
        salaries = cursor.fetchone()[0]
        db_connector.close()
        return salaries

    # описуємо додаткову пропертю яка визначатиме скільки учнів навчається у школі
    @property
    def num_of_school_students(self):
        db_config = read_db_config()
        db_connector = mysql.connector.connect(**db_config)
        cursor = db_connector.cursor()
        cursor.execute(f'''SELECT COUNT(*) FROM school_students''')
        num_students = cursor.fetchone()[0]
        db_connector.close()
        return num_students

    # оголошуємо метод визначення чи прибуткова школа
    def school_revenue(self):
        revenue = (self.school_payment * self.num_of_school_students) - self.school_salary_budget
        if revenue <0:
            return ('Школа збиткова, недостача бюджету становить: ', int(revenue), 'щоб почати заробляти учнів повинно бути більше :', int(self.school_salary_budget/self.school_payment))
        else:
            return ('Школа прибуткова, пибуток становить: ', int(revenue))



if __name__ == "__main__":

    #оголошуємо школу
    qwerty = School("Перша приватна львівська школа",300,3000)

    # показуємо необхідний зарплатний бюджет для школи
    print("school budget is", qwerty.school_salary_budget)

    # показуємо кілкість учнів у школі:
    print("Students at school", qwerty.num_of_school_students)

    # визначаємо чи прибуткова школа
    print(qwerty.school_revenue())

    # оголошуємо нового працівника і приймаємо його на роботу
    d = School_Worker("Galya", "Lysion", "Cleaner", 7000)
    qwerty.hire_school_worker(d)
    print("school budget changed to:", qwerty.school_salary_budget)

    # визначаємо як змінилась прибутковість школи від цього
    print(qwerty.school_revenue())

    #додаємо у школу нового студента і визначаємо як ще вплинуло на прибутковість
    c5 = School_Student("Igor", "Tkachenkо")
    qwerty.accept_school_student(c5, class_id = 1, class_name = '1a')
    print("school students changed to", qwerty.num_of_school_students)
    print(qwerty.school_revenue())
