from . import mongo

class TemplateManager:
    @staticmethod
    def get_all_templates():
        templates = mongo.db.templates.find()
        return list(templates)

    @staticmethod
    def get_template_by_id(template_id):
        template = mongo.db.templates.find_one({'_id': template_id})
        return template

    @staticmethod
    def add_template(data):
        mongo.db.templates.insert_one(data)

    @staticmethod
    def update_template(template_id, data):
        mongo.db.templates.update_one({'_id': template_id}, {'$set': data})

    @staticmethod
    def delete_template(template_id):
        mongo.db.templates.delete_one({'_id': template_id})
