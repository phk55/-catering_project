from ..common_func.forms import BaseForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class AddScoreForm(BaseForm):
    score1 = StringField(validators=[InputRequired(message='尊敬的顾客，您好，请确认色/香/味 三项均已评分！')])
    score2 = StringField(validators=[InputRequired(message='尊敬的顾客，您好，请确认色/香/味 三项均已评分！')])
    score3 = StringField(validators=[InputRequired(message='尊敬的顾客，您好，请确认色/香/味 三项均已评分！')])
    suggest = StringField(validators=[])
    cur_url = StringField(validators=[])
