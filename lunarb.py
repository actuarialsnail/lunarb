# pip install terra_sdk
from terra_sdk.client.lcd import LCDClient
import requests
import json
import time

starttime = time.time()


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
    "luna_bluna_astroport": "terra1j66jatn3k50hjtg2xemnjm8s7y8dws9xqa5y8w",
    "luna_lunax_astroport": "terra1qswfc7hmmsnwf7f2nyyx843sug60urnqgz75zu"
}

query_msg = json.dumps({
    "simulation": {
        "offer_asset": {
            "amount": "1000000",
            "info": {"native_token": {"denom": "uluna"}}
        }
    }
})

while True:

    stader_res = requests.get(
        'https://fcd.terra.dev/terra/wasm/v1beta1/contracts/terra1xacqx447msqp46qmv8k2sq6v5jh9fdj37az898/store',
        params={"query_msg": "eyJzdGF0ZSI6e319"}
    ).json()

    stader_unbond_price = float(
        stader_res["query_result"]["state"]["exchange_rate"]) - 1

    print("LunaX-Luna unbond", '{:.2f}%'.format(stader_unbond_price*100))

    for p in pairs:
        response = requests.get(
            "https://lcd.terra.dev/wasm/contracts/" + pairs[p] + "/store",
            params={"query_msg": query_msg},
        ).json()
        price = int(response["result"]["return_amount"])/1000000 - 1
        price = price + stader_unbond_price if "lunax" in p else price
        print(p, '{:.2f}%'.format(price*100))

    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
