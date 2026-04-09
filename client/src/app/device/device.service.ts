import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import { Device } from "../../data/dashboardData";

@Injectable() 
export class DeviceService {
    private deviceSource = new BehaviorSubject(null);
    private deletedDeviceSource = new BehaviorSubject(-1);
    device = this.deviceSource.asObservable();
    deletedDevice = this.deletedDeviceSource.asObservable();

    constructor() {}

    updateDevice(newDevice: Device) {
        // Update device on editing
    }

    updateDeletedDeviceId(deviceId: number) {
        // Delete device on Id
    }
}