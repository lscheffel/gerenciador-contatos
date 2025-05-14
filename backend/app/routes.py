import re
from flask_restful import Resource, Api, reqparse
from app.models import Contact
from app.database import get_db
from flask import Blueprint
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, help="Name cannot be blank")
parser.add_argument("email", type=str, required=True, help="Email cannot be blank")
parser.add_argument("phone", type=str, required=True, help="Phone number is optional")

class ContactResource(Resource):
    def get(self, contact_id):
        db = next(get_db())
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.error(f"Contato {contact_id} não encontrado")
            return {"message": "Contact not found"}, 404
        logger.info(f"Contato {contact_id} retornado")
        return {"id": contact.id, "name": contact.name, "email": contact.email, "phone": contact.phone}

    def put(self, contact_id):
        args = parser.parse_args()
        db = next(get_db())
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.error(f"Contato {contact_id} não encontrado para atualização")
            return {"message": "Contact not found"}, 404
        contact.name = args["name"]
        contact.email = args["email"]
        contact.phone = args["phone"]
        db.commit()
        logger.info(f"Contato {contact_id} atualizado")
        return {"id": contact.id, "name": contact.name, "email": contact.email, "phone": contact.phone}

    def delete(self, contact_id):
        db = next(get_db())
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.error(f"Contato {contact_id} não encontrado para deleção")
            return {"message": "Contact not found"}, 404
        db.delete(contact)
        db.commit()
        logger.info(f"Contato {contact_id} deletado")
        return {"message": "Contact deleted"}

class ContactListResource(Resource):
    def get(self):
        db = next(get_db())
        contacts = db.query(Contact).all()
        logger.info("Lista de contatos retornada")
        return [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in contacts]

    def post(self):
        args = parser.parse_args()
        db = next(get_db())
        contact = Contact(name=args["name"], email=args["email"], phone=args["phone"])
        db.add(contact)
        db.commit()
        logger.info(f"Contato {contact.id} criado")
        return {"id": contact.id, "name": contact.name, "email": contact.email, "phone": contact.phone}, 201

api.add_resource(ContactListResource, "/contacts")
api.add_resource(ContactResource, "/contacts/<int:contact_id>")