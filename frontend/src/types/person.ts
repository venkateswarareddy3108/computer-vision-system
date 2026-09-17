export interface Person {
  id: string;
  person_id: string;
  name: string;
  email?: string;
  phone?: string;
  department?: string;
  role?: string;
  additional_info: Record<string, any>;
  face_image_path?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  has_face_embedding: boolean;
}

export interface PersonListResponse {
  persons: Person[];
  total: number;
  page: number;
  per_page: number;
}
