class Student:
    def __init__(self, name):
        self.name = name

    def to_str(self):
        return f"Student: {self.name}"


if __name__ == "__main__":
    student1 = Student("Tu")
    student2 = Student("Ten")
