

class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Employee:
    def __init__(self, code, name, salary, direct=True):
        self.code = code
        self.name = name
        self.salary = salary

        # class not directly initialized
        if direct:
            raise TypeError

    def calc_bonus(self):
        pass

    def get_hours(self):
        return 8


class Manager(Employee):
    def __init__(self, code, name, salary, direct=False):
        super().__init__(code, name, salary, direct=False)
        self.__department = Department('managers', 1)

    def get_department(self):
        return(self.__department.name)

    def set_department(self, new_department, code):
        self.__department = Department(new_department, code)

    def calc_bonus(self):
        return self.salary * 0.15


class Seller(Manager):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary)
        self.__department = Department('sellers', 2)
        self.__sales = 0

    def get_department(self):
        return self.__department.name

    def set_department(self, new_department, code):
        self.__department = Department(new_department, code)

    def get_sales(self):
        return(self.__sales)

    def put_sales(self, new_sale):
        self.__sales += new_sale

    def calc_bonus(self):
        return self.__sales * 0.15

    def get_hours(self):
        return 8
