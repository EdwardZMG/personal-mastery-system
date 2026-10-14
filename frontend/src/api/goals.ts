import request from './index';

export interface Goal {
  id: string;
  title: string;
  description: string;
  priority: number;
  category: string;
  deadline?: string;
  progress_percent: number;
  status: string;
  created_at: string;
}

export function getGoals(): Promise<Goal[]> {
  return request.get('/goals/') as any;
}

export function getGoalDetail(id: string): Promise<Goal> {
  return request.get(`/goals/${id}`) as any;
}

export function createGoal(data: { title: string; description?: string; priority?: number; category?: string; deadline?: string }): Promise<Goal> {
  return request.post('/goals/', data) as any;
}

export function updateGoal(id: string, data: Partial<Goal>): Promise<Goal> {
  return request.put(`/goals/${id}`, data) as any;
}

export function deleteGoal(id: string): Promise<void> {
  return request.delete(`/goals/${id}`) as any;
}
