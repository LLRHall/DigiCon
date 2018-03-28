import boto
import boto.s3
import sys
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAJONJ4JMC5ZSSNAAQ'
AWS_SECRET_ACCESS_KEY = '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'
TEST_FILE = 'test_2.jpg'

bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
# bucket_name = 'test-bucket-301'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)

bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

testfile = TEST_FILE
print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


k = Key(bucket)
k.key = TEST_FILE
k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=10)