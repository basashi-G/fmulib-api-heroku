import pandas
import datetime
import logging
from urllib.error import HTTPError

logger = logging.getLogger("logger").getChild(__name__)


class Calender:
    open_time: dict

    def __init__(self) -> None:
        self.open_time = {}
        self.fetch_from_network()

    def fetch_from_network(self) -> None:
        def relese_nest(li: list) -> list:
            result = []
            for i in li:
                result += i
            return result

        result = {}
        now: datetime = datetime.date.today()

        url = (
            "https://www-lib.fmu.ac.jp/lib/calendar/"
            + str(now.strftime("%Y%m"))
            + ".html"
        )

        logger.info("Get calender data from fmu lib web page.")

        # 開館時間をデータフレームから辞書型に変換
        try:
            dfs = pandas.read_html(url)
            data = dfs[1][:-1]
            data_notnan = data.fillna(0)
            li = relese_nest(data_notnan.values.tolist())

            for i in li:
                if i != 0:
                    day_list = i.split()
                    day = int(day_list[0])
                    date = datetime.date(year=now.year, month=now.month, day=day)
                    times = day_list[1:]
                    close_removed_times = [i for i in times if i != "Closed"]
                    if not close_removed_times:
                        time = None
                    else:
                        time = {
                            "start": close_removed_times[0].split("-")[0],
                            "end": close_removed_times[-1].split("-")[1],
                        }
                    result[date] = time
            self.open_time = result

        except ValueError:
            logger.exception("Cannot get date from nerwork")
        except HTTPError:
            logger.exception("page is not publish yet.")

    def check(self, date: datetime.datetime) -> tuple:
        try:
            return ("OK", self.open_time[date])
        except KeyError:
            return ("NG", None)


if __name__ == "__main__":
    cal = Calender()
    print(cal.check(datetime.date.today()))
