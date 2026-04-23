// TypeScript type definitions for Fitness Tracking App

export interface Workout {
  id: number;
  user_name: string;
  activity: string;
  duration: number;
  calories: number;
}

export interface WorkoutCreate {
  user_name: string;
  activity: string;
  duration: number;
}

export interface WorkoutUpdate {
  user_name?: string;
  activity?: string;
  duration?: number;
  calories?: number;
}
