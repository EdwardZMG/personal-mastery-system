import request from './index';

export interface LearningContent {
  id: string;
  title: string;
  content_type: string;
  domain: string;
  url: string;
  duration_minutes: number;
  summary: string;
  created_at: string;
}

export interface LearningRecord {
  id: string;
  content_id: string;
  duration_minutes: number;
  status: string;
  notes: string;
  completed_at: string;
}

export function getContentList(params?: { content_type?: string; domain?: string; limit?: number; offset?: number }): Promise<LearningContent[]> {
  return request.get('/learning/content', { params }) as any;
}

export function getContentDetail(id: string): Promise<LearningContent> {
  return request.get(`/learning/content/${id}`) as any;
}

export function logLearning(data: { content_id: string; duration_minutes: number; status: string; notes?: string }): Promise<LearningRecord> {
  return request.post('/learning/record', data) as any;
}

export function getLearningHistory(params?: { limit?: number; offset?: number }): Promise<LearningRecord[]> {
  return request.get('/learning/records', { params }) as any;
}
