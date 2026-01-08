import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { FormsModule } from '@angular/forms'; 
import { initFlowbite } from 'flowbite';
import { LogisticaService } from '../../../services/logistica';
import { Router, ActivatedRoute } from '@angular/router';

interface DetalleOrden {
  productoId: string;
  cantidad: number;
  unidad: string;
  notas: string;
}

@Component({
  selector: 'app-orden-compra',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './orden-compra.html', 
  styleUrl: './orden-compra.scss' 
})

export class OrdenCompra implements OnInit {

  private logisticaService = inject(LogisticaService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  catalogoClientes: any[] = [];
  catalogoSucursales: any[] = [];
  catalogoProductos: any[] = [];

  clienteSeleccionado: string = '';
  sucursalSeleccionada: string = '';
  noOrden: string = '';
  fechaDocumento: string = '';
  fechaRecepcion: string = '';
  fechaEntrega: string = '';
  esEdicion: boolean = false;
  idPedidoEditar: number | null = null;

  productosEnOrden: DetalleOrden[] = [];

  ngOnInit(): void {
    initFlowbite();
    this.cargarCatalogos();

    // Verifica si hay un ID en la URL
    const id = this.route.snapshot.paramMap.get('id');
    
    if (id) {
      // MODO EDICIÓN
      this.esEdicion = true;
      this.idPedidoEditar = Number(id);
      this.cargarDatosPedido(this.idPedidoEditar);
    } else {
      // MODO CREACIÓN (Lo normal)
      this.agregarFila();
    }
  }

  cargarDatosPedido(id: number) {
    this.logisticaService.getPedidoPorId(id).subscribe(data => {
      this.clienteSeleccionado = data.cliente_id;

      this.onClienteChange();       
      setTimeout(() => {
        this.sucursalSeleccionada = data.sucursal_id;
      }, 100);

      this.noOrden = data.numero_orden_cliente;
      this.fechaDocumento = data.fecha_documento;
      this.fechaRecepcion = data.fecha_recepcion;
      this.fechaEntrega = data.fecha_entrega_pactada;
      
      this.productosEnOrden = data.productos;
    });
  }

  cargarCatalogos() {

    this.logisticaService.getClientes().subscribe((data: any) => {
      this.catalogoClientes = data;
    });

    this.logisticaService.getProductos().subscribe((data: any) => {
      this.catalogoProductos = data;
    });
  }

  onClienteChange() {
    this.catalogoSucursales = [];
    this.sucursalSeleccionada = '';
    
    const cliente = this.catalogoClientes.find((c: any) => c.id == this.clienteSeleccionado);
    
    if (cliente && cliente.sucursales) {
      this.catalogoSucursales = cliente.sucursales;
    }
  }

  agregarFila() {
    this.productosEnOrden.push({
      productoId: '', 
      cantidad: 0,
      unidad: '',
      notas: ''
    });
  }

  eliminarFila(index: number) {
    if (this.productosEnOrden.length > 1) {
      this.productosEnOrden.splice(index, 1);
    } else {
      alert("La orden debe tener al menos un producto.");
    }
  }

  actualizarUnidad(index: number) {
    // Lógica futura para unidad
  }

  guardarOrden() {
    // Validaciones
    if (!this.clienteSeleccionado) {
      alert("Selecciona un cliente");
      return;
    }

    const payload = {
      cliente_id: this.clienteSeleccionado,
      sucursal_id: this.sucursalSeleccionada,
      numero_orden_cliente: this.noOrden,
      fecha_documento: this.fechaDocumento,
      fecha_recepcion: this.fechaRecepcion,
      fecha_entrega_pactada: this.fechaEntrega,
      productos: this.productosEnOrden
    };

    console.log("Enviando...", payload);

    if (this.esEdicion && this.idPedidoEditar) {
      
      // CASO EDICIÓN
      this.logisticaService.actualizarPedido(this.idPedidoEditar, payload).subscribe({
        next: () => {
          alert("¡Orden actualizada correctamente!");
          this.router.navigate(['/ordenes/lista']);
        },
        error: (err: any) => {
          console.error(err);
          alert("Error al actualizar: " + (err.error?.error || err.message));
        }
      });

    } else {
      
      // CASO CREACIÓN 
      this.logisticaService.guardarPedido(payload).subscribe({
        next: (resp: any) => {
          alert("¡Orden creada con éxito! ID: " + resp.id);
          this.router.navigate(['/ordenes/lista']); 
        },
        error: (err: any) => {
          console.error(err);
          alert("Error al guardar: " + (err.error?.error || err.message));
        }
      });
    }
  }
}