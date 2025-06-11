import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Materia {
  id?: number;
  name: string;
  description?: string;
}

@Component({
  selector: 'app-materias',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './materias.component.html',
  styleUrls: ['./materias.component.css']
})
export class MateriasComponent {
  materias: Materia[] = [];
  showModal = false;
  newMateria: Materia = this.getEmptyMateria();
  loading = false;

  constructor(private apiService: ApiService) {
    this.loadMaterias();
  }

  getEmptyMateria(): Materia {
    return {
      name: '',
      description: ''
    };
  }

  loadMaterias() {
    this.loading = true;
    this.apiService.get('Materias/').subscribe({
      next: (data) => {
        this.materias = data.sort(
          (a: Materia, b: Materia) => a.name.localeCompare(b.name)
        );
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  openModal() {
    this.newMateria = this.getEmptyMateria();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createMateria() {
    this.apiService.post('Materias/', this.newMateria).subscribe({
      next: () => {
        this.loadMaterias();
        this.closeModal();
      }
    });
  }

  deleteMateria(id: number) {
    if (confirm('¿Seguro que deseas eliminar esta materia?')) {
      this.apiService.delete(`Materias/${id}/`).subscribe(() => this.loadMaterias());
    }
  }
}
