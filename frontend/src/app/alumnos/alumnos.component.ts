import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

export interface Student {
  id?: number;
  ci: number;
  first_name: string;
  last_name: string;
  birthdate: string;
  gender: string;
  address?: string;
  student_phone?: string;
  parent_phone: string;
  student_email: string;
  created_year?: number;
  user?: number | null;
}

interface StudentCourse {
  id: number;
  student: number;
  grade: number;
  is_repeater: boolean;
}

interface Curso {
  id: number;
  grade: string;
  year: number;
}

@Component({
  selector: 'app-alumnos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './alumnos.component.html',
  styleUrls: ['./alumnos.component.css']
})
export class AlumnosComponent {
  students: Student[] = [];
  allStudents: Student[] = [];
  showModal = false;
  newStudent: Student = this.getEmptyStudent();
  loading = false;
  cursos: Curso[] = [];
  selectedCursoId: number | null = null;

  constructor(private apiService: ApiService) {
    this.loadCursosYDespuesEstudiantes();
  }

  getEmptyStudent(): Student {
    return {
      ci: 0,
      first_name: '',
      last_name: '',
      birthdate: '',
      gender: 'M',
      address: '',
      student_phone: '',
      parent_phone: '',
      student_email: '',
      user: null
    };
  }
  loadCursosYDespuesEstudiantes() {
    this.apiService.get('Cursos/').subscribe({
      next: (data: any) => {
        this.cursos = data;
        this.loadStudents(); // Ahora sí, los cursos ya están cargados
      }
    });
  }

  loadStudents() {
    this.loading = true;
    const cursoId = localStorage.getItem('cursoSeleccionado');
    console.log('ID del curso seleccionado:', cursoId);

    if (cursoId) {
      // Busca el curso en la lista de cursos y muestra el grade
      const curso = this.cursos.find(c => c.id === Number(cursoId));
      if (curso) {
        console.log('Grade del curso seleccionado:', curso.grade);
      } else {
        console.log('No se encontró el curso con ese id en this.cursos');
      }

      // 1. Obtener las relaciones StudentCourse para el curso seleccionado
      this.apiService.get(`CursoPorEstudiante/?grade=${cursoId}`).subscribe({
        next: (relations: StudentCourse[]) => {
          // Filtra solo las relaciones que coinciden con el cursoId
          const filteredRelations = relations.filter(r => r.grade === Number(cursoId));
          console.log('Relaciones filtradas:', filteredRelations);
          const studentIds = filteredRelations.map(r => r.student);
          console.log('IDs de estudiantes relacionados:', studentIds);

          this.apiService.get('Estudiantes/').subscribe({
            next: (data: Student[]) => {
              this.allStudents = data;
              this.students = data.filter(s => studentIds.includes(s.id!));
              console.log('Estudiantes filtrados:', this.students);
              this.loading = false;
            },
            error: () => { this.loading = false; }
          });
        },
        error: () => { this.loading = false; }
      });
    } else {
      // Si no hay filtro, muestra todos los estudiantes
      this.apiService.get('Estudiantes/').subscribe({
        next: (data: Student[]) => {
          this.allStudents = data;
          this.students = data;
          this.loading = false;
        },
        error: () => { this.loading = false; }
      });
    }
  }

  openModal() {
    this.newStudent = this.getEmptyStudent();
    this.selectedCursoId = null;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedCursoId = null;
  }

  createStudent() {
    this.apiService.post('Estudiantes/', this.newStudent).subscribe({
      next: (created: Student) => {
        if (created.id && this.selectedCursoId) {
          // Asociar estudiante al curso
          this.apiService.post('CursoPorEstudiante/', {
            student: created.id,
            grade: this.selectedCursoId
          }).subscribe({
            next: () => {
              this.loadStudents();
              this.closeModal();
            },
            error: () => {
              this.loadStudents();
              this.closeModal();
            }
          });
        } else {
          this.loadStudents();
          this.closeModal();
        }
      }
    });
  }

  deleteStudent(id: number) {
    if (confirm('¿Seguro que deseas eliminar este estudiante?')) {
      this.apiService.delete(`Estudiantes/${id}/`).subscribe(() => this.loadStudents());
    }
  }

  clearCursoFilter() {
    localStorage.removeItem('cursoSeleccionado');
    this.loadStudents();
  }

  get cursoSeleccionado() {
    return localStorage.getItem('cursoSeleccionado');
  }
}
