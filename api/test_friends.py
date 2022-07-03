import time

from .setup_client import client
from .sample_user import get_sample_user
from .test_auth import get_auth_headers


def test_send_invite():
    user1_id = (client.post('/users/', json=get_sample_user(1))).json()
    global user2_id
    user2_id = (client.post('/users/', json=get_sample_user(2))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=1)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    friendship = response.json()
    assert friendship['inviting_friend'] == user1['username']
    assert friendship['accepting_friend'] == user2['username']


def test_send_invite_requires_auth():
    user1_id = (client.post('/users/', json=get_sample_user(1))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    response = client.post(f'/users/{user1_id}/friends/invite')
    assert response.status_code == 401


def test_user_cannot_send_self_invite():
    user111_id = (client.post('/users/', json=get_sample_user(111))).json()
    user111 = (client.get(f'/users/{user111_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=111)
    slug = f'/users/{user111_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    assert response.status_code == 403


def test_get_invites_requires_auth():
    response = client.get(f'/users/{user2_id}/invites/')
    assert response.status_code == 401


def test_user_can_only_see_their_own_invites():
    headers = get_auth_headers(client=client, sample_user_id=1)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    assert response.status_code == 403


def test_get_invites():
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    invites = response.json()
    assert response.status_code == 200
    assert len(invites)


def test_accept_invite_requires_auth():
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    invite['has_been_accepted'] = True
    invite['friendship_start_date'] = int(time.time())
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite
    )
    assert response.status_code == 401


def test_accept_invite():
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    friends_before = (client.get(f'/users/{user2_id}/friends/')).json()
    [invite] = response.json()
    invite['has_been_accepted'] = True
    invite['friendship_start_date'] = int(time.time())
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite,
        headers=headers
    )
    assert response.json()
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    invites = response.json()
    assert len(invites) == 0
    friends_now = (client.get(f'/users/{user2_id}/friends/')).json()
    assert len(friends_before) < len(friends_now)


def test_cannot_accepted_already_accepted_invite():
    # send invite
    user1_id = (client.post('/users/', json=get_sample_user(333))).json()
    user2_id = (client.post('/users/', json=get_sample_user(444))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=333)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    # accept invite
    headers = get_auth_headers(client=client, sample_user_id=444)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    invite['has_been_accepted'] = True
    invite['friendship_start_date'] = int(time.time())
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite,
        headers=headers
    )
    # accept invite again
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite,
        headers=headers
    )
    assert response.status_code == 404


def test_get_friends():
    response = client.get(f'/users/{user2_id}/friends/')
    assert response.status_code == 200


def test_unfriend():
    user1 = get_sample_user(1)
    friends = (client.get(f'/users/{user2_id}/friends/')).json()
    assert len(friends)
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.post(
        f'/users/{user2_id}/friends/{user1["username"]}/delete/',
        headers=headers
    )
    assert response.json()
    friends = (client.get(f'/users/{user2_id}/friends/')).json()
    assert len(friends) == 0
    response = client.post(
        f'/users/{user2_id}/friends/{user1["username"]}/delete/',
        headers=headers
    )
    assert response.status_code == 400


def test_only_authorized_can_unfriend():
    user1 = get_sample_user(1)
    response = client.post(f'/users/{user2_id}/friends/{user1["username"]}/delete/')
    assert response.status_code == 401


def test_only_friends_can_unfriend():
    user1 = get_sample_user(1)
    user2_id = (client.post('/users/', json=get_sample_user(123))).json()
    user2 = (client.get(f'/users/{user2_id}')).json()

    friends = (client.get(f'/users/{user2_id}/friends/')).json()
    assert len(friends) == 0
    # remove friend
    headers = get_auth_headers(client=client, sample_user_id=123)
    response = client.post(
        f'/users/{user2_id}/friends/{user1["username"]}/delete/',
        headers=headers
    )
    assert response.status_code == 400


def test_only_invited_user_can_accept():
    user2 = get_sample_user(2)
    headers = get_auth_headers(client=client, sample_user_id=2)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    invites = response.json()
    assert len(invites) == 0
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invites,
        headers=headers
    )
    assert response.status_code == 422


def test_cannot_send_invite_if_there_is_one_sent():
    user1_id = (client.post('/users/', json=get_sample_user(1))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=1)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    resent = client.post(slug, headers=headers)
    
    assert resent.status_code == 400


def test_cannot_send_invite_if_the_users_are_already_friends():
    user1_id = (client.post('/users/', json=get_sample_user(101))).json()
    user2_id = (client.post('/users/', json=get_sample_user(102))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    # send invite
    headers = get_auth_headers(client=client, sample_user_id=101)
    response = client.post(f'/users/{user2_id}/friends/invite/', headers=headers)
    assert response.status_code == 200
    # accept invite
    headers = get_auth_headers(client=client, sample_user_id=102)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    invite['has_been_accepted'] = True
    invite['friendship_start_date'] = int(time.time())
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite,
        headers=headers
    )
    assert response.status_code == 200
    # send another invite
    headers = get_auth_headers(client=client, sample_user_id=101)
    response = client.post(f'/users/{user2_id}/friends/invite/', headers=headers)
    assert response.status_code == 400


def test_delete_invite_requires_auth():
    user1_id = (client.post('/users/', json=get_sample_user(121))).json()
    user2_id = (client.post('/users/', json=get_sample_user(122))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=121)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)

    headers = get_auth_headers(client=client, sample_user_id=122)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    response = client.post(
        f'/users/{user2_id}/friends/invites/delete/', 
        json=invite
    )
    assert response.status_code == 401


def test_delete_invite():
    user1_id = (client.post('/users/', json=get_sample_user(33))).json()
    user2_id = (client.post('/users/', json=get_sample_user(44))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=33)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    friendship = response.json()
    assert friendship['inviting_friend'] == user1['username']
    assert friendship['accepting_friend'] == user2['username']
    headers = get_auth_headers(client=client, sample_user_id=44)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    response = client.post(
        f'/users/{user2_id}/friends/invites/delete/', 
        json=invite,
        headers=headers
    )
    assert response.json()
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    invites = response.json()
    assert len(invites) == 0


def test_cannot_delete_already_accepted_invite():
    user1_id = (client.post('/users/', json=get_sample_user(103))).json()
    user2_id = (client.post('/users/', json=get_sample_user(104))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    headers = get_auth_headers(client=client, sample_user_id=103)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    friendship = response.json()
    assert friendship['inviting_friend'] == user1['username']
    assert friendship['accepting_friend'] == user2['username']
    headers = get_auth_headers(client=client, sample_user_id=104)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    [invite] = response.json()
    response = client.post(
        f'/users/{user2_id}/friends/invites/delete/', 
        json=invite,
        headers=headers
    )
    assert response.json()
    # delete again
    response = client.post(
        f'/users/{user2_id}/friends/invites/delete/', 
        json=invite,
        headers=headers
    )
    assert response.status_code == 404


def test_user_can_only_accept_own_invite():
    user1_id = (client.post('/users/', json=get_sample_user(105))).json()
    user2_id = (client.post('/users/', json=get_sample_user(106))).json()
    user1 = (client.get(f'/users/{user1_id}')).json()
    user2 = (client.get(f'/users/{user2_id}')).json()
    # send invite
    headers = get_auth_headers(client=client, sample_user_id=105)
    slug = f'/users/{user2_id}/friends/invite/'
    response = client.post(slug, headers=headers)
    assert response.status_code == 200
    # accept invite
    headers = get_auth_headers(client=client, sample_user_id=106)
    response = client.get(f'/users/{user2_id}/invites/', headers=headers)
    assert len(response.json()) == 1
    [invite] = response.json()
    invite['has_been_accepted'] = True
    invite['friendship_start_date'] = int(time.time())
    headers = get_auth_headers(client=client, sample_user_id=105)
    response = client.put(
        f'/users/{user2_id}/friends/invites/accept/', 
        json=invite,
        headers=headers
    )
    assert response.status_code == 403