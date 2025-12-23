import { Routes } from '@angular/router';
import { OrdenCompra } from './modules/logistica/orden-compra/orden-compra';

export const routes: Routes = [
  // Ruta por defecto (Dashboard)
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  
  // Nuestras rutas
  { path: 'ordenes/nueva', component: OrdenCompra },
  
  // Puedes agregar un componente Dashboard temporal si quieres
  // { path: 'dashboard', component: DashboardComponent },
];