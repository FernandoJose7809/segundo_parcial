import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface GrupoProfesor {
  id?: number;
  group: number | null;
  teacherSubject: number | null;
}

interface Grupo {
  id: number;
  sigla: string;
}

interface TeacherSubject {
  id: number;
  teacher: number;
  subject: number;
}

interface Profesor {
  id: number;
  first_name: string;
  last_name: string;
}

interface Materia {
  id: number;
  name: string;
}

@Component({
  selector: 'app-grupoprofesor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './grupoprofesor.component.html',
  styleUrls: ['./grupoprofesor.component.css']
})
export class GrupoprofesorComponent {
  grupoprofesores: GrupoProfesor[] = [];
  grupos: Grupo[] = [];
  teacherSubjects: TeacherSubject[] = [];
  profesores: Profesor[] = [];
  materias: Materia[] = [];
  showModal = false;
  newGrupoProfesor: GrupoProfesor = this.getEmptyGrupoProfesor();
  loading = false;

  constructor(private apiService: ApiService) {
    this.loadGrupoProfesores();
    this.loadGrupos();
    this.loadTeacherSubjects();
    this.loadProfesores();
    this.loadMaterias();
  }

  getEmptyGrupoProfesor(): GrupoProfesor {
    return {
      group: null,
      teacherSubject: null
    };
  }

  loadGrupoProfesores() {
    this.loading = true;
    this.apiService.get('GrupoPorProfesor/').subscribe({
      next: (data) => {
        this.grupoprofesores = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  loadGrupos() {
    this.apiService.get('Gupos/').subscribe({
      next: (data) => {
        this.grupos = data;
      }
    });
  }

  loadTeacherSubjects() {
    this.apiService.get('MateriaPorProfesor/').subscribe({
      next: (data) => {
        this.teacherSubjects = data;
      }
    });
  }

  loadProfesores() {
    this.apiService.get('Profesores/').subscribe({
      next: (data) => {
        this.profesores = data;
      }
    });
  }

  loadMaterias() {
    this.apiService.get('Materias/').subscribe({
      next: (data) => {
        this.materias = data;
      }
    });
  }

  openModal() {
    this.newGrupoProfesor = this.getEmptyGrupoProfesor();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createGrupoProfesor() {
    this.apiService.post('GrupoPorProfesor/', this.newGrupoProfesor).subscribe({
      next: () => {
        this.loadGrupoProfesores();
        this.closeModal();
      }
    });
  }

  deleteGrupoProfesor(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta relación?')) {
      this.apiService.delete(`GrupoPorProfesor/${id}/`).subscribe(() => this.loadGrupoProfesores());
    }
  }

  getGrupoName(id: number | null) {
    const grupo = this.grupos.find(g => g.id === id);
    return grupo ? grupo.sigla : '';
  }

  getTeacherSubjectName(id: number | null) {
    const ts = this.teacherSubjects.find(t => t.id === id);
    if (!ts) return '';
    const prof = this.profesores.find(p => p.id === ts.teacher);
    const materia = this.materias.find(m => m.id === ts.subject);
    const profName = prof ? `${prof.first_name} ${prof.last_name}` : 'Profesor desconocido';
    const materiaName = materia ? materia.name : 'Materia desconocida';
    return `${profName} - ${materiaName}`;
  }

  getProfesorName(id: number | null) {
    const prof = this.profesores.find(p => p.id === id);
    return prof ? `${prof.first_name} ${prof.last_name}` : '';
  }

  getMateriaName(id: number | null) {
    const materia = this.materias.find(m => m.id === id);
    return materia ? materia.name : '';
  }
}
