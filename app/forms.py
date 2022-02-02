from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    HiddenField,
    BooleanField,
    DateField,
)
from wtforms.validators import InputRequired, NumberRange, Regexp
from flask_wtf import FlaskForm


# Date format in YYYY-MM-DD
dateregex = "^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$"
letterregex = "^[a-zA-Z]+$"
numberregex = "^[0-9]+$"


class DailyForm(FlaskForm):
    id_field = HiddenField()
    date = DateField(id="datepick", format="%Y-%m-%d")
    stocks_above_20ma = IntegerField(
        "Stocks above 20ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    stocks_above_50ma = IntegerField(
        "Stocks above 50ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    stocks_above_200ma = IntegerField(
        "Stocks above 200ma (%)",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=100, message="Invalid number"),
        ],
    )
    submit = SubmitField("Submit")


class WeeklyForm(FlaskForm):
    date = DateField(id="datepick", format="%Y-%m-%d")
    industry_groups = StringField("Record notable changes of industry groups")
    scans = BooleanField("Review weekly scans")
    watchlist = BooleanField("Review Watchlist")
    focuslist = BooleanField("Create Focuslist")
    open_positions = BooleanField("Open positions")
    submit = SubmitField("Submit")


class TradeForm(FlaskForm):
    date = DateField(id="datepick", format="%Y-%m-%d")
    symbol = StringField(
        "Symbol",
        validators=[
            InputRequired(),
            Regexp(letterregex, message="Invalid symbol format"),
        ],
    )
    position_size = IntegerField("Position Size ($)")
    net_pnl = IntegerField("Net P&L ($)")
    net_roi = IntegerField("Net ROI (%)")
    notes = StringField("Notes")
    submit = SubmitField("Submit")