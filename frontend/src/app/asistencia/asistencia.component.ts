import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Asistencia {
  id?: number;
  its_here: boolean;
  date?: string;
  note: number | null; // Cambia degreeSubject por note
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
export class AsistenciaComponent implements OnInit {
  asistencias: Asistencia[] = [];
  estudiantes: Student[] = [];
  degreeSubjects: DegreeSubject[] = [];
  subjects: Subject[] = [];
  quetars: Quetar[] = [];
  notas: any[] = [];
  showModal = false;
  editMode = false;
  loading = false;
  newAsistencia: Asistencia = this.getEmptyAsistencia();
  selectedStudent: number | null = null;
  selectedDegreeSubject: number | null = null;
  selectedQuetar: number | null = null;

  constructor(private apiService: ApiService) {
    this.loadAsistencias();
    this.loadEstudiantes();
    this.loadDegreeSubjects();
    this.loadSubjects();
    this.loadQuetars();
  }

  ngOnInit() {
    this.loadNotas();
  }

  loadAsistencias() {
    this.loading = true;
    this.apiService.get('Asitencia/').subscribe({
      next: (data) => {
        this.asistencias = data;
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

  loadNotas() {
    this.apiService.get('Notas/').subscribe({
      next: (data) => { this.notas = data; }
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

  getEmptyAsistencia(): Asistencia {
    return {
      its_here: false,
      note: null
    };
  }

  saveAsistencia() {
    console.log('Estudiante:', this.selectedStudent, 'Materia:', this.selectedDegreeSubject, 'Trimestre:', this.selectedQuetar);

    const noteId = this.findNoteId();
    if (!noteId) {
      alert('No se encontró la nota para la combinación seleccionada.');
      return;
    }
    const payload = {
      its_here: this.newAsistencia.its_here,
      note: noteId
    };
    if (this.editMode && this.newAsistencia.id) {
      this.apiService.put(`Asitencia/${this.newAsistencia.id}/`, payload).subscribe({
        next: () => {
          this.loadAsistencias();
          this.closeModal();
        }
      });
    } else {
      this.apiService.post('Asitencia/', payload).subscribe({
        next: () => {
          this.loadAsistencias();
          this.closeModal();
        }
      });
    }
  }

  deleteAsistencia(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta asistencia?')) {
      this.apiService.delete(`Asitencia/${id}/`).subscribe(() => this.loadAsistencias());
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

  getStudentFullName(studentId: number | null): string {
    const est = this.estudiantes.find(e => e.id === studentId);
    return est ? `${est.first_name} ${est.last_name}` : '';
  }

  findNoteId(): number | null {
    const note = this.notas.find(n =>
      n.degreeSubject === this.selectedDegreeSubject &&
      n.quetar === this.selectedQuetar &&
      n.student === this.selectedStudent
    );
    return note ? note.id : null;
  }

  getStudentNameFromNote(noteId: number | null): string {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const student = this.estudiantes.find(e => e.id === note.student);
    return student ? `${student.first_name} ${student.last_name}` : '';
  }

  getSubjectNameFromNote(noteId: number | null): string {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const ds = this.degreeSubjects.find(d => d.id === note.degreeSubject);
    if (!ds) return '';
    const subject = this.subjects.find(s => s.id === ds.subject);
    return subject ? subject.name : '';
  }

  getQuetarDescriptionFromNote(noteId: number | null): string {
    const note = this.notas.find(n => n.id === noteId);
    if (!note) return '';
    const quetar = this.quetars.find(q => q.id === note.quetar);
    return quetar ? quetar.description : '';
  }
}
