import os
import django
import random
from faker import Faker
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tu_proyecto.settings")
django.setup()

fake = Faker()

from grades.models import Grade,GroupTeacher,StudentCourse,DegreeSubject
from quater.models import Quetar, Notes, FollowUp, TareaUrl
from students.models import Student, Tutor
from subjects.models import Subject
from teacher.models import Teacher, TeacherSubject

#150 estudiantes
gener_choices = ['M', 'F']
def student(n):
    lista = []
    for _ in range(n):
        ci = fake.unique.random_int(min=100000, max=999999)
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=12, maximum_age=18)
        gender = random.choice(gener_choices)
        address = fake.address()
        student_phone = fake.phone_number()
        student_email = fake.unique.email()
        created_year = datetime.now().year
        
        student = Student.objects.create(
            ci=ci,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            gender=gender,
            address=address,
            student_phone=student_phone,
            student_email=student_email,
            created_year=created_year,
            user=None  
        )
        lista.append(student)
    return lista

#4 Profesores
def teacher(n):
    lista = []
    for _ in range(n):
        ci = fake.unique.random_int(min=100000, max=999999)
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=22, maximum_age=58)
        gender = random.choice(gener_choices)
        address = fake.address()
        phone = fake.phone_number()
        email = fake.unique.email()
        created_year = datetime.now().year
        
        teacher = Teacher.objects.create(
            ci=ci,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            gender=gender,
            address=address,
            phone=phone,
            email=email,
            created_year=created_year,
            user=None  
        )
        lista.append(teacher)
    return lista

#4 Materias
def subjects():
    lista = []
    subjects = {
        'Matematica': 'Estudio de números, operaciones y estructuras lógicas.',
        'Lenguaje': 'Desarrollo de habilidades comunicativas orales y escritas.',
        'Ciencias Sociales': 'Análisis de la sociedad, historia, y cultura humana.',
        'Biologia': 'Estudio de los seres vivos y su funcionamiento.'
    }
    for key, value in subjects.items():
        subject = Subject.objects.create(
            name=key,
            description=value
        )
        lista.append(subject)
    return lista

def tutores(students: list):
    lista = []
    for student in students:
        ci = fake.unique.random_int(min=100000, max=999999)
        first_name = fake.first_name()
        last_name = fake.last_name()
        rol = random.choice(['F', 'M', 'O'])  # 'Padre', 'Madre', 'Otro'
        address = fake.address()
        tutor_email = fake.unique.email()
        created_year = datetime.now().year

        tutor = Tutor.objects.create(
            ci=ci,
            first_name=first_name,
            last_name=last_name,
            rol=rol,
            address=address,
            tutor_email=tutor_email,
            user=None,
            created_year=created_year,
            student=student
        )
        lista.append(tutor)
    return lista


def teacherSubject(teacher:list,subject:list):
    lista = []
    for i in range(len(teacher)):
        teacherSubject = TeacherSubject(
            teacher=teacher[i],
            subject=subject[i]
        )
        lista.append(teacherSubject)
    return lista

# year = models.IntegerField(default = datetime.now().year)
#     grade = models.CharField(max_length=1)
#     acronym = models.CharField(max_length=2)
#     average_annual_grade = models.DecimalField(max_digits=5, decimal_places=2,
#                                              null=True, blank=True, default=0)
#     average_annual_attendance = models.DecimalField(max_digits=5, decimal_places=2,
#                                                   null=True, blank=True, default=0)
def grade(coures,years):
    lista = []
    siglas = 'ABCDEFGHIJKLNOPQRSTUVWXYZ'
    for i in range(years+1):
        year = datetime.now().year - years + i
        for j in range(coures):
            siglas[j]