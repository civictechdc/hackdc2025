import { Component, OnInit } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { RegulationsService, Regulation } from '../../services/regulations.service';

@Component({
  standalone: true,
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatCardModule,
    MatChipsModule,
    MatProgressSpinnerModule
  ],
})
export class SearchComponent implements OnInit {
  searchTerm: string = '';
  regulations: Regulation[] = [];
  filteredRegulations: Regulation[] = [];
  loading = false;
  error = '';

  constructor(private regulationsService: RegulationsService) {}

  ngOnInit() {
    this.loading = true;
    this.regulationsService.getAllRegulations().subscribe({
      next: (data) => {
        this.regulations = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error fetching regulations:', err);
        this.error = 'Failed to load regulations. Please try again.';
        this.loading = false;
      }
    });
  }

  search() {
    if (!this.searchTerm.trim()) {
      this.filteredRegulations = [];
      return;
    }
    
    this.loading = true;
    this.error = '';
    
    this.regulationsService.searchRegulations(this.searchTerm).subscribe({
      next: (data) => {
        this.filteredRegulations = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error searching regulations:', err);
        this.error = 'Search failed. Please try again.';
        this.loading = false;
      }
    });
  }
}