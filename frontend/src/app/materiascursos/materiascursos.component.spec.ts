import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MateriascursosComponent } from './materiascursos.component';

describe('MateriascursosComponent', () => {
  let component: MateriascursosComponent;
  let fixture: ComponentFixture<MateriascursosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MateriascursosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MateriascursosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
