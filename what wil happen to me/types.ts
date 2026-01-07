
export type Stage = 'START' | 'PRESET' | 'CALLING' | 'CONNECTING' | 'IN_CALL' | 'RESULT';

export interface PresetData {
  jumpHeight: string;
  balloonSize: string;
  heliumRate: string;
  weight: string;
  landingScene: string;
}

export interface Role {
  id: string;
  name: string;
  title: string;
  avatar: string;
  personality: string;
  color: string;
}

export interface Message {
  roleId: string;
  content: string;
  timestamp: number;
}

export interface DiscussionHistory {
  question: string;
  answers: Record<string, string>;
  finalSummary: string;
}
