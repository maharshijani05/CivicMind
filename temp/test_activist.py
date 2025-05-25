from activist import get_activist_response

policy = "The government will implement a ₹100 congestion tax for entering the city center on weekdays."

response = get_activist_response(policy)
print("ActivistBot says:\n", response)
