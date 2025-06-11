import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrimestreComponent } from './trimestre.component';

describe('TrimestreComponent', () => {
  let component: TrimestreComponent;
  let fixture: ComponentFixture<TrimestreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrimestreComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrimestreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
