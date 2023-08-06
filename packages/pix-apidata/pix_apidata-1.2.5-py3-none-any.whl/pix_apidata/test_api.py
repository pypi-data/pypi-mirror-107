import asyncio
import apidata_lib
import apidata_models
import time
#from pix_apidata import apidata_lib,apidata_models

api = apidata_lib.ApiData()

event_loop = asyncio.get_event_loop()


async def main():
    api.on_connection_started(connection_started)
    api.on_connection_stopped(connection_stopped)
    api.on_trade_update(on_trade)
    api.on_best_update(on_best)
    api.on_refs_update(on_refs)
    api.on_srefs_update(on_srefs)
    
    key = "l+phpXGgBZx/g3t+F0ZpW6xNJEA="
    host = "apidata.accelpix.in"
    #key="OMLW74kiRTZeuBIWiJ4gXKZPsPk="
    #host ="192.168.56.101"
    # host = "localhost:5011"
    s = await api.initialize(key, host)
    print(s)
    
    #history data
    his1 = await api.get_eod('TCS', '20200828', '20200901')
    print("History : ",his1)
    #end

    #Live data
    syms = ["TCS",'NIFTY-1']
    await api.subscribeAll(syms)
    time.sleep(1)
    await api.unsubscribeAll(['TCS'])
    print("=====Unsubscribe Done=====")
    

def connection_started():
    print("Connection started callback")


def connection_stopped():
    print("Connection stopped callback")

def on_trade(msg):
    t = apidata_models.Trade(msg)
    print("Trade :",t.ticker)#trade

def on_best(msg):
    b = apidata_models.Best(msg)
    print("best :",msg)#best

def on_refs(msg):
    ref = apidata_models.Refs(msg)
    print("refs",msg)#refs

def on_srefs(msg):
    sref = apidata_models.RefsSnapshot(msg)
    print("sref:",msg)
#end

event_loop.create_task(main())
event_loop.run_forever()
