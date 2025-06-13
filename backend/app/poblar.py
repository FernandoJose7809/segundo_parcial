import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

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
        teacherSubject = TeacherSubject.objects.create(
            teacher=teacher[i],
            subject=subject[i]
        )
        lista.append(teacherSubject)
    return lista

def grade(courses, years):
    lista = []
    siglas = 'ABCDEFGHIJKLNOPQRSTUVWXYZ'
    for i in range(years + 1):
        year = datetime.now().year - years + i
        for j in range(courses):
            grade = Grade.objects.create(
                year=year,
                grade=str(i + 1),  # Aseguramos que sea string
                acronym=siglas[j],
                average_annual_grade=round(random.uniform(50, 90), 2),
                average_annual_attendance=round(random.uniform(50, 90), 2)
            )
            lista.append(grade)
    return lista

def studentCourse(students:list,grades:list):
    lista = []
    for grade in grades:
        for student in students:
            studentCourse = StudentCourse.objects.create(
                student = student,
                grade = grade,
                is_repeater = random.random() < 0.05
            )
            lista.append(studentCourse)
            
    return lista
            
def group_teacher(grades: list, teacherSubjects: list):
    lista = []
    for teacherSubject in teacherSubjects:
        for grade in grades:
            gt = GroupTeacher.objects.create(
                grade=grade,
                teacherSubject=teacherSubject
            )
            lista.append(gt)
    return lista

def quetars(years):
    lista = []
    descripcion_base = ["Primer trimestre", "Segundo trimestre", "Tercer trimestre"]
    current_year = datetime.now().year
    start_year = current_year - years
    for i in range(years + 1):
        año = start_year + i
        fecha_inicio = datetime(año, 2, 1)
        for j in range(3):
            quetar = Quetar.objects.create(
                queter=str(j + 1),
                description=descripcion_base[j],
                start_date=fecha_inicio + timedelta(days=j * 90),
                end_date=fecha_inicio + timedelta(days=(j + 1) * 90 - 1)
            )
            crear_notas_para_quetar(quetar)
            lista.append(quetar)
    return lista

def crear_notas_para_quetar(quetar):
    for degreeSubject in DegreeSubject.objects.all():
        student_courses = StudentCourse.objects.filter(grade=degreeSubject.grade)
        for sc in student_courses:
            Notes.objects.get_or_create(
                student=sc.student,
                degreeSubject=degreeSubject,
                quetar=quetar
            )
#! Solucianarlo despues Follow UP
def notas():
    for nota in Notes.objects.all():
        nota.note_Task = round(random.uniform(35, 100), 2)
        nota.note_Exam = round(random.uniform(35, 100), 2)
        nota.note_Participation = round(random.uniform(35, 100), 2)
        nota.note_Attendance = 100 if random.random() < 0.9 else 0  
        nota.note = round(
            nota.note_Task * 0.15 +
            nota.note_Exam * 0.60 +
            nota.note_Participation * 0.10 +
            nota.note_Attendance * 0.15
        )
        nota.save()

