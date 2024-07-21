from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np
import lorem
from faker import Faker
import json


N = 10000
history_days = 10
faker = Faker()

ids = np.random.choice(np.arange(1, 1000000), size=N, replace=False, p=None)

def generate_random_date_in_past():
    seconds = random.randint(0, history_days * 86400)
    ms = random.randint(0, 5000)
    created_at = datetime.now() - timedelta(seconds=seconds)
    updated_at = created_at + timedelta(milliseconds=ms)
    return created_at, updated_at


def generate_fake_input_json():
    return json.dumps({
        'id': faker.uuid4(),
        'name': faker.name(),
        'uuid': faker.uuid4(),
        'message': faker.text(),
        'message_id': faker.uuid4(),
        'publication_id': faker.uuid4(),
        'documentum_id': faker.uuid4(),
        'status': status,
    })

data = []
for i, id in enumerate(ids):
    documentum_id = faker.uuid4()
    publication_id = faker.uuid4()
    status = random.choice(['NEW', 'ERROR', 'DONE', 'TO_UPLOAD', 'NOT_CANDIDATE'])
    status_message = lorem.sentence() if status == 'ERROR' else ''
    created_at, updated_at = generate_random_date_in_past()
    fake_input_json = generate_fake_input_json()
    data.append([id, publication_id, documentum_id, status, status_message, created_at, updated_at, fake_input_json])

pd.DataFrame(data, columns=['message_id', 'publication_id', 'documentum_id', 'status', 'status_message', 'created_at', 'updated_at', 'message']).to_pickle("data.pkl")