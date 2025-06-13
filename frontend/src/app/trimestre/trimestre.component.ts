import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Trimestre {
  id?: number;
  queter: string; // o number, según tu backend
  description: string;
  start_date?: string;
  end_date?: string;
}

@Component({
  selector: 'app-trimestre',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './trimestre.component.html',
  styleUrls: ['./trimestre.component.css']
})
export class TrimestreComponent {
  trimestres: Trimestre[] = [];
  showModal = false;
  newTrimestre: Trimestre = this.getEmptyTrimestre();
  loading = false;

  constructor(private apiService: ApiService) {
    this.loadTrimestres();
  }

  getEmptyTrimestre(): Trimestre {
    return {
      queter: '',
      description: '',
      start_date: '',
      end_date: ''
    };
  }

  loadTrimestres() {
    this.loading = true;
    this.apiService.get('Trimestre/').subscribe({
      next: (data) => {
        this.trimestres = data;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  openModal() {
    this.newTrimestre = this.getEmptyTrimestre();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createTrimestre() {
    this.apiService.post('Trimestre/', this.newTrimestre).subscribe({
      next: () => {
        this.loadTrimestres();
        this.closeModal();
      }
    });
  }

  deleteTrimestre(id: number) {
    if (confirm('¿Seguro que deseas eliminar este trimestre?')) {
      this.apiService.delete(`Trimestre/${id}/`).subscribe(() => this.loadTrimestres());
    }
  }
}
