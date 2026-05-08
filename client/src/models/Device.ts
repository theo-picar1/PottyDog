export interface Device {
  id: number;
  user_id: number;
  device_name: string;
  device_location: string;
  status: 'idle' | 'active' | 'offline';
  hasCamera: boolean;
}