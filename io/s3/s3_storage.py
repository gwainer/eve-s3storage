from eve.io.media import MediaStorage
from flask.app import Flask
from flask import current_app
import boto3
from botocore.exceptions import ClientError
from bson.objectid import ObjectId
from io.s3.s3_out import S3Out


BUCKET = current_app.config['S3_STORAGE']['BUCKET']
AWS_REGION = current_app.config['S3_STORAGE']['AWS_REGION']
AWS_KEY = current_app.config['S3_STORAGE']['AWS_KEY']
AWS_SECRET = current_app.config['S3_STORAGE']['AWS_SECRET']


class S3MediaStorage(MediaStorage):
    """
    MediaStorage implementation compatible with AWS S3 service.
    """
    def __init__(self, app=None):
        """
        :param app: the flask application (eve itself). This can be used by
        the class to access, amongst other things, the app.config object to
        retrieve class-specific settings.
        """
        super(S3MediaStorage, self).__init__(app)
        self.validate()
        self.s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                               aws_secret_access_key=AWS_SECRET,
                               region_name=AWS_REGION)

    def validate(self):
        """ Make sure that the application is an eve application.
        instance.
        """
        if self.app is None:
            raise TypeError('Application object cannot be None')

        if not isinstance(self.app, Flask):
            raise TypeError('Application object must be a Eve application')

    def exists(self, id_or_filename, resource=None):
        try:
            self.s3.get_object(Bucket=BUCKET, Key=id_or_filename)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return False
        return True

    def get(self, id_or_filename, resource=None):
        try:
            s3_object = self.s3.get_object(Bucket=BUCKET, Key=str(id_or_filename))
        except ClientError as ex:
            # log.error('Error getting file {}. {}'.format(id_or_filename, ex))
            return None

        length = s3_object.get('ContentLength', 1500)
        content_type = s3_object.get('ContentType', 'image/jpg')
        last_modified = s3_object.get('LastModified', None)

        assert 'Body' in s3_object
        response = S3Out(s3_object['Body'].read(),
                         content_type, last_modified, length)
        # log.info('Returning response for file {}'.format(id_or_filename))
        return response

    def delete(self, id_or_filename, resource=None):
        return self.s3.delete_object(Bucket=BUCKET, Key=id_or_filename)

    def put(self, content, filename=None, content_type=None, resource=None):
        _id = str(ObjectId())
        self.s3.upload_fileobj(content, BUCKET, _id, ExtraArgs={'ContentType': content_type})
        # log.info('File {} stored in bucket {}'.format(filename, BUCKET))
        return _id
