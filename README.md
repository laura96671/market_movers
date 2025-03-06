## Market Movers Screener

### Overview
The project is born from the need of having a market screener able to retrieve the market main movers of the day/
Targeting the most volatile stocks, the idea is to receive a notification on Telegram each and every time a pct change 
reaches a certain value

### Description
The main steps are the following:
- On a schedule, the pipeline will be triggered and market data from yFinance screener will be retrieved
- All retrieved stocks will be listed and and news will be retrieved for all of them
- Data are filtered and saved in a dedicated folder in order to be analyzed afterwards #TODO
- A notification will be sent as soon as a certain pct is reached #TODO

### Usage
```commandline
python main.py
```