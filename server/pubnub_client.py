from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import os

load_dotenv()

def create_pubnub(uuid):
    pnconfig = PNConfiguration()
    pnconfig.publish_key = os.getenv("PUBLISH_KEY")
    pnconfig.subscribe_key = os.getenv("SUBSCRIBE_KEY")
    pnconfig.uuid = uuid
    return PubNub(pnconfig)