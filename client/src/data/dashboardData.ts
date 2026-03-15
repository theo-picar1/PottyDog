export interface Device {
  id: number;
  name: string;
  location: string;
}

export interface DashboardData {
  noDevices: Device[];
  hasDevices: Device[];
};;

export const dashboardData: DashboardData = {
  noDevices: [

  ],
  hasDevices: [
    {
      id: 1,
      name: "Backgarden device",
      location: "Kitchen"
    },
    {
      id: 2,
      name: "Living room device",
      location: "Living Room"
    },
    {
      id: 3,
      name: "Bedroom device",
      location: "Bedroom"
    },
    {
      id: 4,
      name: "Kitchen device",
      location: "Kitchen"
    },
    {
      id: 5,
      name: "Bedroom 2 device",
      location: "Bedroom"
    },
  ]
}