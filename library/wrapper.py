from library import fund_analysis
import logging
import traceback
import sys

# =============================================================
# CONFIGURE LOGGER
# =============================================================
# set format
ft = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(format=ft)

# creates a logger
logger = logging.getLogger(__name__)
logger.setLevel(level=10)


def get_fund_returns(fund=None, start_date=None, end_date=None):
    logger.info("get_fund_returns : start")

    out = dict()
    out["data"] = None
    out["code"] = 0
    out["error"] = list()

    try:
        out["data"] = fund_analysis.get_fund_returns(fund=fund)
    except Exception as err:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_traceback)

        out["code"] += 1
        out["error"] = [''.join(tb.format_exception_only())]

    logger.info("get_fund_returns : end")
    return out