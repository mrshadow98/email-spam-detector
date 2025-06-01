# 📧 Spam Detection via Microservices with Kafka and ML

This project is an example of building a scalable **email spam detection system** using a **logistic regression ML model**, **Bloom filter**, and **Kafka-based microservices** architecture.

## 🚀 Features

- ✅ **Spam Detection with Logistic Regression**
- ✅ **Bloom Filter** to filter known spam efficiently
- ✅ **Kafka Microservices** to stream and process email events
- ✅ **Redis** for fast caching of spam indicators
- ✅ Example of integrating a **Machine Learning model** in a production-ready Kafka microservices setup

---

## 🧠 Architecture
                             +--------------------------+
                             |  gmail-integration-service |
                             +-----------+--------------+
                                         |
                                         v
                             +--------------------------+
                             |      email-processor      |
                             +-----------+--------------+
                                         |
                          +--------------+---------------+
                          |                              |
                          v                              v
        +----------------------------+     +----------------------------+
        |   spam-detector-service    |     |   bloom-filter-service     |
        +----------------------------+     +----------------------------+
                          |
                          v
             +--------------------------+
             | action-handler-service   |
             +--------------------------+

---

## 🔧 Tech Stack

- **Python** for core logic and ML
- **Logistic Regression** for spam detection
- **Bloom Filter** for fast duplicate/spam checks
- **Kafka** for inter-service communication
- **Redis** for caching
- **Docker** for containerization of all services
- **Gmail API** for real-time email fetching
- **Microservices** architecture for modularity and scalability

---

## 📌 Planned Improvements

1. ♻️ **Shared Library Architecture**  
   Move duplicate code across services into a shared library (`lib/`) to encourage reuse.

2. 📊 **Observability**  
   Integrate **OpenTelemetry** or **Sentry** for tracing, logging, and performance monitoring.

3. 🛠 **Terraform for Infra Deployment**  
   Provide Terraform scripts for deployment on cloud environments like AWS or GCP.

4. 🤖 **Auto-learning Loop**  
   Implement active learning – re-train the model when a user flags spam to improve accuracy over time.

5. 🌲 **Model Upgrade**  
   Switch to **Random Forest** or other advanced ML models for better accuracy and expand feature engineering.

---


### ✉ Flow Explanation

1. **`gmail-integration-service`**: Connects to Gmail and pushes new messages to Kafka.
2. **`email-processor`**: Reads Kafka messages and sends them to ML model + Bloom filter.
3. **`spam-detector-service`**: Applies Logistic Regression to classify messages.
4. **`bloom-filter-service`**: Checks if message pattern has been seen before.
5. **`action-handler-service`**: Takes final action (label as spam, log, etc.)

---

## 🚀 Running with Docker

Each service has its own `Dockerfile`. Use `docker-compose` to build and run the full system:

```bash
docker-compose up --build
```

## 📬 Contributing

Pull Requests are welcome!  
If you improve model accuracy, add monitoring, enhance deployment workflows, or refactor the service structure, feel free to open a PR.

---


## 📄 License

This project is licensed under the MIT License.
