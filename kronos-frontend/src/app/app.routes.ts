import { Routes } from '@angular/router';
import { OrdenCompra } from './modules/logistica/orden-compra/orden-compra';
import { ListaOrdenes } from './modules/logistica/lista-ordenes/lista-ordenes';
import { Tablero } from './modules/produccion/tablero/tablero';
import { Catalogos } from './modules/logistica/catalogos/catalogos';
import { GestionProductos } from './modules/producto/gestion-productos/gestion-productos';

export const routes: Routes = [

  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },


  { path: 'ordenes/nueva', component: OrdenCompra },

  { path: 'ordenes/editar/:id', component: OrdenCompra},
  
  { path: 'ordenes/lista', component: ListaOrdenes}, 

  { path: 'ordenes/catalogos', component: Catalogos },

  { path: 'produccion/tablero', component: Tablero},
  
  { path: 'producto/gestion', component: GestionProductos },

];
