import request from './index';

export function getSystemStats(): Promise<any> {
  return request.get('/admin/stats') as any;
}

export function getAdminContents(params?: { content_type?: string; limit?: number; offset?: number }): Promise<any[]> {
  return request.get('/admin/content/', { params }) as any;
}

export function createContent(data: { title: string; content_type: string; category: string; description?: string }): Promise<any> {
  return request.post('/admin/content/', data) as any;
}

export function updateContent(id: string, data: { title?: string; description?: string; is_active?: boolean }): Promise<any> {
  return request.put(`/admin/content/${id}`, data) as any;
}

export function deleteContent(id: string): Promise<void> {
  return request.delete(`/admin/content/${id}`) as any;
}
