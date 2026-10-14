import request from './index';

export interface SpeechDraft {
  id: string;
  topic: string;
  template_type: string;
  estimated_duration: number;
  full_speech: string;
  speaker_notes: string;
  status: string;
  feedback_score: number;
  created_at: string;
}

export interface SpeechGenerateParams {
  topic: string;
  template_type: string;
  key_points: string[];
  audience?: string;
  tone?: string;
  target_duration?: number;
}

export function getSpeechList(params?: { template_type?: string; status_filter?: string; limit?: number; offset?: number }): Promise<SpeechDraft[]> {
  return request.get('/speech/', { params }) as any;
}

export function getSpeechDetail(id: string): Promise<SpeechDraft> {
  return request.get(`/speech/${id}`) as any;
}

export function generateSpeech(data: SpeechGenerateParams): Promise<SpeechDraft> {
  return request.post('/speech/generate', data) as any;
}
