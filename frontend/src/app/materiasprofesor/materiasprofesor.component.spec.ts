import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MateriasprofesorComponent } from './materiasprofesor.component';

describe('MateriasprofesorComponent', () => {
  let component: MateriasprofesorComponent;
  let fixture: ComponentFixture<MateriasprofesorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MateriasprofesorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MateriasprofesorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
