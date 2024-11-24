from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # @task
    # def index(self):
    #     self.client.get("/tasks/create") 

    # @task(3) 
    # def login(self):
    #     self.client.post("/accounts/login/", {"username": "togzhan", "password": "toha2004"}) 

    @task(2) 
    def get_datasets(self):
        status = "pending" 
        self.client.get(f"/products/datasets/{status}/")
