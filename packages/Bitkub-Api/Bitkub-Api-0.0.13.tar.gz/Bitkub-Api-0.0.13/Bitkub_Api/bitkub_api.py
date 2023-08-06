import requests
import json
import hashlib
import hmac
import time


#  all output are json


# GET v #######################################################################################################################################################
class Bitkub:
    def __init__(self, api_key, api_secret):  # key and secret
        self.key = api_key
        self.se = api_secret

    def status(self):  # get status
        response = requests.get("https://api.bitkub.com/api/status").json()
        return response

    def servertime(self):  # get server time
        response = int(time.time())
        return response

    def symbols(self):  # get symbols
        response = requests.get("https://api.bitkub.com/api/market/symbols").json()
        return response

    def ticker(self, sym=None):  # get ticker
        if sym is None:
            response = requests.get("https://api.bitkub.com/api/market/ticker").json()
        else:
            sym = str.upper(sym)
            response = requests.get("https://api.bitkub.com/api/market/ticker?sym=" + sym).json()
        return response

    def trades(self, sym, lmt):  # get trades
        lmt = str(lmt)
        sym = str.upper(sym)
        response = requests.get("https://api.bitkub.com/api/market/trades?sym=" + sym + "&lmt=" + lmt).json()
        return response

    def bids(self, sym, lmt):  # get bids
        lmt = str(lmt)
        sym = str.upper(sym)
        response = requests.get("https://api.bitkub.com/api/market/bids?sym=" + sym + "&lmt=" + lmt).json()
        return response

    def asks(self, sym, lmt):  # get asks
        lmt = str(lmt)
        sym = str.upper(sym)
        response = requests.get("https://api.bitkub.com/api/market/asks?sym=" + sym + "&lmt=" + lmt).json()
        return response

    def books(self, sym, lmt):  # get books
        lmt = str(lmt)
        sym = str.upper(sym)
        response = requests.get("https://api.bitkub.com/api/market/books?sym=" + sym + "&lmt=" + lmt).json()
        return response

    def tradingview(self, sym, int, frm, to):  # get tradingview
        int = str(int)
        frm = str(frm)
        to = str(to)
        sym = str.upper(sym)
        response = requests.get(
            "https://api.bitkub.com/api/market/tradingview?sym=" + sym + "&int=" + int + "&frm=" + frm + "&to=" + to).json()
        return response

    def depth(self, sym, lmt):  # get depth
        lmt = str(lmt)
        sym = str.upper(sym)
        response = requests.get("https://api.bitkub.com/api/market/depth?sym=" + sym + "&lmt=" + lmt).json()
        return response

    # GET ^ #######################################################################################################################################################

    # POST encode sign v ##########################################################################################################################################
    def json_encode(self, data):
        return json.dumps(data, separators=(',', ':'), sort_keys=True)

    def sign(self, data, api_secret):
        j = self.json_encode(data)
        h = hmac.new(api_secret, msg=j.encode(), digestmod=hashlib.sha256)
        return h.hexdigest()

    def get_header(self):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self.key,
        }
        return header

    def sig_data(self, data):
        signature = self.sign(data, self.se)
        data['sig'] = signature
        return data

    # POST encode sign ^ ##########################################################################################################################################

    # POST v ######################################################################################################################################################

    def wallet(self, ts=None):  # get wallet
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/market/wallet", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def balances(self, ts=None):  # get balances
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/market/balances", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def place_bid(self, sym, amt, rat, typ, client_id=None, ts=None):  # place-bid
        sym = str.upper(sym)
        typ = str.lower(typ)
        if typ == "market":
            rat = 0
        if ts is None:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': self.servertime(),
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': self.servertime(),
                }
        else:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': ts,
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/place-bid", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def place_bid_test(self, sym, amt, rat, typ, client_id=None, ts=None):  # place-bid(test)
        sym = str.upper(sym)
        typ = str.lower(typ)
        if typ == "market":
            rat = 0
        if ts is None:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': self.servertime(),
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': self.servertime(),
                }
        else:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': ts,
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/place-bid/test", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def place_ask(self, sym, amt, rat, typ, client_id=None, ts=None):  # place-ask
        sym = str.upper(sym)
        typ = str.lower(typ)
        if typ == "market":
            rat = 0
        if ts is None:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': self.servertime(),
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': self.servertime(),
                }
        else:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': ts,
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/place-ask", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def place_ask_test(self, sym, amt, rat, typ, client_id=None, ts=None):  # place-ask(test)
        sym = str.upper(sym)
        typ = str.lower(typ)
        if typ == "market":
            rat = 0
        if ts is None:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': self.servertime(),
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': self.servertime(),
                }
        else:
            if client_id is None:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'ts': ts,
                }
            else:
                data = {
                    'sym': sym,
                    'amt': amt,
                    'rat': rat,
                    'typ': typ,
                    'client_id': client_id,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/place-ask/test", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def place_ask_by_fiat(self, sym, amt, rat, typ, ts=None):  # place-ask-by-fiat
        sym = str.upper(sym)
        typ = str.lower(typ)
        if typ == "market":
            rat = 0
        if ts is None:
            data = {
                'sym': sym,
                'amt': amt,
                'rat': rat,
                'typ': typ,
                'ts': self.servertime(),
            }
        else:
            data = {
                'sym': sym,
                'amt': amt,
                'rat': rat,
                'typ': typ,
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/market/place-ask-by-fiat", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def cancel_order(self, sym=None, id=None, sd=None, hash=None, ts=None):  # cancel order
        if ts is None:
            if hash is not None:
                data = {
                    'hash': hash,
                    'ts': self.servertime(),
                }
            else:
                sym = str.upper(sym)
                data = {
                    'sym': sym,
                    'id': id,
                    'sd': sd,
                    'ts': self.servertime(),
                }
        else:
            ts = int(ts)
            if hash is not None:
                data = {
                    'hash': hash,
                    'ts': ts,
                }
            else:
                sym = str.upper(sym)
                data = {
                    'sym': sym,
                    'id': id,
                    'sd': sd,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/cancel-order", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def my_open_orders(self, sym, ts=None):  # get your open orders
        sym = str.upper(sym)
        if ts is None:
            data = {
                'sym': sym,
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'sym': sym,
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/market/my-open-orders", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def my_order_history(self, sym, p=None, lmt=None, start=None, end=None, ts=None):  # get your order history
        sym = str.upper(sym)
        if ts is None:
            data = {
                'sym': sym,
                'ts': self.servertime(),
            }
            if p is not None:
                data['p'] = p
            if lmt is not None:
                data['lmt'] = lmt
            if start is not None:
                data['start'] = start
            if end is not None:
                data['end'] = end
        else:
            ts = int(ts)
            data = {
                'sym': sym,
                'ts': ts,
            }
            if p is not None:
                data['p'] = p
            if lmt is not None:
                data['lmt'] = lmt
            if start is not None:
                data['start'] = start
            if end is not None:
                data['end'] = end
        print(data)

        response = requests.post("https://api.bitkub.com/api/market/my-order-history", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def order_info(self, sym=None, id=None, sd=None, hash=None, ts=None):  # get order info
        if ts is None:
            if hash is not None:
                data = {
                    'hash': hash,
                    'ts': self.servertime(),
                }
            else:
                sym = str.upper(sym)
                data = {
                    'sym': sym,
                    'id': id,
                    'sd': sd,
                    'ts': self.servertime(),
                }
        else:
            ts = int(ts)
            if hash is not None:
                data = {
                    'hash': hash,
                    'ts': ts,
                }
            else:
                sym = str.upper(sym)
                data = {
                    'sym': sym,
                    'id': id,
                    'sd': sd,
                    'ts': ts,
                }

        response = requests.post("https://api.bitkub.com/api/market/order-info", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def crypto_addresses(self, p=None, lmt=None, ts=None):  # get all crypto addresses
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/crypto/addresses?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def crypto_withdraw(self, cur, amt, adr, mem=None, ts=None):  # withdraw crypto
        cur = str.upper(cur)
        if ts is None:
            data = {
                'cur': cur,
                'amt': amt,
                'adr': adr,
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'cur': cur,
                'amt': amt,
                'adr': adr,
                'ts': ts,
            }
        if mem is not None:
            data['mem'] = str(mem)

        response = requests.post("https://api.bitkub.com/api/crypto/withdraw", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def crypto_deposit_history(self, p=None, lmt=None, ts=None):  # get all crypto deposit history
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/crypto/deposit-history?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def crypto_withdraw_history(self, p=None, lmt=None, ts=None):  # get all crypto withdraw history
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/crypto/withdraw-history?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def crypto_generate_address(self, sym, ts=None):  # generate crypto address
        sym = str.upper(sym)
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/crypto/generate-address?sym=" + sym,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def fiat_accounts(self, p=None, lmt=None, ts=None):  # get all fiat accounts
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/fiat/accounts?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def fiat_withdraw(self, id, amt, ts=None):  # withdraw to bank
        if ts is None:
            data = {
                'id': id,
                'amt': amt,
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'id': id,
                'amt': amt,
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/fiat/withdraw", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def fiat_deposit_history(self, p=None, lmt=None, ts=None):  # get all deposit history
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/fiat/deposit-history?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def fiat_withdraw_history(self, p=None, lmt=None, ts=None):  # get all withdraw history
        if p is not None:
            p = str(p)
        else:
            p = ""
        if lmt is not None:
            lmt = str(lmt)
        else:
            lmt = ""
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/fiat/withdraw-history?p=" + p + "&lmt=" + lmt,
                                 headers=self.get_header(), data=self.json_encode(self.sig_data(data))).json()
        return response

    def wstoken(self, ts=None):  # get wstoken
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/market/wstoken", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def user_limits(self, ts=None):  # get user limits
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/user/limits", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response

    def user_trading_credits(self, ts=None):  # get user trading credits
        if ts is None:
            data = {
                'ts': self.servertime(),
            }
        else:
            ts = int(ts)
            data = {
                'ts': ts,
            }

        response = requests.post("https://api.bitkub.com/api/user/trading-credits", headers=self.get_header(),
                                 data=self.json_encode(self.sig_data(data))).json()
        return response


class Check:
    def __init__(self):
        self = self

    def check(self, response):
        if type(response) == int:
            return response
        codes = {
            0: 'No error',
            1: 'Invalid JSON payload',
            2: 'Missing X - BTK - APIKEY',
            3: 'Invalid API key',
            4: 'API pending for activation',
            5: 'IP not allowed',
            6: 'Missing / invalid signature',
            7: 'Missing timestamp',
            8: 'Invalid timestamp',
            9: 'Invalid user',
            10: 'Invalid parameter',
            11: 'Invalid symbol',
            12: 'Invalid amount',
            13: 'Invalid rate',
            14: 'Improper rate',
            15: 'Amount too low',
            16: 'Failed to get balance',
            17: 'Wallet is empty',
            18: 'Insufficient balance',
            19: 'Failed to insert order into db',
            20: 'Failed to deduct balance',
            21: 'Invalid order for cancellation',
            22: 'Invalid side',
            23: 'Failed to update order status',
            24: 'Invalid order for lookup',
            25: 'KYC level 1 is required to proceed',
            30: 'Limit exceeds',
            40: 'Pending withdrawal exists',
            41: 'Invalid currency for withdrawal',
            42: 'Address is not in whitelist',
            43: 'Failed to deduct crypto',
            44: 'Failed to create withdrawal record',
            45: 'Nonce has to be numeric',
            46: 'Invalid nonce',
            47: 'Withdrawal limit exceeds',
            48: 'Invalid bank account',
            49: 'Bank limit exceeds',
            50: 'Pending withdrawal exists',
            51: 'Withdrawal is under maintenance',
            90: 'Server error (please contact support)',
        }
        if response.keys().__contains__('error'):
            code = response['error']
        else:
            return response
        if codes.keys().__contains__(code):
            response["code description"] = codes[code]
        return response

