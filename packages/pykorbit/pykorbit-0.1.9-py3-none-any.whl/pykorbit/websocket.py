import websockets
import asyncio
import datetime
import json
import multiprocessing as mp


class WebSocketManager(mp.Process):
    """웹소켓을 관리하는 클래스

        사용 예제:

            >> wm = WebSocketManager("ticker", ["BTC_KRW"])
            >> for i in range(3):
                data = wm.get()
                print(data)
            >> wm.terminate()

        주의 :

           재귀적인 호출을 위해 다음의 guard를 반드시 추가해야 한다.
           >> if __name__ == "__main__"

    """
    def __init__(self, type: list, symbols: list, ticktype: list=None, qsize: int=1000):
        """웹소켓을 컨트롤하는 클래스의 생성자

        Args:
            type     (list          ): 구독 메시지 종류 (ticker/transaction/orderbook)
            symbols  (list          ): 구독할 암호 화폐의 리스트 [btc_krw, eth_krw, …]
            qsize    (int , optional): 메시지를 저장할 Queue의 크기
        """
        self.__q = mp.Queue(qsize)
        self.alive = False



        self.type = type
        self.symbols = symbols

        super().__init__()

    async def __connect_socket(self):
        uri = "wss://ws.korbit.co.kr/v1/user/push"

        async with websockets.connect(uri, ping_interval=None) as websocket:
            now = datetime.datetime.now()
            timestamp = int(now.timestamp() * 1000)

            req_msg = [f"{x}:{','.join(self.symbols)}" for x in self.type]
            print(req_msg)
            subscribe_fmt = {
                "accessToken": None,
                "timestamp": timestamp,
                "event": "korbit:subscribe",
                "data": {
                    "channels": req_msg
                }
            }
            subscribe_data = json.dumps(subscribe_fmt)
            await websocket.send(subscribe_data)

            recv_data = await websocket.recv()
            recv_data = json.loads(recv_data)
            assert(recv_data['event'] == 'korbit:connected')

            recv_data = await websocket.recv()
            recv_data = json.loads(recv_data)
            assert(recv_data['event'] == 'korbit:subscribe')

            while self.alive:
                recv_data = await websocket.recv()
                self.__q.put(json.loads(recv_data))

    def run(self):
        self.__aloop = asyncio.get_event_loop()
        self.__aloop.run_until_complete(self.__connect_socket())

    def get(self):
        if self.alive == False:
            self.alive = True
            self.start()
        return self.__q.get()

    def terminate(self):
        self.alive = False

        super().terminate()

if __name__ == "__main__":
    wm = WebSocketManager(['transaction', 'ticker'], ['xrp_krw'])
    for i in range(10):
        data = wm.get()
        print(data)
    wm.terminate()
