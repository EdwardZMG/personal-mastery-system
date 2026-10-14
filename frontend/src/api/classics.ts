import request from './index';

export function getClassicProgress(classicName: string): Promise<any> {
  return request.get(`/classics/${classicName}`) as any;
}

export function getAllClassicsProgress(): Promise<any> {
  return request.get('/classics/progress') as any;
}

export function updateProgress(data: { classic_name: string; chapter_number: number; status: string; mastery_level: number }): Promise<any> {
  return request.put('/classics/progress', data) as any;
}

export function getClassicsStats(): Promise<any> {
  return request.get('/classics/stats') as any;
}
