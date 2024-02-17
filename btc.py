import datetime
import bit
import config
import pydantic_models
wallet = bit.Key() # наш кошелек готов и содержится в переменной
wallet
print(f"Баланс: {wallet.get_balance()}")
print(f"Адрес: {wallet.address}")
print(f"Приватный ключ: {wallet.to_wif()}")
print(wallet.get_transactions())