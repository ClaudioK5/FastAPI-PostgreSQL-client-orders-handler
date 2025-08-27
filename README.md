This Python Pipeline automates the process of **storing Customers data and Customers order data** using **FastAPI**. It stores data in a **PostsgreSQL** database and provides real-time data overview through a set of **RESTful API endpoints**. 
It is integrated with **generative AI** (more specifically **DeepSeek**) to create analytical report based on current month's orders. The analysis is then forwarded to a desired email address.

**Endpoints**
- POST /customers : creates a new customer.
- POST /orders: creates a new order for an already existing customer.
- GET /customers: gives an overview of the existing customers in the database.
- GET /orders: gives an overview of the existing orders in the database.
- GET /generate_report: creates an AI report for the orders in the current month which is then retrieved to your email.

The pipeline is scalable and newer features will be added.
