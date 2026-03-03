import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductoEspecificacionesComponent } from './producto-especificaciones.component';

describe('ProductoEspecificacionesComponent', () => {
  let component: ProductoEspecificacionesComponent;
  let fixture: ComponentFixture<ProductoEspecificacionesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProductoEspecificacionesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProductoEspecificacionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
