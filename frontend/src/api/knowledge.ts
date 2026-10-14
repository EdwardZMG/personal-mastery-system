import request from './index';

export interface KnowledgeItem {
  id: string;
  content: string;
  domain: string;
  intent: string;
  tags: string[];
  source: string;
  language: string;
  status: string;
  created_at: string;
}

export interface KnowledgeListParams {
  domain?: string;
  intent?: string;
  status_filter?: string;
  limit?: number;
  offset?: number;
}

export function getKnowledgeList(params?: KnowledgeListParams): Promise<KnowledgeItem[]> {
  return request.get('/knowledge/', { params }) as any;
}

export function getKnowledgeDetail(id: string): Promise<KnowledgeItem> {
  return request.get(`/knowledge/${id}`) as any;
}

export function createKnowledge(data: { content: string; domain?: string; source?: string; language?: string }): Promise<KnowledgeItem> {
  return request.post('/knowledge/capture', data) as any;
}

export function getStructuredKnowledge(id: string): Promise<any> {
  return request.get(`/knowledge/knowledge/${id}`) as any;
}
