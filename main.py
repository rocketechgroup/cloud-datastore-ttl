import pendulum
import hashlib

from google.cloud import datastore


def prepend_sha2(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    return m.hexdigest() + '_' + str(value)


def add_customer(customer_id):
    customer_id = str(customer_id)
    customer_id_with_hash = prepend_sha2(customer_id)
    with client.transaction():
        customer_key = client.key("Customer", customer_id_with_hash, namespace="customer_app")
        task = datastore.Entity(key=customer_key)
        task.update(
            {
                "first_name": "Dummy " + customer_id,
                "last_name": "Dummy " + customer_id
            }
        )

        client.put(task)


def add_transaction(customer_id, transaction_id, expiry_minutes):
    transaction_id = str(transaction_id)
    time_now = pendulum.now()
    expiry_timestamp = time_now.add(minutes=expiry_minutes)
    transaction_id_with_hash = prepend_sha2(transaction_id)
    key_with_parent = client.key(
        "Customer", prepend_sha2(customer_id), "Transaction", transaction_id_with_hash,
        namespace="customer_app"
    )

    task = datastore.Entity(key=key_with_parent, exclude_from_indexes=['expiry_timestamp'])

    task.update(
        {
            "transaction_type": "Personal",
            "amount": 25.00,
            "expiry_timestamp": expiry_timestamp
        }
    )

    client.put(task)


if __name__ == '__main__':
    client = datastore.Client()

    # parent - customer record
    add_customer(customer_id=12345)
    add_customer(customer_id=12346)

    # child, customer transactions
    for i in range(10):
        add_transaction(customer_id=12345, transaction_id=i, expiry_minutes=1)
        add_transaction(customer_id=12346, transaction_id=i, expiry_minutes=5)
