from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
import os

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Replace with your bot token

client = WebClient(token=SLACK_BOT_TOKEN)

try:
    client.chat_postMessage(
        channel="#test_channel",
        text="Hey everyone, have you seen the latest gold mining shares? Prices have been fluctuating quite a bit lately.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Yeah, I noticed! The recent surge in gold prices seems to be pushing up mining stocks. Barrick Gold's share price hit a nice high recently.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Exactly. Barrick's up by about 3% this week. However, there’s a lot of volatility too. One moment it's up, then it dips back down. The overall market sentiment is a bit unstable.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="It’s a bit of a wait-and-see situation, right? I think if you’re looking for short-term gains, mining shares could be a solid pick, but for long-term, I’m cautious about putting too much in the sector right now.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="True. With inflation and interest rate concerns globally, the gold price might still see some spikes, but the broader market could be pulling back, which affects gold stocks too.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Agreed. On top of that, geopolitical tensions, especially in regions with major mines, can have a significant impact on share prices. That risk is something we have to monitor closely.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="So, what’s the play here? Do we lean into big players like Barrick and Newmont, or diversify with smaller miners to spread the risk?",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="For me, I’d go with a balanced approach. Look at companies with strong fundamentals, solid reserves, and a good track record of navigating market volatility. But I’d keep a small portion in smaller miners for some high-reward potential.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Solid strategy. I’ve also been looking into ETFs that track mining stocks. Easier to diversify and still benefit from the sector's movement. Any thoughts on that?",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="ETFs are a great way to reduce single-stock risk. If you’re in it for a safer play, something like the VanEck Vectors Gold Miners ETF could be a good option. It’s got exposure to top-tier miners and still moves with the market trends.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="That’s a good point. ETFs provide a good mix of stability and exposure, especially if you’re looking to get into the gold mining sector without going all-in on individual stocks.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Yeah, and don’t forget to keep an eye on the cost of production for these companies. If gold prices continue to rise, higher-cost miners will have a much harder time keeping their margins healthy.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text="Great insights. Looks like it’s all about balancing risk. Thanks, everyone! I’m leaning towards an ETF and holding on to some bigger miners for now.",
        user="U08EX40QWRF"
    )
    
    client.chat_postMessage(
        channel="#test_channel",
        text= "Hey, I’m heading to Sydney this weekend with some friends, and we’re looking for some awesome food spots to hit up. Any recommendations?",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "Oh, you’re in for a treat! Sydney has some great food spots. If you’re into seafood, you have to check out Sydney Fish Market. It’s an iconic spot with fresh seafood straight from the ocean. You can get oysters, sushi, and the best fish and chips.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "I second that! Also, Chin Chin in Surry Hills is amazing for modern Thai food. Super vibrant and flavorful, and their pad Thai is next-level. Don’t skip the crispy pork belly either!",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "If you want something more laid-back, try The Grounds of Alexandria. It’s a beautiful café with a huge variety of options. Perfect for brunch or lunch. They do this epic banana bread that you can't miss!",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "That’s a great pick, Emma! And if you're craving something sweet, check out Black Star Pastry in Newtown. They’ve got this famous strawberry watermelon cake, it’s totally Instagram-worthy and delicious.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "For something a bit fancier, Aria near Circular Quay is a great spot for modern Australian fine dining. The views of the Opera House and Harbour Bridge are stunning. A bit on the pricier side, but worth it for a special night out.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "Ooh, I’m loving these ideas! What about after dinner? Any good bars for cocktails?",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "If you’re looking for cocktails, Maybe Sammy is a must. It’s a swanky cocktail bar in The Rocks. The vibe is awesome, and their cocktails are some of the best in Sydney.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "If you want something a little more laid-back but still cool, head over to The Baxter Inn. It’s a hidden gem with an extensive whiskey selection. Plus, the atmosphere is super cozy.",
        user="U08EX40QWRF"
    )

    client.chat_postMessage(
        channel="#test_channel",
        text= "For a more upscale vibe, The Rockpool Bar & Grill is great for drinks with a view, especially at sunset. It’s a nice spot to unwind after dinner.",
        user="U08EX40QWRF"
    )

except SlackApiError as e:
    print(f"Error posting message: {e.response['error']}")
