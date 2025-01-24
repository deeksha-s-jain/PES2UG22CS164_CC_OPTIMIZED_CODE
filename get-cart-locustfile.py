from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCartUser(FastHttpUser):
    # Define the base host URL
    host = "http://localhost:5000"
    
    # Define reusable headers
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        
        # Update headers with the token
        self.default_headers.update({
            "Authorization": f"Bearer {self.token}"
        })

    @task
    def view_cart(self):
        """
        Task to simulate viewing the cart
        """
        # Make the GET request to the `/cart` endpoint
        with self.client.get(
            "/cart",
            headers=self.default_headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to load cart: {response.status_code}")

if __name__ == "__main__":
    run_single_user(AddToCartUser)
