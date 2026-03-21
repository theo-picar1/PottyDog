export interface Device {
  id: number;
  name: string;
  location: string;
  status: 'Off' | 'Inactive' | 'Movement';
  isOffline: boolean;
  hasCamera: boolean;
}

export interface DashboardData {
  noDevices: Device[];
  devices: Device[];
};

export const dashboardData: DashboardData = {
  noDevices: [

  ],
  devices: [
    {
      id: 1,
      name: "Backgarden device",
      location: "Kitchen",
      status: "Inactive",
      isOffline: true,
      hasCamera: false
    },
    {
      id: 2,
      name: "Living room device",
      location: "Living Room",
      status: "Off",
      isOffline: true,
      hasCamera: false
    },
    {
      id: 3,
      name: "Bedroom device",
      location: "Bedroom",
      status: "Inactive",
      isOffline: true,
      hasCamera: false
    },
    {
      id: 4,
      name: "Kitchen device",
      location: "Kitchen",
      status: "Off",
      isOffline: true,
      hasCamera: false
    },
    {
      id: 5,
      name: "Bedroom 2 device",
      location: "Bedroom",
      status: "Movement",
      isOffline: true,
      hasCamera: false
    },
  ]
}