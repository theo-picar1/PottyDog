from ..pubnub_client import create_pubnub
import time

pubnub = create_pubnub("raspberry-pi")

def publish_motion(state):
    pubnub.publish().channel("Channel-Barcelona").message({
        "motion": state,
        "timestamp": time.time()
    }).sync()