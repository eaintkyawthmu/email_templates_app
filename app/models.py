from bson.objectid import ObjectId
from flask import current_app
from . import mongo  # Ensure mongo is initialized in your __init__.py

class TemplateManager:
    @staticmethod
    def get_all_templates():
        """Retrieve all templates from the database."""
        try:
            templates = mongo.db.templates.find()
            return list(templates)
        except Exception as e:
            current_app.logger.error("Failed to retrieve all templates: %s", e)
            return []
        
    @staticmethod
    def get_template_by_id(template_id):
        """Retrieve a template by its ID."""
        try:
            # ObjectId is used for converting the string ID to a MongoDB ObjectId
            return mongo.db.templates.find_one({'_id': ObjectId(template_id)})
        except Exception as e:
            current_app.logger.error(f"Error retrieving template by ID {template_id}: {e}")
            return None

    @staticmethod
    def get_templates_by_tag(tag):
        """Retrieve templates by a specific tag."""
        try:
            templates = mongo.db.templates.find({"tags": tag})
            return list(templates)
        except Exception as e:
            current_app.logger.error(f"Error retrieving templates by tag {tag}: {e}")
            return []

    @staticmethod
    def add_template(data):
        """Add a new template to the database."""
        try:
            return mongo.db.templates.insert_one(data).inserted_id
        except Exception as e:
            current_app.logger.error(f"Error adding new template: {e}")
            return None

    @staticmethod
    def update_template(template_id, data):
        """Update an existing template."""
        try:
            result = mongo.db.templates.update_one({'_id': ObjectId(template_id)}, {'$set': data})
            return result.modified_count > 0  # Returns True if the document was updated
        except Exception as e:
            current_app.logger.error(f"Error updating template ID {template_id}: {e}")
            return False

    @staticmethod
    def delete_template(template_id):
        """Delete a template by its ID."""
        try:
            result = mongo.db.templates.delete_one({'_id': ObjectId(template_id)})
            return result.deleted_count > 0  # Returns True if the document was deleted
        except Exception as e:
            current_app.logger.error(f"Error deleting template ID {template_id}: {e}")
            return False
        
    @staticmethod
    def search_templates(query):
        """Search templates by text index."""
        try:
            templates = mongo.db.templates.find({"$text": {"$search": query}})
            return list(templates)
        except Exception as e:
            current_app.logger.error(f"Error searching templates: {e}")
            return []
        
    @staticmethod
    def get_templates_by_tag(tag):
        templates = mongo.db.templates.find({"tags": tag})
        return list(templates)