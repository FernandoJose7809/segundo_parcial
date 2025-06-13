import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Tarea {
  id?: number;
  value: number;
  end_date: string;
  degreeSubject: number | null;
  url: string; // <-- Agrega esta línea
  note?: number;
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
  notas: any[] = []; // Asegúrate de cargar las notas
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
    this.loadNotas();
  }

  getEmptyTarea(): Tarea {
    return {
      value: 0,
      end_date: '',
      degreeSubject: null,
      url: '', // <-- Agrega esta línea
      note: 0
    };
  }

  loadTareas() {
    this.loading = true;
    this.apiService.get('Tarea/').subscribe({
      next: (data) => {
        this.tareas = data;
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

  loadNotas() {
    this.apiService.get('Notas/').subscribe({
      next: (data) => { this.notas = data; }
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
      this.apiService.put(`Tarea/${this.newTarea.id}/`, this.newTarea).subscribe({
        next: () => {
          this.loadTareas();
          this.closeModal();
        }
      });
    } else {
      this.apiService.post('Tarea/', this.newTarea).subscribe({
        next: () => {
          this.loadTareas();
          this.closeModal();
        }
      });
    }
  }

  deleteTarea(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta tarea?')) {
      this.apiService.delete(`Tarea/${id}/`).subscribe(() => this.loadTareas());
    }
  }

  getStudentNameFromNote(noteId: number | undefined) {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const est = this.estudiantes.find(e => e.id === note.student);
    return est ? `${est.first_name} ${est.last_name}` : '';
  }

  getSubjectNameFromNote(noteId: number | undefined) {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const ds = this.degreeSubjects.find(d => d.id === note.degreeSubject);
    if (!ds) return '';
    const subject = this.subjects.find(s => s.id === ds.subject);
    return subject ? subject.name : '';
  }

  getQuetarDescriptionFromNote(noteId: number | undefined) {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const q = this.quetars.find(qt => qt.id === note.quetar);
    return q ? q.description : '';
  }
}
