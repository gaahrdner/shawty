from flask import Flask, request, jsonify, redirect
from werkzeug.exceptions import BadRequest
from urllib.parse import urlparse

import settings
import boto3
import time
import shortuuid

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')

# Use an alphabet that doesn't contain similar characters
ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def validate_url(url):
    if url is None:
        raise BadRequest("URL key does not exist in the submitted JSON payload.")
    
    parsed_url = urlparse(url)

    if not parsed_url.scheme or "http" not in parsed_url.scheme:
        raise BadRequest("Unsupported or non-existent URL scheme; at this time only http and https are supported.")
    
    if not parsed_url.netloc:
        raise BadRequest("Malformed URL, please retry with a valid URL.")


def generate_uuid(url):
    shortuuid.set_alphabet(ALPHABET)
    uuid = shortuuid.ShortUUID().random(length=8)
    # add a lookup to ensure we don't have duplicates
    return uuid


def store_uuid(uuid, long_url):
    table = dynamodb.Table(settings.URL_TABLE)
    timestamp = int(time.time() * 1000)

    record = {
        'short_url': uuid,
        'long_url': long_url,
        'created_at': timestamp
    }

    table.put_item(Item=record)


def lookup_url(uuid):
    table = dynamodb.Table(settings.URL_TABLE)

    record = table.get_item(
        Key={
            'short_url': uuid
        }
    )

    return record    


@app.route('/', methods=['GET'])
def home():
    return "shawty - the url shortener"

# this is not great
@app.route('/favicon.ico')
def favicon():
    return "favicon"

@app.route('/<id>', methods=['GET'])
def get_url(id):

    try:
        long_url = lookup_url(id)['Item']['long_url']
        return redirect(long_url, 302)
    except KeyError:
        return jsonify(
            msg="short url not found."
        ), 404
    

@app.route('/', methods=['POST'])
def create_url():
    payload = request.get_json()
    url = payload.get('url')
    validate_url(url)

    uuid = generate_uuid(url)
    store_uuid(uuid, url)

    return jsonify(
        short_url=settings.BASE_URL + "/" + uuid
    )
