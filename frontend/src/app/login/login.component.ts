import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule], // Importa FormsModule aquí
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private router: Router) {}

  login() {
    if (this.email === 'admin' && this.password === 'admin123') {
      this.router.navigate(['/dashboard']); // Redirige al dashboard
    } else {
      alert('Credenciales incorrectas');
    }
  }
}
