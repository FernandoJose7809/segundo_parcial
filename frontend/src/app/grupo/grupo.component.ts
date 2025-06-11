import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Grupo {
  id?: number;
  sigla: string;
  grade: number | null;
}

@Component({
  selector: 'app-grupo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './grupo.component.html',
  styleUrls: ['./grupo.component.css']
})
export class GrupoComponent {
  grupos: Grupo[] = [];
  showModal = false;
  newGrupo: Grupo = this.getEmptyGrupo();
  loading = false;
  cursos: any[] = [];

  constructor(private apiService: ApiService) {
    this.loadGrupos();
    this.loadCursos();
  }

  getEmptyGrupo(): Grupo {
    return {
      sigla: '',
      grade: null
    };
  }

  loadGrupos() {
    this.loading = true;
    this.apiService.get('Gupos/').subscribe({
      next: (data) => {
        this.grupos = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
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
    this.newGrupo = this.getEmptyGrupo();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createGrupo() {
    this.apiService.post('Gupos/', this.newGrupo).subscribe({
      next: () => {
        this.loadGrupos();
        this.closeModal();
      }
    });
  }

  deleteGrupo(id: number) {
    if (confirm('¿Seguro que deseas eliminar este grupo?')) {
      this.apiService.delete(`Gupos/${id}/`).subscribe(() => this.loadGrupos());
    }
  }

  getCursoName(id: number | null) {
    const curso = this.cursos.find(c => c.id === id);
    return curso ? curso.grade : '';
  }
}
