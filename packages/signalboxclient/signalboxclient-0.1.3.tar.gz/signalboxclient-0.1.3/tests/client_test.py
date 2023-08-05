from context import signalboxclient
# import client
import uuid
import environment

creds = signalboxclient.client.Credentials(environment.api_key)
test_client = signalboxclient.client.SignalBoxClient(creds)
my_token = test_client.access_token

#create user
user_id = str(uuid.uuid1())
test_client.create_user('testuser', user_id)
print('created user with id=', user_id)
offer = test_client.create_offer('my_offer', 'AUD', 100, 50)
offer_id = offer['id']

experiment = test_client.create_experiment([offer_id], name='Experiment Name', segmentId= None, concurrentOffers=1)
print('created experiment')
experiment_id = experiment['id']

get_experiment_response = test_client.get_experiment(experiment_id)
print('\nPrinting get_experiment test response: ', get_experiment_response)

print('\nPrinting create_offer test response: ', offer)
print('\nPrinting create_experiment test response: ', experiment)

presentation = test_client.recommend_offer(experiment_id, user_id)
print(presentation)

# choose accept or rekect
tracked = test_client.track_recommendation_outcome(presentation, presentation['offers'][0]['id'], 'accept')
print(tracked)

print('\nPrinting recommendation test response: ', presentation)

print('\ntests successful')
