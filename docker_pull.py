import os
import sys
import gzip
from io import StringIO, BytesIO
import json
import hashlib
import shutil
import requests
import tarfile
import urllib3
urllib3.disable_warnings()

if len(sys.argv) != 2 :
	print('Usage:\n\tdocker_pull.py [repository/]image[:tag]\n')
	exit(1)

# Look for the Docker image to download
repo = 'library'
tag = 'latest'
try:
    repo,imgtag = sys.argv[1].split('/')
except ValueError:
    imgtag = sys.argv[1]
try:
    img,tag = imgtag.split(':')
except ValueError:
    img = imgtag
repository = '{}/{}'.format(repo, img)

# Get Docker token and fetch manifest v2
resp = requests.get('https://auth.docker.io/token?service=registry.docker.io&scope=repository:' + repository + ':pull', verify=False)
access_token = resp.json()['access_token']
auth_head = {'Authorization':'Bearer '+ access_token, 'Accept':'application/vnd.docker.distribution.manifest.v2+json'}

# Get image layer digests
resp = requests.get('https://registry-1.docker.io/v2/{}/manifests/{}'.format(repository, tag), headers=auth_head, verify=False)
if (resp.status_code != 200):
	print('Cannot fetch manifest for {} [HTTP {}]'.format(repository, resp.status_code))
	exit(1)
layers = resp.json()['layers']

# Create tmp folder that will hold the image
imgdir = 'tmp_{}_{}'.format(img, tag)
os.mkdir(imgdir)
print('Creating image structure in: ' + imgdir)

config = resp.json()['config']['digest']
confresp = requests.get('https://registry-1.docker.io/v2/{}/blobs/{}'.format(repository, config), headers=auth_head, verify=False)
file = open('{}/{}.json'.format(imgdir, config[7:]), 'wb')
file.write(confresp.content)
file.close()

content = [{
	'Config': config[7:] + '.json',
	'RepoTags': [ repository + ':' + tag ],
	'Layers': [ ]
	}]

empty_json = '{"created":"1970-01-01T00:00:00Z","container_config":{"Hostname":"","Domainname":"","User":"","AttachStdin":false, \
	"AttachStdout":false,"AttachStderr":false,"Tty":false,"OpenStdin":false, "StdinOnce":false,"Env":null,"Cmd":null,"Image":"", \
	"Volumes":null,"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":null}}'

# Build layer folders
parentid=''
for layer in layers:
	ublob = layer['digest']
	# FIXME: Creating fake layer ID. Don't know how Docker generates it
	fake_layerid = hashlib.sha256((parentid+'\n'+ublob+'\n').encode('utf-8')).hexdigest()
	layerdir = imgdir + '/' + fake_layerid
	os.mkdir(layerdir)

	# Creating VERSION file
	file = open(layerdir + '/VERSION', 'w')
	file.write('1.0')
	file.close()

	# Creating layer.tar file
	print(ublob[7:19] + ': Downloading...',
	sys.stdout.flush())
	bresp = requests.get('https://registry-1.docker.io/v2/{}/blobs/{}'.format(repository, ublob), headers=auth_head, verify=False)
	if (bresp.status_code != 200):
		print('\rERROR: Cannot download layer {} [HTTP {}]'.format(ublob[7:19], bresp.status_code, bresp.headers['Content-Length']))
		print(bresp.content)
		exit(1)
	print("\r{}: Pull complete [{}]".format(ublob[7:19], bresp.headers['Content-Length']))
	content[0]['Layers'].append(fake_layerid + '/layer.tar')
	file = open(layerdir + '/layer.tar', "wb")
	mybuff = BytesIO(bresp.content)
	unzLayer = gzip.GzipFile(fileobj=mybuff)
	file.write(unzLayer.read())
	unzLayer.close()
	file.close()
	
	# Creating json file
	file = open(layerdir + '/json', 'w')
	# last layer = config manifest - history - rootfs
	if layers[-1]['digest'] == layer['digest']:
		# FIXME: json.loads() automatically converts to unicode, thus decoding values whereas Docker doesn't
		json_obj = json.loads(confresp.content)
		del json_obj['history']
		del json_obj['rootfs']
	else: # other layers json are empty
		json_obj = json.loads(empty_json)
	json_obj['id'] = fake_layerid
	if parentid:
		json_obj['parent'] = parentid
	parentid = json_obj['id']
	file.write(json.dumps(json_obj))
	file.close()

file = open(imgdir + '/manifest.json', 'w')
file.write(json.dumps(content))
file.close()

content = { repository : { tag : fake_layerid } }
file = open(imgdir + '/repositories', 'w')
file.write(json.dumps(content))
file.close()

# Create image tar and clean tmp folder
docker_tar = repo + '_' + img + '.tar'
tar = tarfile.open(docker_tar, "w")
tar.add(imgdir, arcname=os.path.sep)
tar.close()
shutil.rmtree(imgdir)
print('Docker image pulled: ' + docker_tar)
