# NOTE: DO NOT FORK THIS REPOSITORY. CLONE AND SETUP A STANDALONE REPOSITORY.

# Adbrew Test!

Hello! This test is designed to specifically test your Python, React and web development skills. The task is unconventional and has a slightly contrived setup on purpose and requires you to learn basic concepts of Docker on the fly. 


# Solution

Errors faced during building docker images- 

1-	#0 1.953 The following packages have unmet dependencies:
	#0 2.081  mongodb-org-mongos : Depends: libssl1.1 (>= 1.1.0) but it is not installable       
	#0 2.081  mongodb-org-server : Depends: libssl1.1 (>= 1.1.0) but it is not installable       
	#0 2.081  mongodb-org-shell : Depends: libssl1.1 (>= 1.1.0) but it is not installable    
	
	Solution- Made changes in the docker file to install libssl1.1 from source url rather as it wasn't availbe on pip
	wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
	sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

2-	 > [adb_test-api 15/17] RUN easy_install pip:
	#0 0.486 /bin/sh: line 1: easy_install: command not found
	
	Solution-This was due to new pip not having easy-install as it was outdated and already integrated in the updated pip so I removed that from docker file
	

3-	There was an error regarding coroutines while starting the react server, it had to do with a SSL package and how node18 didn't support it properly to fix that we set node_options environment variable to --openssl-legacy-provider



Explanation of the Docker File-

The docker file sets up the host os or the host machine for other sub images or other images to work, in it we are using the 
python-3.8 image which is based off ubuntu/Debian, first we install all the required packages with apt-get install, then we install all dependencies for mongo, in which I faced some errors listed above, after that it installs yarn for the react server and after that it installs the python dependencies, in which there were some unmet dependencies and had an issue with easy-install as it was outdated so fixed them.

Explanation of Docker Compose file-

The docker compose file consists of the initial commands which need to be run in those instances along with the volumes that they are gonna use, they can use the same or different volumes, in this we have 3 instances, app,api and mongo, app one is for the react server, api is for the Django server and the mongo is for the mongo server, we specify on which ports we want the services up and running and what commands to run to make sure those services run well.

How I approached the full stack implementation-

Backend-

I went with the repository pattern for the backend making kind of a repository layer for mongo client so it can have insert  one, find and delete all methods for collection names so that it's easily isolated and decoupled and doesn't require too much of re-using code, I also created a service in views.py for ToDos which basically handles insertion, deletion and fetching of all ToDos data.

Frontend-

For frontend I simply used proper validations and state rendering in a way that it doesn't cause re-renders and only renders when necessary, I tried implementing tailwind styling, worked fine with npm run start but with docker I was facing some issues even after configuring package.json file correctly, apart from the styling the functionality works correctly although if given enough time I would have found a way to debug that too, I hope it's considerable.



# Structure

This repository includes code for a Docker setup with 3 containers:
* App: This is the React dev server and runs on http://localhost:3000. The code for this resides in src/app directory.
* API: This is the backend container that run a Django instance on http://localhost:8000. 
* Mongo: This is a DB instance running on port 27017. Django views already have code written to connect to this instance of Mongo.

We highly recommend you go through the setup in `Dockerfile` and `docker-compose.yml`. If you are able to understand and explain the setup, that will be a huge differentiator.

# Setup
1. Clone this repository (DO NOT FORK)
```
git clone https://github.com/adbrew/test.git
```
2. Change into the cloned directory and set the environment variable for the code path. Replace `path_to_repository` appropriately.
```
export ADBREW_CODEBASE_PATH="{path_to_repository}/test/src"
```
3. Build container (you only need to build containers for the first time or if you change image definition, i.e., `Dockerfile`). This step will take a good amount of time.
```
docker-compose build
```
4. Once the build is completed, start the containers:
```
docker-compose up -d
```
5. Once complete, `docker ps` should output something like this:
```
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                      NAMES
e445be7efa61   adbrew_test_api     "bash -c 'cd /src/re…"   3 minutes ago   Up 2 seconds   0.0.0.0:8000->8000/tcp     api
0fd203f12d8a   adbrew_test_app     "bash -c 'cd /src/ap…"   4 minutes ago   Up 3 minutes   0.0.0.0:3000->3000/tcp     app
884cb9296791   adbrew_test_mongo   "/usr/bin/mongod --b…"   4 minutes ago   Up 3 minutes   0.0.0.0:27017->27017/tcp   mongo
```
6. Check that you are able to access http://localhost:3000 and http://localhost:8000/todos
7. If the containers in #5 or #6 are not up, we would like you to use your debugging skills to figure out the issue. Only reach out to us if you've exhausted all possible options. The `app` container may take a good amount of time to start since it will download all package dependencies.

# Tips
1. Once containers are up and running, you can view container logs by executing `docker logs -f --tail=100 {container_name}` Replace `container_name` with `app` or `api`(output of `docker ps`)
2. You can enter the container and inspect it by executing `docker exec -it {container_name} bash` Replace `{container_name}` with `app` or `api` (output of `docker ps`)
3. Shut all containers using `docker-compose down`
4. Restart a container using `docker restart {container_name}`


# Task

When you run `localhost:3000`, you would see 2 things:
1. A form with a TODO description textbox and a submit button. On this form submission, the app should interact with the Django backend (`POST http://localhost:8000/todos`) and create a TODO in MongoDB.
2. A list with hardcoded TODOs. This should be changed to reflect TODOs in the backend (`GET http://localhost:8000/todos`). 
3. When the form is submitted, the TODO list should refresh again and fetch latest list of TODOs from MongoDB.

# Instructions [IMPORTANT] 
1. All React code should be implemented using [React hooks](https://reactjs.org/docs/hooks-intro.html) and should not use traditional stateful React components and component lifecycle method.
2. Do not use Django's model, serializers or SQLite DB. Persist and retrieve all data from the mongo instance. A `db` instance is already present in `views.py`.
3. Do not bypass the Docker setup. Submissions that do not have proper docker setup will be rejected.
4. We are looking for developers who have strong fundamentals and can ramp up fast. We expect you to learn and grasp basic React Hooks/Mongo/Docker concepts on the fly.
5. Do not fork this repository or submit your solution as a PR since this is a public repo and there are other candidates taking the same test. Send us a link to your repo privately.
6. If you are able to complete the test, we will have a live walkthrough of your code and ask questions to check your understanding.
7. The code for the actual solution is pretty easy. The code quality in your solution should be production-ready - error handling, abstractions, well-maintainable and modular code. If you're not aware, we recommend reading a bit about software design principles and applying them (both JS and Python). Here are some reading resources to get you started:
   * https://kinsta.com/blog/python-object-oriented-programming/
   * https://realpython.com/solid-principles-python/
   * https://www.toptal.com/python/python-design-patterns

