export const MESSAGES = {
  DEVICE: {
    DEVICE_LOCATION_TEXT: (location: string) => `Location: ${location}`,
    NO_CAMERA_TEXT: "This device has no camera",
    CAMERA_OFFLINE_TEXT: "Camera is currently offline",
    CONFIRM_DELETE_TEXT: "All device data will be permanently removed. Would you like to proceed?",
    NO_DEVICES_TEXT: "No devices found. Set one up now!",
    NO_DEVICE_TEXT: "No device found."
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
    ERROR_TITLE: "An error has occured"
  },
  PLACEHOLDERS: {
    DEVICE_NAME_PLACEHOLDER: "Enter new device name",
    DEVICE_LOCATION_PLACEHOLDER: "Enter new device location"
  },
  ERRORS: {
    INVALID_EMAIL_ERROR: "Please enter a valid email address",
    EMAIL_REQUIRED_ERROR: "Email is required",
    PASSWORD_REQUIRED_ERROR: "Password is required",
    DEVICE_NAME_REQUIRED_ERROR: "Device name is required",
    INVALID_DEVICE_NAME_LENGTH_ERROR: "Name must be between 2 and 30 characters",
    DEVICE_LOCATION_REQUIRED_ERROR: "Device location is required",
    STATUS_0_ERROR: "Unable to connect to the server.",
    STATUS_403_ERROR: "You do not have permission to access this resource.",
    STATUS_500_ERROR: "An unexpected server error has occured.",
    STATUS_503_ERROR: "This service is temporarily unavailable."
  },
  COMMON: {
    UNDER_DEV_TEXT: "This feature is currently not available. Please try another time!",
    LOGIN_CONTACT_TEXT: "Please contact theopicar@example.com if you are having any issues logging in.",
    LOADING_TEXT: "Loading...",
    DYNAMIC_LOADING_TEXT: (text: string) => `Loading ${text}...`
  }
}