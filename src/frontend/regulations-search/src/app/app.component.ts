import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HomepageComponent } from './components/homepage/homepage.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HomepageComponent],
  template: `<app-homepage></app-homepage>`,
})
export class AppComponent {
  title = 'regulations-search';
}