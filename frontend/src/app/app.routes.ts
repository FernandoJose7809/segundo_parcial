import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AlumnosComponent } from './alumnos/alumnos.component';
import { TareasComponent } from './tareas/tareas.component';
import { LoginComponent } from './login/login.component';
import { AsistenciaComponent } from './asistencia/asistencia.component';
import { ExamenesComponent } from './examenes/examenes.component';
import { MateriasComponent } from './materias/materias.component';
import { NotasComponent } from './notas/notas.component';
import { ParticipacionComponent } from './participacion/participacion.component';
import { CursosComponent } from './cursos/cursos.component';
import { MateriascursosComponent } from './materiascursos/materiascursos.component';
import { MateriasprofesorComponent } from './materiasprofesor/materiasprofesor.component';
import { GrupoComponent } from './grupo/grupo.component';
import { GrupoprofesorComponent } from './grupoprofesor/grupoprofesor.component';
import { TrimestreComponent } from './trimestre/trimestre.component';

export const routes: Routes = [
  { path: '', component: LoginComponent }, // Ruta raíz para el login
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      { path: 'alumnos', component: AlumnosComponent },
      { path: 'tareas', component: TareasComponent },
      { path: 'asistencia', component: AsistenciaComponent },
      { path: 'examenes', component: ExamenesComponent },
      { path: 'materias', component: MateriasComponent },
      { path: 'notas', component: NotasComponent },
      { path: 'participacion', component: ParticipacionComponent },
      { path: 'cursos', component: CursosComponent},
      { path: 'cursos_materias', component: MateriascursosComponent },
      { path: 'materias_profesor', component: MateriasprofesorComponent },
      { path: 'grupos', component: GrupoComponent },
      { path: 'grupos_profesor', component: GrupoprofesorComponent },
      { path: 'trimestre', component: TrimestreComponent },
    ],
  },
  { path: '**', redirectTo: '' }, // Redirección para rutas no encontradas
];
