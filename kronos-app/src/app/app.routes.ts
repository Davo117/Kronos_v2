import { Routes } from '@angular/router';
import { LogisticaDashboardComponent } from './components/logistica/logistica-dashboard/logistica-dashboard.component';

export const routes: Routes = [
  { path: 'logistica', component: LogisticaDashboardComponent },
  { path: '', redirectTo: 'logistica', pathMatch: 'full' } // Redirigir al inicio
];