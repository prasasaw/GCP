from google.cloud import pubsub_v1

# Set the topic name
topic_name = "orders"

# Create a Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()

# Create the message to be published
message = "Hello, Sweden!".encode("utf-8")

# Publish the message to the topic
topic_path = publisher.topic_path("prasad-gcp4-project", topic_name)
future = publisher.publish(topic_path, data=message)

# Wait for the message to be published
result = future.result()

print(f"Message published: {result}")
