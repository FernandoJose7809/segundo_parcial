import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tu_proyecto.settings")
django.setup()

fake = Faker()

from app.grades.models import Grade,GroupTeacher,StudentCourse,DegreeSubject
from app.quater.models import Quetar, Notes, Task, Attendance, Participation, Exam
from app.students.models import Student, Tutor
from app.subjects.models import Subject
from app.teacher.models import Teacher, TeacherSubject

#150 estudiantes
gener_choices = ['M', 'F']
def student(n):
    lista = []
    for _ in range(n):
        ci = fake.unique.random_int(min=100000, max=999999)
        first_name = fake.first_name()[:14]
        last_name = fake.last_name()[:14]
        birthdate = fake.date_of_birth(minimum_age=12, maximum_age=18)
        gender = random.choice(gener_choices)
        address = fake.address()[:14]
        student_phone = fake.phone_number()[:14]
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
        first_name = fake.first_name()[:14]
        last_name = fake.last_name()[:14]
        birthdate = fake.date_of_birth(minimum_age=22, maximum_age=58)
        gender = random.choice(gener_choices)
        address = fake.address()[:14]
        phone = fake.phone_number()[:14]
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
        first_name = fake.first_name()[:14]
        last_name = fake.last_name()[:14]
        rol = random.choice(['F', 'M', 'O'])  # 'Padre', 'Madre', 'Otro'
        address = fake.address()[:14]
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

def followUp():
    notes = Notes.objects.all()
    for note in notes:
        # Usamos un rango realista basado en el Quetar
        quetar = note.quetar
        start = quetar.start_date
        end = quetar.end_date

        for _ in range(10):
            date = fake.date_between(start_date=start, end_date=end)
            Attendance.objects.create(
                its_here = random.random() < 0.9,
                date = date,
                note = note
            )

        for _ in range(3):
            date = fake.date_between(start_date=start, end_date=end)
            Exam.objects.create(
                value = round(random.uniform(35, 100), 2),
                date = date,
                note = note
            )

        for _ in range(5):
            start_date = fake.date_between(start_date=start, end_date=end - timedelta(days=1))
            end_date = fake.date_between(start_date=start_date, end_date=end)
            Task.objects.create(
                value = round(random.uniform(35, 100), 2),
                start_date = start_date,
                end_date = end_date,
                url = "",  # O fake.url() si es requerido
                note = note
            )

        for _ in range(5):
            date = fake.date_between(start_date=start, end_date=end)
            Participation.objects.create(
                value = round(random.uniform(35, 100), 2),
                date = date,
                note = note
            )
def calcular_notas_reales():
    for nota in Notes.objects.all():
        tasks = Task.objects.filter(note=nota)
        exams = Exam.objects.filter(note=nota)
        participations = Participation.objects.filter(note=nota)
        attendances = Attendance.objects.filter(note=nota)

        # Promedios calculados
        avg_task = sum(t.value for t in tasks) / len(tasks) if tasks else 0
        avg_exam = sum(e.value for e in exams) / len(exams) if exams else 0
        avg_participation = sum(p.value for p in participations) / len(participations) if participations else 0
        avg_attendance = (sum(1 for a in attendances if a.its_here) / len(attendances) * 100) if attendances else 0

        # Cálculo final ponderado
        final_note = round(
            avg_task * 0.15 +
            avg_exam * 0.60 +
            avg_participation * 0.10 +
            avg_attendance * 0.15,
            2
        )

        # Guardamos en el modelo Notes
        nota.note_Task = round(avg_task, 2)
        nota.note_Exam = round(avg_exam, 2)
        nota.note_Participation = round(avg_participation, 2)
        nota.note_Attendance = round(avg_attendance, 2)
        nota.note = final_note
        nota.save()   
            
def pobalarBaseDeDatos():
    estudiante = student(150)
    profesor = teacher(4)
    materias = subjects()
    tutor = tutores(estudiante)
    profesorDeMateria = teacherSubject(profesor, materias)
    curso = grade(2,4)
    cursoEstudiante = studentCourse(estudiante, curso)
    grupoProfesor = group_teacher(curso, profesorDeMateria)
    trimestres = quetars(4)
    followUp()
    calcular_notas_reales()
    

