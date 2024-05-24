# FireGuard - Group 5

The FireGuard Cloud Service v.0.1.0 for the ADA502 course.

**Collaborators:** Alexander Ringheim, Daniel Vikøyr, Sigve Bjørhovde, Thomas Mavropoulos

![firerisk drawio](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/4137667/55bc8db2-eecd-4cf1-8f12-f2505d1a3d48)

The project git repository is publicly available on [Github](https://github.com/ADA502-FireGuard/frcm-monolith). 
The project consists of two separately developed microservices. These services can be found in their separate git reposiories, the main FireRisk API service [dynamic-frcm](https://github.com/ADA502-FireGuard/dynamic-frcm) and the database service [postgres-frcm](https://github.com/ADA502-FireGuard/postgres-frcm).

The Docker repository for dynamic-frcm can be found at [DockerHub](https://hub.docker.com/r/alexbringh/fireguard-v-0-1-0/).

We currently provide these security measures (HTTPS) and have begun implementing authentication through keycloak....

The Fireguard service is implemented as multiple micro services, offloading tasks such as encryption to the keyclock service, the retrieval of coordinates to Kartverket, the retrieval of weather data to Frost, the storage of results to a separate database service and the actual calculation to the Fireguard API service. Whilst the service strives to offload each task as a microservice, it has become necessary to break with the ideal idea of a microservice architecture by having the Fireguard API service perform most of the coordination of tasks as well, not just limiting it to the calculation alone.

The service offers interfacing with clients as a RestAPI, primarily offering GET requests and some PUT requests that can be easily used by a client directly or a middleware service. 


## Getting started

There are mainly two recommended ways of getting the service running on your machine. You can either clone the Git repository or grab the Docker image. We describe the required steps to both approaches below.

For interacting with the API in Windows, we recommend these applications:

* [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701) - Modern terminal application
* [Bruno](https://www.usebruno.com/) - Web API client

> **Tip:** Windows comes with two terminals pre-installed, `Command Prompt` and `PowerShell`. You can access either from the Windows search bar.

Note that FireGuard encrypts traffic with `Secure Sockets Layer`. For purposes of testing and demoing, we provide keys with the project. As they are publicly available, they should not be trusted in production settings. Generate your own `SSL` keys and add them before deploying.

### Running with container orchestration

This is the most convenient way to quickly get all the services running.

With container orchestration through docker-compose, we're able to provide an easy way to run our two microservices `dynamic-frcm` and `postgres-frcm` in conjunction. To this end, we have prepared a monorepo.

Clone the `frcm-monolith` repository to your machine

```bash
git clone https://github.com/ADA502-FireGuard/frcm-monolith.git
```

Navigate to the cloned directory

```bash
cd frcm-monolith
```

Add the MET API ID and secret to your environment variables

```bash
export MET_CLIENT_ID="<INSERT ID>"
export MET_CLIENT_SECRET="<INSERT SECRET>"
```

You can now run the image

```bash
docker-compose up -d
```

You can now access the Fireguard API service at `https://127.0.0.1:8000`. The database is accessible locally on port `5432`. The database can be accessed via `Adminer` at `http://127.0.0.1:8888`, or through whichever PostgreSQL compatible database management tool you prefer.

#### Running tests

Our repository includes a comprehensive suite of tests covering client interactions with geocoding and meteorological data, core computations, data models, fire risk calculations, data extraction modules, API integrations, logical processing, and weather data handling. These tests ensure the robustness and reliability of our software. You can run all tests using the provided Docker command.

```bash
docker-compose run firerisk poetry run pytest
```

### Running as microservices

FireGuard employs [Met.no's API](https://api.met.no), which requires authentication to use. You need to register for credentials [here](https://frost.met.no/auth/requestCredentials.html) before beginning.

> **Note:** Assuming you are using Windows, you will probably want to have [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) installed to run the Docker image. In tha case, start `Docker Desktop` before continuing.

Clone the `dynamic-frcm` repository to your machine

```bash
git clone https://github.com/ADA502-FireGuard/dynamic-frcm.git
```

Navigate to the cloned directory

```bash
cd dynamic-frcm
```

Add the MET API ID and secret to your environment variables

```bash
export MET_CLIENT_ID="<INSERT ID>"
export MET_CLIENT_SECRET="<INSERT SECRET>"
```

Build a docker image

```bash
docker build -t firerisk .
```

Now, run the docker container

```bash
docker run firerisk
```

You can exit anytime by pressing `CTRL+C`

You will need to do the equivalent for `postgres-frcm` repository and set up a bridged network to get database functionality.

#### Via DockerHub

If you would rather run the microservice directly from `DockerHub` through `Docker Desktop`. Simply enter `alexbringh/fireguard-v-0-1-0:latest` into the top search bar and pull the latest image.

> **Tip:** You can also achieve the same result through the command-line with the command, `docker pull alexbringh/fireguard-v-0-1-0:latest`!

Before attempting to run a container, find the image under the `Images` tab. Select the play button and enter 8000 as the host port under `Optional settings`. Now press `Run`.

![rundockerdesktop](https://github.com/ADA502-FireGuard/dynamic-frcm/assets/4137667/70963408-f437-44ec-bed0-5cd2c8aeb915)

## User guide

Once running, the FireGuard Cloud Service will accept inputs. Assuming the Docker container is running locally you can reach the API at `https://127.0.0.1:8000`.

The service accepts inputs in the form of standard HTTP requests through a `RESTful API`. You may use any framework or program that sends HTTP requests such as `get` and `post` to interact with the service. The `API endpoints` with the valid `query parameters` are described below.

For simple testing of functionality, we recommend using `Bruno`, as it gives a simple GUI for setting up these requests. We have prepared a pre-configured Postman collection which can be imported into `Bruno`. You can find the tests [here](https://github.com/ADA502-FireGuard/dynamic-frcm/tree/main/tests).

 For stress-testing or multi-user simulation of the system, it would be more appropriate to create a custom multithreading script. By default, `Bruno` only sends one request at a time.

### Setting up requests to the FireGuard Cloud Service

The following examples assume that you have set up the Docker container as detailed above.

The most simple HTTP request that can be made of FireGuard is `GET https://127.0.0.1:8000/`, which will simply return a welcoming message, letting you know the service is available.

The next endpoint is `/services", which lists available API endpoints and query parameters.

```bash
GET https://localhost:8000/services
```

> **Note:** As of v0.1.0 the services list is not updated to include all services, and you should instead follow this guide for now.

FireGuard offers five different methods of calculating fire risk. You may manually insert weather data, location and timestamp yourself, and have the model simply calculate and return the results using the following request.

```bash
POST https://localhost:8000/rawdata?temp=...
```

Usually, users will not have all necessary data to use the `rawdata` option directly. Rather, a more common use-case is someone interested in discovering the fire risk at a certain location, such as an address, postal code or even longitude and latitude. Based on the given location data point, FireGuard offers to retrieve the remaining required parameters for the user. FireGuard accomplishes this by seamlessly converting that location to coordinates through a GeoCoding service. We then retrieve weather data for those coordinates through a Meteorological service, before finally doing the fire risk calculations.

The available options for the area service are as follows.

#### GPS

```bash
POST https://localhost:8000/area/gps?lon=...+lat=...+day=...
```

This option takes coordinates as inputs along with a timedelta for which the service is to calculate for.
The required tags.

```bash
lon:  float - The longitude coordinate
lat:  float - The latitude coordinate
days: float - Number of days to be calculated for
```

```bash
POST https://localhost:8000/area/address?adr=...+days=...
```

```bash
adr:  str - The address string. Make sure it is a valied address, for example "Inndalsveigen 28"
days: float - The number of days to be calculated for.
```

#### Postcode

```bash
GET http://localhost:8000/area/postcode?postcode=...+days=...
```

This option takes a Norwegian four-digit postcode and uses a Geocoding API to try and turn the address into coordinates automatically. Normally the Geocoding API will give a whole lot of coordinates for the postcode in question, the code requests that only the one best representing the postcode area be sent. This is a hard-coded option into FireGuard, however it is possible to change this option of course, but the user does not have this option by default.
The required tags.

```bash
postcode:  int - The four-digit postcode for the area. Make sure that the postcode is valid. For example "5063" (Bergen)
days:      float - The number of days to be calculated for.
```

## Following Versions

In the upcoming releases, our emphasis will shift towards a robust continuous integration process. Our new objectives for the product include accommodating multiple data points for any given feature and expanding our offerings to encompass additional functionalities like postal area specification, enhanced authentication, and data subscriptions for specific regions.

To safeguard against errors and potential security vulnerabilities due to user input, we will be enhancing our input validation measures. Furthermore, there's a planned incorporation of consistently timed automated test routines, such as combined smoke and security testing, to ensure the software's integrity.

We will be integrating a suite of comprehensive tests -- including integration, functional, performance, load, stress, security, and usability assessments. These tests will support our regression strategy and acceptance criteria to drive quality assurance. Moreover, as the project evolves, the role of continuous deployment is becoming increasingly vital. Consequently, we are placing greater emphasis on code reliability and efficient testing protocols, as the complexity and resource demands for manual testing grow, underscoring the need for exceptionally thorough testing practices. 
