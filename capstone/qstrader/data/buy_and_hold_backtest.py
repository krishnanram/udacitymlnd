import click
from common import settings
from common.compat import queue
from portfolio.portfolio_handler import PortfolioHandler
from price_handler.price_parser import PriceParser
from qstrader.position_sizer.fixed import FixedPositionSizer
from smarttrader.strategy import Strategies, DisplayStrategy
from smarttrader.strategy.buy_and_hold import BuyAndHoldStrategy
from smarttrader.compliance import ExampleCompliance
from smarttrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
from smarttrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from smarttrader.risk_manager.example import ExampleRiskManager
from smarttrader.simulator.backtest import Backtest
from smarttrader.statistics import SimpleStatistics


def run(config, testing, tickers, filename):

    # Set up variables needed for backtest
    events_queue = queue.Queue()
    csv_dir = "./"
    initial_equity = PriceParser.parse(500000.00)

    # Use Yahoo Daily Price Handler
    price_handler = YahooDailyCsvBarPriceHandler(
        csv_dir, events_queue, tickers
    )

    # Use the Buy and Hold Strategy
    strategy = BuyAndHoldStrategy(tickers, events_queue)
    strategy = Strategies(strategy, DisplayStrategy())

    # Use an example Position Sizer
    position_sizer = FixedPositionSizer()

    # Use an example Risk Manager
    risk_manager = ExampleRiskManager()

    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler(
        initial_equity, events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the ExampleCompliance component
    compliance = ExampleCompliance(config)

    # Use a simulated IB Execution Handler
    execution_handler = IBSimulatedExecutionHandler(
        events_queue, price_handler, compliance
    )

    # Use the default Statistics
    statistics = SimpleStatistics(config, portfolio_handler)

    # Set up the backtest
    backtest = Backtest(
        price_handler, strategy,
        portfolio_handler, execution_handler,
        position_sizer, risk_manager,
        statistics, initial_equity
    )
    results = backtest.simulate_trading(testing=testing)
    statistics.save(filename)
    return results


@click.command()
@click.option('--config', default=settings.DEFAULT_CONFIG_FILENAME, help='Config filename')
@click.option('--testing/--no-testing', default=False, help='Enable testing mode')
@click.option('--tickers', default='SP500TR', help='Tickers (use comma)')
@click.option('--filename', default='', help='Pickle (.pkl) statistics filename')
def main(config, testing, tickers, filename):
    print config

    tickers = tickers.split(",")
    config = settings.from_file(config, testing)
    run(config, testing, tickers, filename)


if __name__ == "__main__":
    main()
