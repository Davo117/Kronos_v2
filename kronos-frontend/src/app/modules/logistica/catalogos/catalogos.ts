import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CatalogosService } from '../../../services/catalogos';
import { LogisticaService } from '../../../services/logistica';

@Component({
  selector: 'app-catalogos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './catalogos.html',
  styleUrl: './catalogos.scss'
})
export class Catalogos implements OnInit {

  private catalogosService = inject(CatalogosService);
  private logisticaService = inject(LogisticaService);

  // Listas para los Selects
  listaCiudades: any[] = [];
  listaClientes: any[] = [];

  // Modelos para los Formularios
  ciudad = { nombre: '', estado: '', pais: 'México' };
  
  cliente = { 
    nombre_fiscal: '', rfc: '', telefono: '', 
    direccion: '', colonia: '', codigo_postal: '', ciudad_id: '' 
  };

  sucursal = { 
    cliente_id: '', nombre: '', transporte: '', telefono: '',
    direccion: '', colonia: '', codigo_postal: '', ciudad_id: '' 
  };


  listaEstados: string[] = [
    'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 
    'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 
    'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 
    'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 
    'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 
    'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'
  ];

  ngOnInit(): void {
    this.cargarListas();
  }

  cargarListas() {
    // Cargar Ciudades
    this.catalogosService.getCiudades().subscribe(data => this.listaCiudades = data);
    // Cargar Clientes (Reutilizamos el servicio de Logística)
    this.logisticaService.getClientes().subscribe(data => this.listaClientes = data);
  }

  // --- GUARDAR CIUDAD ---
  guardarCiudad() {
    this.catalogosService.crearCiudad(this.ciudad).subscribe({
      next: () => {
        alert('Ciudad agregada');
        this.ciudad = { nombre: '', estado: '', pais: 'México' }; // Limpiar
        this.cargarListas(); // Recargar para que aparezca en los otros formularios
      },
      error: (e) => alert('Error: ' + e.message)
    });
  }

  // --- GUARDAR CLIENTE ---
  guardarCliente() {
    this.catalogosService.crearCliente(this.cliente).subscribe({
      next: () => {
        alert('Cliente registrado con éxito');
        // Limpiar formulario
        this.cliente = { nombre_fiscal: '', rfc: '', telefono: '', direccion: '', colonia: '', codigo_postal: '', ciudad_id: '' };
        this.cargarListas();
      },
      error: (e) => alert('Error: ' + e.message)
    });
  }

  // --- GUARDAR SUCURSAL ---
  guardarSucursal() {
    this.catalogosService.crearSucursal(this.sucursal).subscribe({
      next: () => {
        alert('Sucursal vinculada con éxito');
        this.sucursal = { cliente_id: '', nombre: '', transporte: '', telefono: '', direccion: '', colonia: '', codigo_postal: '', ciudad_id: '' };
      },
      error: (e) => alert('Error: ' + e.message)
    });
  }

}