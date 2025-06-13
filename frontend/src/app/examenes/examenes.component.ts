import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Examen {
  id?: number;
  note: number;
  note_value: number; // <-- Agrega este campo
  student: number | null;
  degreeSubject: number | null;
  quetar: number | null;
  type: string; // Siempre "E"
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
  selector: 'app-examenes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './examenes.component.html',
  styleUrls: ['./examenes.component.css']
})
export class ExamenesComponent {
  examenes: Examen[] = [];
  estudiantes: Student[] = [];
  degreeSubjects: DegreeSubject[] = [];
  subjects: Subject[] = [];
  quetars: Quetar[] = [];
  showModal = false;
  editMode = false;
  loading = false;
  newExamen: Examen = this.getEmptyExamen();

  constructor(private apiService: ApiService) {
    this.loadExamenes();
    this.loadEstudiantes();
    this.loadDegreeSubjects();
    this.loadSubjects();
    this.loadQuetars();
  }

  getEmptyExamen(): Examen {
    return {
      note: 0,
      note_value: 0, // <-- Agregado
      student: null,
      degreeSubject: null,
      quetar: null,
      type: 'E'
    };
  }

  loadExamenes() {
    this.loading = true;
    this.apiService.get('TrimestreDelEsudiante/').subscribe({
      next: (data) => {
        this.examenes = data.filter((e: Examen) => e.type === 'E');
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

  openModal(examen?: Examen) {
    if (examen) {
      this.newExamen = { ...examen };
      this.editMode = true;
    } else {
      this.newExamen = this.getEmptyExamen();
      this.editMode = false;
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  saveExamen() {
    this.newExamen.note_value = Number(this.newExamen.note);

    // Crea una copia y cambia el nombre del campo
    const examenToSend: any = { ...this.newExamen };
    examenToSend.degreeSubject_id = examenToSend.degreeSubject;
    delete examenToSend.degreeSubject; // Elimina el campo viejo

    this.apiService.post('TrimestreDelEsudiante/', examenToSend).subscribe({
      next: () => {
        this.loadExamenes();
        this.closeModal();
      }
    });
  }

  deleteExamen(id: number) {
    if (confirm('¿Seguro que deseas eliminar este examen?')) {
      this.apiService.delete(`TrimestreDelEsudiante/${id}/`).subscribe(() => this.loadExamenes());
    }
  }
}
