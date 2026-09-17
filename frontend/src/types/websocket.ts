import { DetectionEvent } from './detection';

export interface WebSocketMessage {
  frame: string; // Base64 encoded JPEG
  events: DetectionEvent[];
}
