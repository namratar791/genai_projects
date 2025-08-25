import { Component, NgZone, OnDestroy, OnInit } from '@angular/core';
import { SpeechService } from '../../services/speech-service';
import { UserThreadService } from '../../services/user-thread-service';
import { Subscription } from 'rxjs

export interface CaseDetails {
  caseId: number;
  crime_type: string;
  location: string;
  date_registered: string;
  status: string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.html',
  styleUrls: ['./chat.css'],
  standalone: false
})
export class Chat implements OnInit, OnDestroy{
  messages: { text: string; fromUser: boolean; timestamp: Date, type: string, dbResults: null | CaseDetails[]  }[] = [];
  messageInput = '';
  minimized = true;

  recording = false;
  loading = false
  mediaRecorder: any;
  audioChunks: Blob[] = [];
  cancelled = false;

  currentThread: string = '';
  private threadSub?: Subscription;

  constructor(private speechService: SpeechService, private ngZone: NgZone, private userThreadService: UserThreadService) {}

  ngOnInit() {
    this.messages.push({
      text: "Hello! Welcome to AI powered voice based Bot.", fromUser: false, timestamp: new Date(), type: 'text', dbResults: null 
    },
    {
      text: "How can I help you today?", fromUser: false, timestamp: new Date(), type: 'text', dbResults: null 
    })
    // Subscribe to thread updates
    this.threadSub = this.userThreadService.thread$.subscribe(threadId => {
      this.currentThread = threadId;
      console.log('Thread updated:', threadId);
    });

    // Optionally, get current value synchronously
    const currentValue = this.userThreadService.getThread();
    console.log('Current thread value on init:', currentValue);
  }


  // Example method to emit/set a new thread value
  updateThread(newThreadId: string) {
    this.userThreadService.setThread(newThreadId);
  }
  toggleMinimize() {
    this.minimized = !this.minimized;
  }

  sendMessage() {
    const message = this.messageInput.trim();
    if (!message) return;

    this.messages.push({
      text: message,
      fromUser: true,
      timestamp: new Date(),
      type: 'text',
      dbResults: null
    });
    this.messageInput = '';

  }

  startRecording() {
    this.cancelled = false; // reset
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert('Audio recording not supported in this browser.');
      return;
    }
    this.audioChunks = [];
  
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      this.mediaRecorder = new MediaRecorder(stream);
      this.mediaRecorder.start();
      this.recording = true;
  
      this.mediaRecorder.addEventListener('dataavailable', (event: any) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      });
  
      this.mediaRecorder.addEventListener('stop', () => {
        // Stop all tracks to release mic
        stream.getTracks().forEach((track) => track.stop());
  
        if (!this.cancelled) {
          // Only send if NOT cancelled
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
          this.sendAudioToServer(audioBlob);
        } else {
          console.log('Recording cancelled — not sending audio');
          this.loading = false;
        }
  
        this.ngZone.run(() => {
          this.recording = false;
          // this.loading = false;
        });
      });
    });
  }
  
  stopRecording() {
    if (this.mediaRecorder && this.recording) {
      this.mediaRecorder.stop();
      this.cancelled = false; // normal stop
    }
    console.log("stop is called.....");
  }
  
  cancelRecording() {
    if (this.mediaRecorder && this.recording) {
      this.cancelled = true; // mark cancel
      this.mediaRecorder.stop();
    }
    this.audioChunks = [];
    this.recording = false;
    console.log('Recording cancelled and stopped');
  }

  sendAudioToServer(audioBlob: Blob) {
    this.loading = true;
    const audioFile = new File([audioBlob], 'voice_message.wav', { type: 'audio/wav' });
    this.speechService.uploadAudio(audioFile).subscribe(
      (res: any) => {

        this.currentThread = res?.thread_id || '';
        this.updateThread(this.currentThread)
        this.messageInput = res?.response?.user_query;
        this.loading = false;
      },
      (err: any) => {
        this.loading = false;
        console.error('Speech to text failed', err);
        alert('Speech to text conversion failed.');
      }
    );
  }
  sendTextToServer() {
    const payload = {
      'user_query': this.messageInput,
      'threadId': this.currentThread
    }
    this.speechService.sendTextToServer(payload).subscribe(
      (res: any) => {
        
        this.currentThread = res?.thread_id || '';
        this.updateThread(this.currentThread)
        
        if( res?.response?.is_complete == 'complete') {
          let list = res?.response?.db_results 
          
          let result = list && list?.length > 0 ? this.get_converetd(list) : []
          console.log(result,"::::::::::::::")
          
          // let list = res?.response?.db_results
            this.messages.push({
              text: '',
              fromUser: false,
              timestamp: new Date(),
              dbResults: result,
              type: 'dbResults'
            });
        } else {
          this.messages.push({
            text: res?.response?.final_response,
            fromUser: false,
            timestamp: new Date(),
            dbResults: null,
            type: 'text'
          });
        }

      },
      (err: any) => {
        console.error('Speech to text failed', err);
        alert('Speech to text conversion failed.');
      }
    );
  }

  get_converetd(list: any){
    const keys = ["caseId", "crime_type", "location", "date_registered", "status"];
    const converted = list.map((item: any) => {
      const obj: any = {};
      keys.forEach((key, i) => {
        obj[key] = item[i];
      });
      return obj;
    });

    return converted;
  }

  hasResults(msg: any){
    return !!(msg?.dbResults?.length > 0)
  }
  ngOnDestroy() {
    // Unsubscribe to avoid memory leaks
    this.threadSub?.unsubscribe();
  }
}
