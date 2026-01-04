// String is motion, value is [message, imagePath]
const statusMap = new Map([
    ["inactive", ["has not been around the door!", "/static/images/inactive_dog.png"]],
    ["detected", ["is around the door. Be ready!", "/static/images/happy_dog.png"]],
    ["potty", ["is waiting to go out!", "/static/images/need_potty.png"]]
])

// UI styles ffor motion status
const statusStyles = {
    inactive: {
        border: "border-secondary",
        text: "text-muted",
        filter: "grayscale(100%) brightness(75%)"
    },
    detected: {
        border: "border-warning",
        text: "text-warning",
        filter: "grayscale(20%) brightness(95%)"
    },
    potty: {
        border: "border-danger",
        text: "text-danger",
        filter: "grayscale(0%) brightness(100%)"
    }
}

// Update dashboard status based on motion message
function updateStatusUI(status, message, imagePath) {
    const card = document.getElementById("status-card")
    const img = document.getElementById("status-image")
    const text = document.getElementById("status-message")

    if (!card || !img || !text) return

    // Reset previous styles
    card.classList.remove("border-secondary", "border-warning", "border-danger")
    text.classList.remove("text-muted", "text-warning", "text-danger")

    // Apply new styles
    const style = statusStyles[status]
    card.classList.add(style.border)
    text.classList.add(style.text)

    img.style.filter = style.filter
    img.src = imagePath

    // Show buttons for logging if potty time
    // const buttons = document.getElementById('potty-log-buttons')
    // if (status === "potty") {
    //     buttons.style.display = "flex"  
    // } 
    // else {
    //     buttons.style.display = "none"
    // }

    // Remove initial message when hardware not active
    const placeholder = document.getElementById("status-placeholder")
    if (placeholder) placeholder.remove()
    text.innerText = ` ${message}`
}

document.addEventListener("DOMContentLoaded", () => {
    // Get user's PubNub token based on permissions
    fetch("/get_pubnub_token", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            // No registered device yet
            if (!data.token) {
                alert(data.message)
                return
            }

            // No read access
            if(!data.can_read) {
                alert("You do not have the permissions to use the tracker. Please contact the admin.")
                return
            }

            const pubnub = new PubNub({
                subscribeKey: PUBNUB_SUB_KEY,
                authKey: data.token,
                uuid: "dashboard-" + String(data.username)
            })

            pubnub.subscribe({ channels: ["Channel-Barcelona"] })

            // For changing mascot UI depending on PubNub motion message
            pubnub.addListener({
                message: function (event) {
                    const motion = event.message.motion
                    if (!statusMap.has(motion)) return

                    const [message, imagePath] = statusMap.get(motion)
                    updateStatusUI(motion, message, imagePath)
                }
            })
        })
        .catch(err => console.error("Error fetching token:", err))
})