import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Produccion } from '../../../services/produccion';

@Component({
  selector: 'app-tablero',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tablero.html',
  styleUrl: './tablero.scss'
})
export class Tablero implements OnInit {

  private produccionService = inject(Produccion);

  kpis: any = {
    eficiencia: 0,
    metros_hoy: 0,
    en_cola: 0,
    merma: 0
  };

  ordenesActivas: any[] = [];
  cargando: boolean = true;

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos() {
    this.produccionService.getDashboardData().subscribe({
      next: (data) => {
        this.kpis = data.kpis;
        this.ordenesActivas = data.ordenes;
        this.cargando = false;
      },
      error: (err) => {
        console.error(err);
        this.cargando = false;
      }
    });
  }

  getClaseEstatus(estatus: string): string {
    if (estatus === 'PRODUCCION') return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    if (estatus === 'CONFIRMADO') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    return 'bg-gray-100 text-gray-800';
  }
}