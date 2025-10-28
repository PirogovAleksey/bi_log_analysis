#!/usr/bin/env python3
"""
Setup Elasticsearch index template for banking logs
"""

import requests
import json
import time
import sys


def wait_for_elasticsearch(url='http://localhost:9200', timeout=60):
    """Wait for Elasticsearch to be ready"""
    print(f"Waiting for Elasticsearch at {url}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Elasticsearch is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(2)
        print(".", end="", flush=True)

    print("\nTimeout waiting for Elasticsearch")
    return False


def create_index_template(url='http://localhost:9200'):
    """Create index template for banking logs"""
    template_url = f"{url}/_index_template/banking-logs-template"

    # Read template from file
    with open('elasticsearch/index_template.json', 'r') as f:
        template = json.load(f)

    print(f"\nCreating index template...")

    response = requests.put(
        template_url,
        json=template,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code in [200, 201]:
        print("Index template created successfully!")
        return True
    else:
        print(f"Failed to create index template: {response.status_code}")
        print(response.text)
        return False


def main():
    es_url = 'http://localhost:9200'

    if not wait_for_elasticsearch(es_url):
        sys.exit(1)

    if not create_index_template(es_url):
        sys.exit(1)

    print("\nElasticsearch setup completed successfully!")


if __name__ == '__main__':
    main()
