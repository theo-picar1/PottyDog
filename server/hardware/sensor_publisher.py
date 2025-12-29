from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Create PubNub object
pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("SUBSCRIBE_KEY")
pnconfig.uuid = "raspberry-pi"
pubnub = PubNub(pnconfig)

# The pi's own device ID. This NEEDS to be manually set for comms to work with PubNub
channel_name = os.getenv("device_id")

def publish_motion(state):
    pubnub.publish().channel(channel_name).message({
        "motion": state,
        "timestamp": time.time()
    }).sync()