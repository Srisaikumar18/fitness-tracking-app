import axios, { AxiosInstance } from 'axios';
import type {
  Workout,
  WorkoutCreate,
  WorkoutUpdate,
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Workout endpoints
  async createWorkout(workoutData: WorkoutCreate): Promise<Workout> {
    const response = await this.client.post<Workout>('/api/workouts/', workoutData);
    return response.data;
  }

  async getWorkouts(): Promise<Workout[]> {
    const response = await this.client.get<Workout[]>('/api/workouts/');
    return response.data;
  }

  async updateWorkout(workoutId: number, workoutData: WorkoutUpdate): Promise<Workout> {
    const response = await this.client.put<Workout>(
      `/api/workouts/${workoutId}`,
      workoutData
    );
    return response.data;
  }

  async deleteWorkout(workoutId: number): Promise<void> {
    await this.client.delete(`/api/workouts/${workoutId}`);
  }
}

export const apiClient = new ApiClient();
