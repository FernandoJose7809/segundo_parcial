import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrupoprofesorComponent } from './grupoprofesor.component';

describe('GrupoprofesorComponent', () => {
  let component: GrupoprofesorComponent;
  let fixture: ComponentFixture<GrupoprofesorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GrupoprofesorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GrupoprofesorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
