import request from './index';

export function getDashboardOverview(): Promise<any> {
  return request.get('/dashboard/overview') as any;
}

export function getKnowledgeStats(): Promise<any> {
  return request.get('/dashboard/knowledge-stats') as any;
}

export function getLearningTimeline(params?: { days?: number }): Promise<any> {
  return request.get('/dashboard/learning-timeline', { params }) as any;
}

export function getMaskScores(): Promise<any> {
  return request.get('/dashboard/mask-scores') as any;
}

export function getPhysicalScores(): Promise<any> {
  return request.get('/dashboard/physical-scores') as any;
}

export function getMaslowScores(): Promise<any> {
  return request.get('/dashboard/maslow-scores') as any;
}
