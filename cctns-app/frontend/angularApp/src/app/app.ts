import { Component, signal } from "@angular/core";
import { SpeechService } from "../services/speech-service";

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: false,
  styleUrls: ['./app.css']   // <-- fix here: styleUrls (array)
})
export class App {
  protected readonly title = signal('angularChat');
  response: any;
  highlights: string[] = [
    "Voice-Enabled Access: Enables police personnel to interact with the CCTNS database using natural language voice commands.",
    "Democratized Data Access: Removes technical barriers, allowing officers at all levels—from constables to senior officials—to retrieve crime and investigation data effortlessly.",
    "Multi-Language Support: Supports English and optionally Telugu to cater to a wider range of users.",
    "AI-Powered Query Interpretation: Converts spoken queries into precise, safe SQL statements for accurate data retrieval.",
    "Secure Middleware Layer: Ensures input sanitization, secure data handling, and strict access control.",
    "Real-Time Error Detection: Provides immediate feedback and step-by-step clarifications to enhance query accuracy.",
    "Interactive Query Refinement: Helps users refine their requests with suggestions to prevent data misinterpretation or inaccuracies.",
    "Structured Report Generation: Produces readable reports with tables, charts, and summaries suitable for field operations and management.",
    "Scalable Client-Server Architecture: Designed to adapt seamlessly across various police stations in Andhra Pradesh.",
    "Enhanced Operational Efficiency: Empowers police personnel with reliable, timely information to improve decision-making and workflow."
  ];

  constructor() {}
}
