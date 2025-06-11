import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Participacion {
  id?: number;
  note: number;
  student: number | null;
  degreeSubject: number | null;
  quetar: number | null;
  type: string; // Siempre "P"
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
  selector: 'app-participacion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './participacion.component.html',
  styleUrls: ['./participacion.component.css']
})
export class ParticipacionComponent {
  participaciones: Participacion[] = [];
  estudiantes: Student[] = [];
  degreeSubjects: DegreeSubject[] = [];
  subjects: Subject[] = [];
  quetars: Quetar[] = [];
  showModal = false;
  editMode = false;
  loading = false;
  newParticipacion: Participacion = this.getEmptyParticipacion();

  constructor(private apiService: ApiService) {
    this.loadParticipaciones();
    this.loadEstudiantes();
    this.loadDegreeSubjects();
    this.loadSubjects();
    this.loadQuetars();
  }

  getEmptyParticipacion(): Participacion {
    return {
      note: 0,
      student: null,
      degreeSubject: null,
      quetar: null,
      type: 'P'
    };
  }

  loadParticipaciones() {
    this.loading = true;
    this.apiService.get('TrimestreDelEsudiante/').subscribe({
      next: (data) => {
        this.participaciones = data.filter((p: Participacion) => p.type === 'P');
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

  openModal(participacion?: Participacion) {
    if (participacion) {
      this.newParticipacion = { ...participacion };
      this.editMode = true;
    } else {
      this.newParticipacion = this.getEmptyParticipacion();
      this.editMode = false;
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveParticipacion() {
    if (this.editMode && this.newParticipacion.id) {
      this.apiService.put(`TrimestreDelEsudiante/${this.newParticipacion.id}/`, this.newParticipacion).subscribe({
        next: () => {
          this.loadParticipaciones();
          this.closeModal();
        }
      });
    } else {
      this.apiService.post('TrimestreDelEsudiante/', this.newParticipacion).subscribe({
        next: () => {
          this.loadParticipaciones();
          this.closeModal();
        }
      });
    }
  }

  deleteParticipacion(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta participación?')) {
      this.apiService.delete(`TrimestreDelEsudiante/${id}/`).subscribe(() => this.loadParticipaciones());
    }
  }
}
