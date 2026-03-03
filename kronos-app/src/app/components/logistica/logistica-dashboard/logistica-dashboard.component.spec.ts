import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogisticaDashboardComponent } from './logistica-dashboard.component';

describe('LogisticaDashboardComponent', () => {
  let component: LogisticaDashboardComponent;
  let fixture: ComponentFixture<LogisticaDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LogisticaDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LogisticaDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
