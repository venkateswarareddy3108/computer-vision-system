import { Person, PersonListResponse } from '../types/person';

const API_BASE_URL = '/api/v1';

export const api = {
  // Persons
  getPersons: async (page = 1, perPage = 50, search = ''): Promise<PersonListResponse> => {
    const params = new URLSearchParams({ page: page.toString(), per_page: perPage.toString() });
    if (search) params.append('search', search);
    
    const response = await fetch(`${API_BASE_URL}/persons/?${params}`);
    if (!response.ok) throw new Error('Failed to fetch persons');
    return response.json();
  },

  getPerson: async (id: string): Promise<Person> => {
    const response = await fetch(`${API_BASE_URL}/persons/${id}`);
    if (!response.ok) throw new Error('Failed to fetch person');
    return response.json();
  },

  createPerson: async (data: Partial<Person>): Promise<Person> => {
    const response = await fetch(`${API_BASE_URL}/persons/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Failed to create person');
    }
    return response.json();
  },

  registerFace: async (personId: string, file: File, replaceExisting = false) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('replace_existing', replaceExisting.toString());

    const response = await fetch(`${API_BASE_URL}/persons/${personId}/face`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Failed to register face');
    }
    return response.json();
  },

  deletePerson: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/persons/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete person');
    return response.json();
  },

  // Detection
  startDetection: async (cameraIndex = 0) => {
    const response = await fetch(`${API_BASE_URL}/detection/start?camera_index=${cameraIndex}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to start detection');
    return response.json();
  },

  stopDetection: async () => {
    const response = await fetch(`${API_BASE_URL}/detection/stop`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to stop detection');
    return response.json();
  },

  getDetectionStatus: async () => {
    const response = await fetch(`${API_BASE_URL}/detection/status`);
    if (!response.ok) throw new Error('Failed to get status');
    return response.json();
  }
};
