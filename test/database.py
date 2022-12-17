# coding:utf-8
import unittest
from model import UserModel,PetModel,ServeModel, db
from exts import app


class TestDatabase(unittest.TestCase):
    """Test database case"""
    def setUp(self):
        #Enable Test Mode
        app.debug = True
        #database configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/pet-hospital?charset=utf8t"
        db.drop_all()
        #The first table is generated
        db.create_all()

    def tearDown(self):
        """Called after all test methods have been executed"""
        # Test task to clear records
        db.session.remove()
        # Clearing Database Data
        db.drop_all()


    def test_adm(self):
        """Test whether the administrator account exists"""
        adm = UserModel.query.filter_by(email="Charlie@adm.com").first()
        self.assertIsNotNone(adm)
        self.assertEqual(adm.email, "itcast")

    def test_user(self):
        """Test add author cases"""
        user = UserModel(username="Wangyue", email="wangyue@qq.com",password="wangyue")
        db.session.add(user)
        db.session.commit()

        ret_user = UserModel.query.filter_by(email="wangyue@qq.com").first()

        self.assertIsNotNone(ret_user)

        self.assertEqual(ret_user.email, "itcast")

    def test_serve(self):
        """Test the case for adding a service"""
        serve = ServeModel(servename="asdcv", classification="Vaccine",obj="Cat",price="88.88",introduction="A Vaccine")
        db.session.add(serve)
        db.session.commit()

        ret_serve = ServeModel.query.filter_by(servename="asdcv").first()

        self.assertIsNotNone(ret_serve)

        self.assertEqual(ret_serve.servename, "itcast")

    def test_pet(self):
        """Test the case of adding a pet"""
        pet = PetModel(masterid="3", petname="datou",species="Cat",breed="Shorthair",sex="Male",birthday="2021-05-15")
        db.session.add(pet)
        db.session.commit()

        ret_pet = PetModel.query.filter_by(petname="datou").first()

        self.assertIsNotNone(ret_pet)

        self.assertEqual(ret_pet.email, "itcast")



if __name__ == '__main__':
    unittest.main()