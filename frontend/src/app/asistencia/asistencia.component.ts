import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Asistencia {
  id?: number;
  note: number;
  student: number | null;
  degreeSubject: number | null;
  quetar: number | null;
  type: string; // Siempre "A"
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
  // Puedes agregar más campos si tu API los retorna
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
  selector: 'app-asistencia',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './asistencia.component.html',
  styleUrls: ['./asistencia.component.css']
})
export class AsistenciaComponent {
  asistencias: Asistencia[] = [];
  estudiantes: Student[] = [];
  degreeSubjects: DegreeSubject[] = [];
  subjects: Subject[] = [];
  quetars: Quetar[] = [];
  showModal = false;
  editMode = false;
  loading = false;
  newAsistencia: Asistencia = this.getEmptyAsistencia();

  constructor(private apiService: ApiService) {
    this.loadAsistencias();
    this.loadEstudiantes();
    this.loadDegreeSubjects();
    this.loadSubjects();
    this.loadQuetars();
  }

  getEmptyAsistencia(): Asistencia {
    return {
      note: 0,
      student: null,
      degreeSubject: null,
      quetar: null,
      type: 'A'
    };
  }

  loadAsistencias() {
    this.loading = true;
    this.apiService.get('TrimestreDelEsudiante/').subscribe({
      next: (data) => {
        // Filtra solo asistencias
        this.asistencias = data.filter((a: Asistencia) => a.type === 'A');
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
      next: (data) => { this.degreeSubjects = data; }
    });
  }

  loadSubjects() {
    this.apiService.get('Materias/').subscribe({
      next: (data) => { this.subjects = data; }
    });
  }

  loadQuetars() {
    this.apiService.get('Trimestre/').subscribe({
      next: (data) => { this.quetars = data; }
    });
  }

  openModal(asistencia?: Asistencia) {
    if (asistencia) {
      this.newAsistencia = { ...asistencia };
      this.editMode = true;
    } else {
      this.newAsistencia = this.getEmptyAsistencia();
      this.editMode = false;
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveAsistencia() {
    if (this.editMode && this.newAsistencia.id) {
      this.apiService.put(`TrimestreDelEsudiante/${this.newAsistencia.id}/`, this.newAsistencia).subscribe({
        next: () => {
          this.loadAsistencias();
          this.closeModal();
        }
      });
    } else {
      this.apiService.post('TrimestreDelEsudiante/', this.newAsistencia).subscribe({
        next: () => {
          this.loadAsistencias();
          this.closeModal();
        }
      });
    }
  }

  deleteAsistencia(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta asistencia?')) {
      this.apiService.delete(`TrimestreDelEsudiante/${id}/`).subscribe(() => this.loadAsistencias());
    }
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
}
