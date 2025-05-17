import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AlumnosComponent } from './alumnos/alumnos.component';
import { TareasComponent } from './tareas/tareas.component';
import { LoginComponent } from './login/login.component';

export const routes: Routes = [
  { path: '', component: LoginComponent }, // Ruta raíz para el login
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      { path: 'alumnos', component: AlumnosComponent },
      { path: 'tareas', component: TareasComponent },
    ],
  },
  { path: '**', redirectTo: '' }, // Redirección para rutas no encontradas
];
