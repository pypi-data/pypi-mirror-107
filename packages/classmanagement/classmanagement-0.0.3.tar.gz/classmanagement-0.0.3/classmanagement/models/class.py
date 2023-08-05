from classmanagement.models.student import Student


class Class:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def print_class(self):
        print(f"Class: {self.name}")
        for v in self.students:
            print(v.to_str())


if __name__ == "__main__":
    student1 = Student("Tu")
    student2 = Student("Ten")
    ucode = Class("ucode")
    ucode.add_student(student1)
    ucode.add_student(student2)
    ucode.print_class()