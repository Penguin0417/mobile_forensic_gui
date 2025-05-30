# utils/data_parser.py
def get_mock_data(data_type):
    return [
        {"time": "2023-11-01 12:00", "content": "Test Message", "source": data_type},
        {"time": "2023-11-01 12:01", "content": "Another Test", "source": data_type}
    ]
