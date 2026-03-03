import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdenFormComponent } from './orden-form.component';

describe('OrdenFormComponent', () => {
  let component: OrdenFormComponent;
  let fixture: ComponentFixture<OrdenFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrdenFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdenFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
