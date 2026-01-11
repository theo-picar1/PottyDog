from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import time
import os

load_dotenv("/home/pi/PottyDog/.env")

# Create PubNub object
pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("SUBSCRIBE_KEY")
pnconfig.uuid = "raspberry-pi"
pubnub = PubNub(pnconfig)
pubnub.set_token(os.getenv("PUBLISH_TOKEN"))

def publish_motion(state):
    pubnub.publish().channel("Channel-Barcelona").message({
        "motion": state,
        "timestamp": time.time()
    }).sync()