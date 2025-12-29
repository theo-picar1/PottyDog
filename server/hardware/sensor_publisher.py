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

def publish_motion(state):
    pubnub.publish().channel("Channel-Barcelona").message({
        "motion": state,
        "timestamp": time.time()
    }).sync()