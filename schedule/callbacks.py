from dash.dependencies import Input, Output, State
import dash.html as html
import dash_bootstrap_components as dbc
from datetime import datetime

from data_loader import load_schedule_data, get_day_info

def register_schedule_callbacks(app):
    
    schedule_data = load_schedule_data()

    @app.callback(
        [Output("schedule-table", "children"),
         Output("schedule-title", "children")],
        [Input("group-filter", "value"),
         Input("date-picker", "date")]
    )
    def update_schedule(selected_group, selected_date):
        
        day_of_week, week_parity = get_day_info(selected_date)

        if not day_of_week:
            return html.P("Пожалуйста, выберите дату."), "Расписание"

        schedule_list = schedule_data.get('schedule', [])
        
        todays_schedule = []
        for pair in schedule_list:
            if pair['day_of_week'] == day_of_week:
                if pair['week_parity'] == 'always' or pair['week_parity'] == week_parity:
                    todays_schedule.append(pair)
        
        date_formatted = datetime.strptime(selected_date.split('T')[0], '%Y-%m-%d').strftime('%d.%m.%Y')
        title = f"Расписание на {date_formatted} ({day_of_week.capitalize()})"

        if not todays_schedule:
            cards = html.Div(
                f"Занятий нет.", 
                className="text-success text-center p-4"
            )
            return cards, title

        todays_schedule.sort(key=lambda x: x['pair_number'])

        cards = []
        for pair in todays_schedule:
            cards.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H5(f"{pair['pair_number']}. {pair['subject']}", className="card-title"),
                        html.H6(f"{pair['time_start']} - {pair['time_end']}", className="card-subtitle mb-2 text-muted"),
                        html.P(f"Тип: {pair['class_type']}", className="card-text"),
                        html.P(f"Преподаватель: {pair.get('lecturer', 'Не указан')}", className="card-text"),
                        html.P(f"Аудитория: {pair.get('classroom', 'Не указана')}", className="card-text"),
                    ]),
                    className="mb-3"
                )
            )
        
        return cards, title