import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserThreadService {
  // Initialize BehaviorSubject with empty string (or null, or any default)
  private threadSubject: BehaviorSubject<string> = new BehaviorSubject<string>('');

  // Observable stream to subscribe to thread value changes
  thread$: Observable<string> = this.threadSubject.asObservable();

  constructor() {}

  // Emit new thread value
  setThread(threadId: string): void {
    this.threadSubject.next(threadId);
  }

  // Get current thread value (latest emitted)
  getThread(): string {
    return this.threadSubject.getValue();
  }
}
