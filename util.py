def get_email_name(email):
    return email.split('@')[0]


def parse_semester(semester):
    """Converts a semester string into a sortable format."""
    year, term = semester.lower().split(' ')
    term_order = {'fall': 1, 'spring': 2, 'summer': 3}
    return int(year), term_order[term]

def sort_data(data):
    """Sorts the data by semester."""
    return sorted(data, key=lambda x: parse_semester(x['semester']), reverse=True)

def get_most_recent_track(data):
    """Finds the most recent track from the sorted data."""
    sorted_data = sort_data(data)
    for record in sorted_data:
        if record['track'] is not None:
            return record['track']
    return None