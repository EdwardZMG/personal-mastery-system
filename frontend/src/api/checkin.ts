import request from './index';

export function getTodayCheckin(): Promise<any> {
  return request.get('/checkins/today') as any;
}

export function listCheckins(params?: { start_date?: string; end_date?: string; limit?: number }): Promise<any> {
  return request.get('/checkins/', { params }) as any;
}

export function createCheckin(data: {
  mood?: number;
  energy_level?: number;
  focus_areas?: string[];
  reflections?: string;
  achievements?: string;
  challenges?: string;
  tomorrow_plan?: string;
}): Promise<any> {
  return request.post('/checkins/', data) as any;
}
