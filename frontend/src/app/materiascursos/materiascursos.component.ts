import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface MateriaCurso {
  id?: number;
  subject: number | null;
  grade: number | null;
}

interface Materia {
  id: number;
  name: string;
}

interface Curso {
  id: number;
  grade: string;
}

@Component({
  selector: 'app-materiascursos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './materiascursos.component.html',
  styleUrls: ['./materiascursos.component.css']
})
export class MateriascursosComponent {
  materiascursos: MateriaCurso[] = [];
  materias: Materia[] = [];
  cursos: Curso[] = [];
  showModal = false;
  newMateriaCurso: MateriaCurso = this.getEmptyMateriaCurso();
  loading = false;

  constructor(private apiService: ApiService) {
    this.loadMateriasCursos();
    this.loadMaterias();
    this.loadCursos();
  }

  getEmptyMateriaCurso(): MateriaCurso {
    return {
      subject: null,
      grade: null
    };
  }

  loadMateriasCursos() {
    this.loading = true;
    this.apiService.get('MateriaPorCurso/').subscribe({
      next: (data) => {
        this.materiascursos = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  loadMaterias() {
    this.apiService.get('Materias/').subscribe({
      next: (data) => {
        this.materias = data;
      }
    });
  }

  loadCursos() {
    this.apiService.get('Cursos/').subscribe({
      next: (data) => {
        this.cursos = data;
      }
    });
  }

  openModal() {
    this.newMateriaCurso = this.getEmptyMateriaCurso();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createMateriaCurso() {
    this.apiService.post('MateriaPorCurso/', this.newMateriaCurso).subscribe({
      next: () => {
        this.loadMateriasCursos();
        this.closeModal();
      }
    });
  }

  deleteMateriaCurso(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta relación?')) {
      this.apiService.delete(`MateriaPorCurso/${id}/`).subscribe(() => this.loadMateriasCursos());
    }
  }

  getMateriaName(id: number | null) {
    const materia = this.materias.find(m => m.id === id);
    return materia ? materia.name : '';
  }

  getCursoName(id: number | null) {
    const curso = this.cursos.find(c => c.id === id);
    return curso ? curso.grade : '';
  }
}
