# TWStocks Python SDK
TWStocks HTTP API SDK

## Installation
```
$ pip install tw_stocks
```

## How to use?
```
from tw_stocks import TWStocks
tw_stocks = TWStocks('API secret key')
tw_stocks.get_cash_flow_statement('1101', '2021-01-01')
```
Output:
```
[{'CMKey': '1101',
  'CashAndCashEquivalents': '62025098',
  'CashFlowFromFinancingActivities': '-1790927',
  'CashFlowFromInvestingActivities': '5292661',
  'CashFlowFromOperatingActivities': '7124458',
  'DateRange': '202101',
  'EarningsBeforeTaxes': '4846931',
  'FreeCashFlow': '2232457',
  'NetCashFlow': '10591576'}]
```

