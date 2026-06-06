import httpx


class ZohoClient:

    def __init__(self, access_token: str, portal_id: str):
        self.access_token = access_token
        self.portal_id = portal_id
        self.base_url = "https://projectsapi.zoho.in/restapi"

    @property
    def headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"
            
        }
    async def get_projects(self):

        url = f"{self.base_url}/portal/{self.portal_id}/projects/"
        
        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=self.headers
            )

        return response.json()
    
        
    async def get_tasks(self, project_id: str):

        url = (
            f"{self.base_url}/portal/"
            f"{self.portal_id}/projects/"
            f"{project_id}/tasks/"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=self.headers
            )

        return {
            "status_code": response.status_code,
            "response": response.json()
        }
    async def create_task(
        self,
        project_id: str,
        task_name: str,
    ):
        endpoint = f"/portal/{self.portal_id}/projects/{project_id}/tasks/"

        payload = {
            "name": task_name
        }
    async def update_task_status(
        self,
        project_id: str,
        task_id: str,
        status: str,
    ):

        url = (
            f"https://projects.zoho.in/api/v3/"
            f"portal/{self.portal_id}/projects/"
            f"{project_id}/tasks/bulk-update"
        )

        payload = {
            "taskids": task_id,
            "status": {
                "id": status
            },
            "ignore_bug_association": "no",
            "isdetailspageopen": True,
            "pagefor": "project"
        }

        print("PATCH URL:", url)
        print("PATCH PAYLOAD:", payload)

        async with httpx.AsyncClient() as client:

            response = await client.patch(
                url,
                headers=self.headers,
                json=payload,
            )

        print("STATUS UPDATE RESPONSE")
        print(response.status_code)
        print(response.text)

        response.raise_for_status()

        return response.json()
    async def create_task(
        self,
        project_id: str,
        task_name: str,
    ):
        endpoint = f"/portal/{self.portal_id}/projects/{project_id}/tasks/"

        payload = {
            "name": task_name
        }
        
        return await self.post(
            endpoint,
            data=payload,
        )
    async def create_project(
        self,
        project_name: str,
    ):
        endpoint = f"/portal/{self.portal_id}/projects/"

        payload = {
            "name": project_name
        }

        return await self.post(
            endpoint,
            data=payload,
        )
    async def post(
        self,
        endpoint: str,
        data: dict | None = None,
    ):
        import httpx

        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                headers=self.headers,
                data=data
            )

        print("POST URL:", url)
        print("POST PAYLOAD:", data)
        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        return response.json()