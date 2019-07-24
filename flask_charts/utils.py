import datetime

def prep_data(data):
    for row in data['rows']:
        for val in row['c']:
            if isinstance(val['v'], datetime.datetime):
                val['v'] = "Date({}, {}, {}, {}, {}, {}, {})".format(
                                                    val['v'].year,
                                                    val['v'].month-1,
                                                    val['v'].day,
                                                    val['v'].hour,
                                                    val['v'].minute,
                                                    val['v'].second,
                                                    val['v'].microsecond)
            elif isinstance(val['v'], datetime.date):
                val['v'] = "Date({}, {}, {})".format(val['v'].year,
                                                     val['v'].month-1,
                                                     val['v'].day)
    return data


def render_data(columns, rows):
    data = {'cols': [], 'rows': []}

    for column in columns:
        data['cols'].append({"id": "", "label": column[1], "pattern": "", "type": column[0]})

    for row in rows:
        new_row = {'c': []}
        for field in row:
            new_row['c'].append({"v": field, "f": None})
        data['rows'].append(new_row)
    return prep_data(data)