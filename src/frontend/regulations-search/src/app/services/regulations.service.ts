import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Regulation {
  docket_id: number;
  title: string;
  summary: string;
  keywords: string[];
}

@Injectable({
  providedIn: 'root'
})
export class RegulationsService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getAllRegulations(): Observable<Regulation[]> {
    return this.http.get<Regulation[]>(`${this.apiUrl}/regulations`);
  }

  searchRegulations(term: string): Observable<Regulation[]> {
    return this.http.get<Regulation[]>(`${this.apiUrl}/regulations/search/${term}`);
  }

  getRegulation(id: number): Observable<Regulation> {
    return this.http.get<Regulation>(`${this.apiUrl}/regulations/${id}`);
  }
}
