export const MESSAGES = {
  DEVICE: {
    DEVICE_LOCATION_TEXT: (location: string) => `Location: ${location}`,
    NO_CAMERA_TEXT: "This device has no camera",
    CAMERA_OFFLINE_TEXT: "Camera is currently offline",
    CONFIRM_DELETE_TEXT: "All device data will be permanently removed. Would you like to proceed?"
  },
  BUTTON: {
    LOGIN_TEXT: "Login",
    CLEAR_TEXT: "Clear",
    GO_TO_DEVICE_TEXT: "Go to device",
    ADD_DEVICE_TEXT: "Add device",
    YOUR_ACCOUNT_TEXT: "Your account",
    LOGOUT_TEXT: "Log out",
    CLOSE_TEXT: "Close",
    BACK_TO_DASHBOARD_TEXT: "Back to dashboard",
    EDIT_DEVICE_TEXT: "Edit device",
    DELETE_DEVICE_TEXT: "Delete device",
    SAVE_CHANGES_TEXT: "Save changes",
    CANCEL_TEXT: "Cancel",
    CONFIRM_TEXT: "Confirm",
  },
  LABEL: {
    EMAIL_ADDRESS_LABEL: "Email address",
    PASSWORD_LABEL: "Password",
    DEVICE_LOCATION_LABEL: "Location",
    DEVICE_NAME_LABEL: "Device name",
  },
  TITLE: {
    WEBSITE_TITLE: "PottyDog",
    DEVICES_DASHBOARD_TITLE: "Your devices",
    NOT_AVAILABLE_TITLE: "Currently not available",
    EDIT_DEVICE_TITLE: "Edit device",
    DELETE_DEVICE_TITLE: "Delete device"
  },
  ERRORS: {
    INVALID_EMAIL_ERROR: "Please enter a valid email address",
    EMAIL_REQUIRED_ERROR: "Email is required",
    PASSWORD_REQUIRED_ERROR: "Password is required",
  }
  COMMON: {
    UNDER_DEV_TEXT: "This feature is currently not available. Please try another time!",
    LOGIN_CONTACT_TEXT: "Please contact theopicar@example.com if you are having any issues logging in."
  }
}