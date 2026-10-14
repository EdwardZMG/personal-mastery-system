import request from './index';

export interface ReviewSession {
  id: string;
  review_type: string;
  scheduled_time: string;
  completed_time?: string;
  status: string;
  responses?: string;
  summary?: string;
  created_at: string;
}

export function getReviewList(params?: { review_type?: string; status_filter?: string; limit?: number; offset?: number }): Promise<ReviewSession[]> {
  return request.get('/review/', { params }) as any;
}

export function getReviewDetail(id: string): Promise<ReviewSession> {
  return request.get(`/review/${id}`) as any;
}

export function triggerReviewSession(data: { review_type: string }): Promise<ReviewSession> {
  return request.post('/review/trigger', data) as any;
}

export function submitReview(id: string, data: { responses: string; new_insights?: object }): Promise<ReviewSession> {
  return request.post(`/review/${id}/respond`, data) as any;
}
