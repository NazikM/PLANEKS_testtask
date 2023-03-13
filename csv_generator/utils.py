import pandas as pd
from random import randint
from faker import Faker

range_types = ['int', 'text']


def check_range(col_range):
    if all(col_range) and len(col_range) == 2:
        return tuple(map(int, col_range))
    raise ValueError


def generate_value(n, col_type, col_range, fake):
    if col_type in range_types:
        col_range = check_range(col_range)
    if col_type == "name":
        return [fake.name() for _ in range(n)]
    elif col_type == "job":
        return [fake.job() for _ in range(n)]
    elif col_type == "email":
        return [fake.email() for _ in range(n)]
    elif col_type == "domain":
        return [fake.domain_name() for _ in range(n)]
    elif col_type == "phone":
        return [fake.phone_number() for _ in range(n)]
    elif col_type == "company":
        return [fake.company() for _ in range(n)]
    elif col_type == "text":
        return [fake.sentences(randint(*col_range)) for _ in range(n)]
    elif col_type == "int":
        return [randint(*col_range) for _ in range(n)]
    elif col_type == "address":
        return [fake.address() for _ in range(n)]
    elif col_type == "date":
        return [fake.date() for _ in range(n)]
    raise NotImplemented


def generate_csv(schema, post_args):
    # Check post_args and schema
    fake = Faker()
    csv_data = {}
    columns = sorted(schema.columns, key=lambda c: c['order'])
    for column in columns:
        csv_data[column['name']] = generate_value(int(post_args['rows']), column['type'], column.get('range'), fake)
    df = pd.DataFrame(csv_data)
    return df.to_csv(sep=schema.separator, quotechar=schema.string_char)
