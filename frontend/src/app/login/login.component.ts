import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { FormsModule } from '@angular/forms'; // <-- Agrega esto

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule], // <-- Agrega esto
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = ''; 
  password: string = '';

  constructor(private router: Router, private apiService: ApiService) {}

  login() {
    const loginData = { username: this.username, password: this.password }; // Usa 'username'

    this.apiService.post('token/', loginData).subscribe(
      (response: any) => {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        alert('Credenciales incorrectas');
      }
    );
  }
}
