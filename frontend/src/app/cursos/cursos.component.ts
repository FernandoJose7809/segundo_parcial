import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';

interface Curso {
  id?: number;
  year: number;
  grade: string;
  average_annual_grade?: number;
  average_annual_attendance?: number;
}

@Component({
  selector: 'app-cursos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cursos.component.html',
  styleUrls: ['./cursos.component.css']
})
export class CursosComponent {
  cursos: Curso[] = [];
  showModal = false;
  newCurso: Curso = this.getEmptyCurso();
  loading = false;

  constructor(private apiService: ApiService, private router: Router) {
    this.loadCursos();
  }

  getEmptyCurso(): Curso {
    return {
      year: new Date().getFullYear(),
      grade: ''
    };
  }

  loadCursos() {
    this.loading = true;
    this.apiService.get('Cursos/').subscribe({
      next: (data) => {
        this.cursos = data.sort(
          (a: Curso, b: Curso) => a.grade.localeCompare(b.grade)
        );
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  openModal() {
    this.newCurso = this.getEmptyCurso();
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  createCurso() {
    this.apiService.post('Cursos/', this.newCurso).subscribe({
      next: () => {
        this.loadCursos();
        this.closeModal();
      }
    });
  }

  deleteCurso(id: number) {
    if (confirm('¿Seguro que deseas eliminar este curso?')) {
      this.apiService.delete(`Cursos/${id}/`).subscribe(() => this.loadCursos());
    }
  }

  goToAlumnos(id: number) {
    localStorage.setItem('cursoSeleccionado', id.toString());
    this.router.navigate(['/dashboard/alumnos']);
  }
}
