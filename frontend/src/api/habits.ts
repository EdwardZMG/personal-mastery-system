import request from './index';

export interface Habit {
  id: string;
  name: string;
  description: string;
  frequency: string;
  target_count: number;
  current_streak: number;
  longest_streak: number;
  created_at: string;
}

export function getHabits(): Promise<Habit[]> {
  return request.get('/habits/') as any;
}

export function createHabit(data: { name: string; description?: string; frequency?: string; target_count?: number }): Promise<Habit> {
  return request.post('/habits/', data) as any;
}

export function logHabit(habitId: string, data: { count?: number; note?: string }): Promise<any> {
  return request.post(`/habits/${habitId}/log`, data) as any;
}

export function getHabitLogs(habitId: string): Promise<any[]> {
  return request.get(`/habits/${habitId}/logs`) as any;
}

export function getHabitStats(): Promise<any> {
  return request.get('/habits/stats') as any;
}
