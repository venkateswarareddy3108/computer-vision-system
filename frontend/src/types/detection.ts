export interface DetectionEvent {
  tracking_id: number;
  bbox: [number, number, number, number];
  confidence: number;
  face_bbox?: [number, number, number, number] | null;
  face_confidence?: number | null;
  hands_count: number;
  fingers_count: number;
  eye_state: string;
  awake_status: string;
  estimated_expression: string;
  expression_confidence: number;
  timestamp: number;
  person?: {
    uuid: string;
    person_id: string;
    name: string;
    department?: string;
  };
  distance?: number;
}
