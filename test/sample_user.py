
def get_sample_user(user_id: int):
    return {
      'username': f'user{user_id}',
      'password': 'secret',
      'date_of_birth': 1635353891,
      'email': f'user{user_id}@gmail.com'
    }

def get_sample_user_with_points(user_id: int):
    return get_sample_user(user_id).update({
        'points': 30
    })

def get_sample_user_with_tournaments(user_id: int):
    return get_sample_user(user_id).update({
        'tournaments': '3,5,7'
    })

sample_user = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com'
}

sample_user_with_points = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com',
  'points': 30
}

sample_user_with_tournaments = {
  'username': 'user1',
  'password': 'secret',
  'date_of_birth': 1635353891,
  'email': 'user1@gmail.com',
  'points': 30,
  'tournaments': '3,5,7'
}

