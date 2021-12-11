from sqlalchemy.orm import sessionmaker
import unittest

from base64 import b64encode
from app import app
import json
from models import User, Medicament, Purchase
from app import engine
from user import bcrypt

Session = sessionmaker(bind=engine)

class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    session = Session()

    def tearDown(self):
        self.close_session()

    def close_session(self):
        self.session.close()

class ApiTest(TestingBase):
    user = {
        "name": "SoniaPlaystatio",
        "login": "Baran@gmail.com",
        "password": "12345678",
        "role": "user"
    }

    playlist = {
        "user_id": 1,
        "product_id": 1,
        "number": 4
    }

    medicament = {
        "name": "Cytramon",
        "price": 5,
        "number": 10
    }

    def test_User_Creation(self):
        response = self.tester.post("/users/", data=json.dumps(self.user),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(User).filter_by(name='SoniaPlaystatio').delete()
        self.session.commit()

    def test_User_Creation_invalid(self):
        response = self.tester.post("/users/", data=json.dumps({
        "name": "SoniaPlaystatio",
        "login": "bara@gmail.com",
        "password": "1234",
        "role": "user"
    }), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_Get_User_By_id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(id=123, name="SoniaPlaystatio", login="bara@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        #creds = b64encode (b"SoniaPlaxstation:12345678-).decode(tutt-8-)
        response = self.tester.get('/users')
        code = response.status_code
        self.assertEqual(200, code)

    def test_Update_User(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystation", login="baranya@gmail.com",  password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"cucumber@gmail.com:12345678").decode("utf-8")
        response = self.tester.put('/users/1',
                                   data=json.dumps({"nickname": "Sonya", "login": "baranyyy@gmail.com",
                                                    "password": "12345678", "role": "user"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(User).filter_by(name='Sonya').delete()
        self.session.commit()

    def test_Update_User_invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystation", login="baranya@gmail.com",  password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"SoniaPlaystation:12345678").decode("utf-8")
        response = self.tester.put('/users/1',
                                   data=json.dumps({"nickname": "Sonya", "login": "baranyyy@gmail.com",
                                                    "password": "12345678", "role": "user"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(User).filter_by(name='SoniaPlaystation').delete()
        self.session.commit()

    def test_Delete_User_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystatio", login="bara@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        #creds = b64encode(b"SoniaPlaystati:12345678").decode("utf-8")
        response = self.tester.delete('/users/124')
        code = response.status_code
        self.assertEqual(401, code)

    def test_Login_User(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="baran@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"name": "rassel", "password": "12345678"}), content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(401, code)

    def test_Login_User_invalid1(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"nickname": "rasssel", "password": "12345678"}), content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(401, code)

    def test_Login_User_invalid2(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"nickname": "rassel", "password": "5678"}), content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(401, code)

    def test_Create_Medicament(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/drug/", data=json.dumps(self.medicament),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(Medicament).filter_by(name='Cytramon').delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()

    def test_Create_Medicament_Invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/drug/", data=json.dumps(self.medicament),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(Medicament).filter_by(name='Cytramon').delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()

    def test_Get_Medicament_By_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Medicament(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.get('/drug/1', headers={"Authorization": f"Basic {creds}"})
        self.session.delete(drug)
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(200, code)
        self.assertEqual({"user": {"id": 1, "name": "aspiryn", "price": 10, "number": 5}}, response.json)

    def test_Delete_Medicament_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Medicament(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/drug/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.delete(user)
        self.session.commit()

    def test_Delete_Medicament_by_Id_Invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Medicament(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/drug/10', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.delete(user)
        self.session.commit()

    def test_Create_Purchase(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/purchase/", data=json.dumps(self.medicament),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(Purchase).filter_by(number=5).delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()

    def test_Create_Purchase_Invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/purchase/", data=json.dumps(self.medicament),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.query(Purchase).filter_by(number=5).delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()

    def test_Get_Purchase_By_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        purchase = Purchase(user_id=2, product_id=1, number=3)
        self.session.add(purchase)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.get('/purchase/1', headers={"Authorization": f"Basic {creds}"})
        self.session.delete(purchase)
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(401, code)

    def test_Delete_Purchase_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        purchase = Purchase(user_id=2, product_id=1, number=3)
        self.session.add(purchase)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/purchase/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.delete(user)
        self.session.commit()

    def test_Delete_Purchase_by_Id_Invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        purchase = Purchase(user_id=2, product_id=1, number=3)
        self.session.add(purchase)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/purchase/9', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.delete(user)
        self.session.commit()