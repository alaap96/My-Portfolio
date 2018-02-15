import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    # TODO implement

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:029785545301:Deployportfoliotopic')
    s3 = boto3.resource('s3')
    try:
        portfolio_bucket = s3.Bucket('alaapvasireddy.portfolio')
        build_bucket = s3.Bucket('alaapvasireddy')

        portfolio_zip = io.BytesIO()

        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                ExtraArgs= {'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print ('job done deploying from lambda_handler')
        topic.publish(Subject="Portfolio", Message="Portfolio Deployed!")
    except:
        topic.publish(Subject="Portfolio",Message="Deployed Failed!")
    return 'Hello from Lambda'
