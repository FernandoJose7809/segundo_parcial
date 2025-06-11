import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface MateriaProfesor {
  id?: number;
  subject: number | null;
  teacher: number | null;
}

interface Materia {
  id: number;
  name: string;
}

interface Profesor {
  id: number;
  first_name: string;
  last_name: string;
}

@Component({
  selector: 'app-materiasprofesor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './materiasprofesor.component.html',
  styleUrls: ['./materiasprofesor.component.css']
})
export class MateriasprofesorComponent {
  materiasprofesor: MateriaProfesor[] = [];
  materias: Materia[] = [];
  profesores: Profesor[] = [];
  showModal = false;
  newMateriaProfesor: MateriaProfesor = this.getEmptyMateriaProfesor();
  loading = false;

  constructor(private apiService: ApiService) {
    this.loadMateriasProfesor();
    this.loadMaterias();
    this.loadProfesores();
  }

  getEmptyMateriaProfesor(): MateriaProfesor {
    return {
      subject: null,
      teacher: null
    };
  }

  loadMateriasProfesor() {
    this.loading = true;
    this.apiService.get('MateriaPorProfesor/').subscribe({
      next: (data) => {
        this.materiasprofesor = data;
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

  loadProfesores() {
    this.apiService.get('Profesores/').subscribe({
      next: (data) => {
        this.profesores = data;
      }
    });
  }

  openModal() {
    this.newMateriaProfesor = this.getEmptyMateriaProfesor();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createMateriaProfesor() {
    this.apiService.post('MateriaPorProfesor/', this.newMateriaProfesor).subscribe({
      next: () => {
        this.loadMateriasProfesor();
        this.closeModal();
      }
    });
  }

  deleteMateriaProfesor(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta relación?')) {
      this.apiService.delete(`MateriaPorProfesor/${id}/`).subscribe(() => this.loadMateriasProfesor());
    }
  }

  getMateriaName(id: number | null) {
    const materia = this.materias.find(m => m.id === id);
    return materia ? materia.name : '';
  }

  getProfesorName(id: number | null) {
    const prof = this.profesores.find(p => p.id === id);
    return prof ? `${prof.first_name} ${prof.last_name}` : '';
  }
}
