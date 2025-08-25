import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs
import { catchError } from 'rxjs/operators

@Injectable({
  providedIn: 'root'
})
export class SpeechService {

  private baseUrl = ' http://127.0.0.1:8000';  // Your backend URL
  public threadId: string = '';  // Set this from component or elsewhere as needed

  constructor(private http: HttpClient) { }

  uploadAudio(file: File): Observable<any> {
    const headers = new HttpHeaders().set('thread-id', this.threadId);
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.baseUrl}/process_audio/`, formData, { headers })
      .pipe(
        catchError(this.handleError)
      );
  }
  sendTextToServer(payload: any): Observable<any>{
    const headers = new HttpHeaders().set('thread-id', payload?.threadId);
    return this.http.post(`${this.baseUrl}/process_text/`, payload, { headers })
    .pipe(
      catchError(this.handleError)
    );
  }

  // Optional: Error handling for HTTP requests
  private handleError(error: HttpErrorResponse) {
    console.error('Upload failed:', error);
    return throwError(() => new Error('Error uploading audio file; please try again later.'));
  }

}

