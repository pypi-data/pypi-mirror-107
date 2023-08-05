from collections import OrderedDict
from ..repository.repository_object import RepositoryObject
from ..attachment import Attachment

class BaseNode(RepositoryObject):

    def __init__(self, branch, data):
            super(BaseNode, self).__init__(branch.repository, data)
            
            self.branch_id = branch._doc
            self.branch = branch

    def uri(self):
        return '%s/nodes/%s' % (self.branch.uri(), self._doc)

    def refresh(self):
        uri = self.uri() + '/refresh'
        return self.client.post(uri)

    def download_attachment(self, attachment_id='default'):
        uri = self.uri() + '/attachments/' + attachment_id

        return self.client.get(uri, output_json=False)

    def upload_attachment(self, file, content_type, attachment_id='default', filename=None):
        uri = self.uri() + '/attachments/' + attachment_id
        name = filename if filename else attachment_id

        return self.client.upload(uri, name, file, content_type)

    def delete_attachment(self, attachment_id='default'):
        uri = self.uri() + '/attachments/' + attachment_id
        return self.client.delete(uri)
    
    def list_attachments(self):
        uri = self.uri() + '/attachments'
        response = self.client.get(uri)
        return Attachment.attachments_map(self, response['rows'])

    def get_feature_ids(self):
        features_obj = self.data['_features']
        return features_obj.keys()

    def get_feature(self, feature_id):
        features_obj = self.data['_features']
        return features_obj.get(feature_id)

    def has_feature(self, feature_id):
        features_obj = self.data['_features']
        return feature_id in features_obj

    def add_feature(self, feature_id, feature_config):
        uri = self.uri() + '/features/' + feature_id
        self.client.post(uri, data=feature_config)
        self.reload()
    
    def remove_feature(self, feature_id):
        uri = self.uri() + '/features/' + feature_id
        self.client.delete(uri)
        self.reload()

    @classmethod
    def node_map (cls, branch, data):
        return OrderedDict((node['_doc'], cls.build_node(branch, node)) for node in data)

    @classmethod
    def build_node (cls, branch, data, force_association=False):
        if force_association or ('is_association' in data and data['is_association']):
            from ..association import Association
            return Association(branch, data)
        else:
            from . import Node
            return Node(branch, data)