import requests
import json

from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="columbus-5",
    url="https://lcd.terra.dev"
)

# print(terra.market.swap_rate('100uusd', 'uluna'))

# print(requests.get('https://fcd.terra.dev/v1/market/price?denom=uusd&interval=1h').json())

# Populate the address and contact variables
pairs = {
    "luna_bluna_terraswap": "terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p",
    "luna_lunax_terreswap": "terra1zrzy688j8g6446jzd88vzjzqtywh6xavww92hy",
    "luna_bluna_loop": "terra1v93ll6kqp33unukuwls3pslquehnazudu653au",
    "luna_lunax_loop": "terra1ga8dcmurj8a3hd4vvdtqykjq9etnw5sjglw4rg",
}

query_msg = json.dumps({
    "simulation": {
        "offer_asset": {
            "amount": "1000000",
            "info": {"native_token": {"denom": "uluna"}}
        }
    }
})

for p in pairs:
    response = requests.get(
        "https://lcd.terra.dev/wasm/contracts/" + pairs[p] + "/store",
        params={"query_msg": query_msg},
    ).json()
    price = int(response["result"]["return_amount"])/1000000 - 1
    print(p, '{:.2f}%'.format(price*100))
