import requests
import datetime
from requests.exceptions import HTTPError

DEFAULT_TWSTOCKS_URL = 'http://appworks.octave.vip'


class TWStocks():
    def __init__(self, secret_key, twstocks_url=DEFAULT_TWSTOCKS_URL, session=None, timeout=60):
        self.secret_key = secret_key
        self.timeout = timeout
        self.twstocks_url = twstocks_url.rstrip('/')
        self.session = session or requests.session()
        self.session.headers['Accept'] = 'application/json'

    def _convert_date(self, date_string):
        try:
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"time data '{date_string}' does not match format '%Y-%m-%d'")

    def _api_request(self, method, path, cmkey, date=None, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        url = self.twstocks_url + path
        if method == 'POST':
            if date is not None:
                self._convert_date(date)
            headers = kwargs.get('headers', {})
            headers['Content-Type'] = 'application/json'

            kwargs['json'] = {
                'secret_key': self.secret_key,
                'cmkey': cmkey,
                'start_date': date,
            }
            kwargs['headers'] = headers

        r = self.session.request(method, url, **kwargs)
        http_error_msg = ''

        if 400 <= r.status_code < 600:
            reason = r.reason
            try:
                reason = r.json()['message']
            except Exception:
                pass
            http_error_msg = 'HTTPError: %s %s' % (r.status_code, reason)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=r)

        return r

    def get_cash_flow_statement(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_cash_flow_statement'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_balance_sheet(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_balance_sheet'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_financial_ratios(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_financial_ratios'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_income_statement(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_income_statement'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_k_image(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_k_image'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_per_and_pbr(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_per_and_pbr'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_reinvestment(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_reinvestment'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_stock_basic_info(self, cmkey):
        api_endpoint = '/stocks/get_cmoney_stock_basic_info'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey)
        return r.json()

    def get_stock_name(self, cmkey):
        api_endpoint = '/stocks/get_cmoney_stock_info'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey)
        return r.json()

    def get_stock_revenue_surplus(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_stock_revenue_surplus'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()

    def get_trader_sum(self, cmkey, date):
        api_endpoint = '/stocks/get_cmoney_trader_sum'
        r = self._api_request('POST', api_endpoint, cmkey=cmkey, date=date)
        return r.json()
