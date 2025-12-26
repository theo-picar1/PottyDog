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

    // Remove initial message when hardware not active
    const placeholder = document.getElementById("status-placeholder")
    if (placeholder) placeholder.remove()
    text.innerText = ` ${message}`
}

document.addEventListener("DOMContentLoaded", () => {
    const pubnub = new PubNub({
        subscribeKey: PUBNUB_SUB_KEY,
        uuid: "pottydog-website"
    })

    pubnub.subscribe({
        channels: ["Channel-Barcelona"]
    })

    pubnub.addListener({
        message: function (event) {
            const motion = event.message.motion
            if (!statusMap.has(motion)) return

            const [message, imagePath] = statusMap.get(motion)
            updateStatusUI(motion, message, imagePath)
        }
    })
})