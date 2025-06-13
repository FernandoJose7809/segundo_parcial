import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Tarea {
  id?: number;
  note: number;
  student: number | null;
  degreeSubject: number | null;
  quetar: number | null;
  type: string; // Siempre "T"
}

interface Student {
  id: number;
  first_name: string;
  last_name: string;
}

interface DegreeSubject {
  id: number;
  subject: number | null;
  grade: number | null;
}

interface Subject {
  id: number;
  name: string;
}

interface Quetar {
  id: number;
  description: string;
}

@Component({
  selector: 'app-tareas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tareas.component.html',
  styleUrls: ['./tareas.component.css']
})
export class TareasComponent {
  tareas: Tarea[] = [];
  estudiantes: Student[] = [];
  degreeSubjects: DegreeSubject[] = [];
  subjects: Subject[] = [];
  quetars: Quetar[] = [];
  showModal = false;
  editMode = false;
  loading = false;
  newTarea: Tarea = this.getEmptyTarea();

  constructor(private apiService: ApiService) {
    this.loadTareas();
    this.loadEstudiantes();
    this.loadDegreeSubjects();
    this.loadSubjects();
    this.loadQuetars();
  }

  getEmptyTarea(): Tarea {
    return {
      note: 0,
      student: null,
      degreeSubject: null,
      quetar: null,
      type: 'T'
    };
  }

  loadTareas() {
    this.loading = true;
    this.apiService.get('TrimestreDelEsudiante/').subscribe({
      next: (data) => {
        this.tareas = data.filter((t: Tarea) => t.type === 'T');
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  loadEstudiantes() {
    this.apiService.get('Estudiantes/').subscribe({
      next: (data) => {
        this.estudiantes = data.sort(
          (a: Student, b: Student) => a.last_name.localeCompare(b.last_name)
        );
      }
    });
  }

  loadDegreeSubjects() {
    this.apiService.get('MateriaPorCurso/').subscribe({
      next: (data: any) => { this.degreeSubjects = data; }
    });
  }

  loadSubjects() {
    this.apiService.get('Materias/').subscribe({
      next: (data: any) => { this.subjects = data; }
    });
  }

  loadQuetars() {
    this.apiService.get('Trimestre/').subscribe({
      next: (data: any) => { this.quetars = data; }
    });
  }

  getStudentName(id: number | null) {
    const est = this.estudiantes.find(e => e.id === id);
    return est ? `${est.first_name} ${est.last_name}` : '';
  }

  getSubjectName(degreeSubjectId: number | null) {
    const ds = this.degreeSubjects.find(d => d.id === degreeSubjectId);
    if (!ds) return '';
    const subject = this.subjects.find(s => s.id === ds.subject);
    return subject ? subject.name : '';
  }

  getQuetarDescription(quetarId: number | null) {
    const q = this.quetars.find(qt => qt.id === quetarId);
    return q ? q.description : '';
  }

  openModal(tarea?: Tarea) {
    if (tarea) {
      this.newTarea = { ...tarea };
      this.editMode = true;
    } else {
      this.newTarea = this.getEmptyTarea();
      this.editMode = false;
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveTarea() {
    if (this.editMode && this.newTarea.id) {
      this.apiService.put(`TrimestreDelEsudiante/${this.newTarea.id}/`, this.newTarea).subscribe({
        next: () => {
          this.loadTareas();
          this.closeModal();
        }
      });
    } else {
      this.apiService.post('TrimestreDelEsudiante/', this.newTarea).subscribe({
        next: () => {
          this.loadTareas();
          this.closeModal();
        }
      });
    }
  }

  deleteTarea(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta tarea?')) {
      this.apiService.delete(`TrimestreDelEsudiante/${id}/`).subscribe(() => this.loadTareas());
    }
  }
}
