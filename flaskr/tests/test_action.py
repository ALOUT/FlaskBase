import flaskr
from flaskr import app
from flaskr.models import Entry

def setup_module():
	flaskr.db.drop_all()
	flaskr.models.init()

def test_post_entry():
	
	client = app.test_client()
	response = client.post('/add',
		data={'title':'test title1','text':'test text1'},
		follow_redirects=True)
	
	assert response.status_code == 200
	
	with app.test_request_context():
 		assert Entry.query.count() == 1
    	entry = Entry.query.get(1)
    	assert entry.title == 'test title1'
    	assert entry.text == 'test text1'