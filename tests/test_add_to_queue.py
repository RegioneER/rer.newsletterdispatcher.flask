# -*- coding: utf-8 -*-

import json


def test_route_accept_only_post(client):
    # Given
    payload = json.dumps({})

    # When
    response = client.get(
        '/add-to-queue',
        headers={"Content-Type": "application/json"},
        data=payload,
    )

    # Then
    assert response.status_code == 405


def test_route_does_not_accept_empty_request(client):
    # Given
    payload = json.dumps({})

    # When
    response = client.post(
        '/add-to-queue',
        headers={"Content-Type": "application/json"},
        data=payload,
    )

    # Then
    assert response.status_code == 400
    assert response.json['message'] == {
        '_authenticator': 'Missing required parameter in the JSON body or the post body or the query string'  # noqa
    }


def test_route_has_two_required_parameters(client):
    # Given
    payload = json.dumps({'_authenticator': 'foo'})

    # When
    response = client.post(
        '/add-to-queue',
        headers={"Content-Type": "application/json"},
        data=payload,
    )

    # Then
    assert response.status_code == 400
    assert response.json['message'] == {
        'uid': 'Missing required parameter in the JSON body or the post body or the query string'  # noqa
    }


def test_route_return_queue_infos(client):
    # Given
    payload = json.dumps({'_authenticator': 'foo', 'uid': 'bar'})

    # When
    response = client.post(
        '/add-to-queue',
        headers={"Content-Type": "application/json"},
        data=payload,
    )
    # Then
    assert response.status_code == 200
    assert 'job_id' in response.json
    assert 'date' in response.json
