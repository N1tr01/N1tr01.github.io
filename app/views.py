from crypt import methods
from turtle import position
from . import app, db
from .tools import allowed_file
from .models import WeeklyRoutine, DailyRoutine, Trade
from .forms import DailyForm, WeeklyForm, TradeForm
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from csv import reader
from datetime import datetime
from sqlalchemy import desc

dateformat = "%Y-%m-%d"


@app.route("/")
def index():
    """
    Return the homepaege.
    """
    trades = Trade.query.all()
    latesttrades = Trade.query.order_by(desc(Trade.date)).limit(10).all()

    latest_labels = [trade.date.strftime(dateformat) for trade in latesttrades]
    latest_values = [trade.net_roi for trade in latesttrades]

    roidata = [trade.net_roi for trade in trades]
    wins = len([win for win in roidata if win > 0])
    loses = len(roidata) - wins
    winloss_labels = ["win", "loss"]
    winloss_values = [wins, loses]

    return render_template(
        "index.html",
        title="Trading Journal",
        winloss_labels=winloss_labels,
        winloss_values=winloss_values,
        latest_labels=latest_labels,
        latest_values=latest_values,
    )


@app.route("/add_dailyroutine", methods=["GET", "POST"])
def add_dailyroutine():
    """
    Return exisiting and add new daily routine entries.
    """

    form = DailyForm()

    if form.validate_on_submit():

        record = DailyRoutine(
            date=datetime.strptime(form.date.data, dateformat),
            stocks_above_20ma=form.stocks_above_20ma.data,
            stocks_above_50ma=form.stocks_above_50ma.data,
            stocks_above_200ma=form.stocks_above_200ma.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_dailyroutine.html", message=message, form=form)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_dailyroutine.html", form=form, title="Daily Routine")


@app.route("/add_dailyroutine/data")
def daily_data():
    """
    Return daily routine table data.
    """
    return {
        "data": [dailyroutine.to_dict() for dailyroutine in DailyRoutine.query.all()]
    }


@app.route("/add_weeklyroutine", methods=["GET", "POST"])
def add_weeklyroutine():
    """
    Return exisiting and add new weekly routine entries.
    """

    form = WeeklyForm()

    if form.validate_on_submit():

        record = WeeklyRoutine(
            date=datetime.strptime(form.date.data, dateformat),
            industry_groups=form.industry_groups.data,
            scans=form.scans.data,
            watchlist=form.watchlist.data,
            focuslist=form.focuslist.data,
            open_positions=form.open_positions.data,
        )

        db.session.add(record)
        db.session.commit()

        message = f"The data for {record.date} has been submitted."

        return render_template("add_weeklyroutine.html", message=message, form=form)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_weeklyroutine.html", form=form, title="Weekly Routine")


@app.route("/add_weeklyroutine/data")
def weekly_data():
    """
    Return weekly routine table data.
    """
    return {
        "data": [weeklyroutine.to_dict() for weeklyroutine in WeeklyRoutine.query.all()]
    }


@app.route("/add_trade", methods=["GET", "POST"])
def add_trade():
    """
    Return exisiting and add new trades.
    """

    form = TradeForm()

    if form.validate_on_submit():

        date = datetime.strptime(form.date.data, dateformat)
        symbol = form.symbol.data.upper()
        num_shares = form.num_shares.data
        buy_price = form.buy_price.data
        sell_price = form.sell_price.data
        position_size = round(num_shares * buy_price, 2)
        if sell_price == 0:
            net_pnl = 0
            net_roi = 0
        else:
            net_pnl = round((num_shares * sell_price) - position_size, 2)
            net_roi = round(net_pnl / position_size * 100, 2)

        record = Trade(
            date=date,
            symbol=symbol,
            num_shares=num_shares,
            buy_price=buy_price,
            sell_price=sell_price,
            position_size=position_size,
            net_pnl=net_pnl,
            net_roi=net_roi,
            notes=form.notes.data,
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("add_trade"))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    "Error in {}: {}".format(getattr(form, field).label.text, error),
                    "error",
                )

    return render_template("add_trade.html", form=form, title="Trades")


@app.route("/update_trade", methods=["GET", "POST"])
def update_trade():
    """
    Update an exiting trade in the database.
    """

    return "404"


@app.route("/trades/data")
def trade_data():
    """
    Return trade table data.
    """

    return {"data": [trade.to_dict() for trade in Trade.query.all()]}


@app.errorhandler(404)
def handle_404(e):
    """
    Return a 404 error page.
    """
    return "404", 404


@app.errorhandler(500)
def handle_500(e):
    """
    Return a 500 error page.
    """
    return "500", 500
