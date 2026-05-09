import { Device } from "../models/Device";

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
      user_id: 1,
      device_name: "Backgarden device",
      device_location: "Kitchen",
      status: "idle",
      has_camera: true
    },
    {
      id: 2,
      user_id: 1,
      device_name: "Living room device",
      device_location: "Living Room",
      status: "idle",
      has_camera: false
    },
    {
      id: 3,
      user_id: 1,
      device_name: "Bedroom device",
      device_location: "Bedroom",
      status: "idle",
      has_camera: true
    },
    {
      id: 4,
      user_id: 1,
      device_name: "Kitchen device",
      device_location: "Kitchen",
      status: "offline",
      has_camera: false
    },
    {
      id: 5,
      user_id: 1,
      device_name: "Bedroom 2 device",
      device_location: "Bedroom",
      status: "active",
      has_camera: false
    },
  ]
}