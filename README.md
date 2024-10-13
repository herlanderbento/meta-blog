<center>
  <p align="center">
    <img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png?1576869008" alt="Python Logo" width="130" />
  </p>  
  <h1 align="center">🚀 Meta Blog - Python</h1>
  <p align="center">
   Microservice for the  Meta Blog Administration backend<br />Using Clean Architecture, DDD, Test Pyramid and the main current market best practices.
  </p>
</center>
<br />


## How to start

To start the project on you local machine follow the steps below:

```bash
python3 -m venv venv

# For linux/macos
source venv/bin/activate

# For windown
. venv\Scripts\activate

pip install -r requirements.txt

python3 manage.py runserver
```

<!-- ## How to execute?

- Just clone the Repository:

```sh
git clone https://github.com/herlanderbento/fc3-admin-video-catalog-typescript.git
```

- Upload the project containers
  <br/>

```sh
docker-compose up -d
```

<br/>

- Install the project dependencies

```sh
npm install
```

- Run tests

```sh
npm run test:e2e
```
```sh
npm run test
```

<br/>
<Br/>

# Development Environment Setup

## Technologies and Tools Used

- IDE (Visual Studio Code): We recommend using a TypeScript-compatible IDE for efficient development.

- Node 18v or + installed

- Docker: Used to create and manage containers, making it easier to configure the development environment.

<br />

## Architecture and designer patterns

- Domain-Driven Design (DDD): Use the DDD pattern to structure and organize the code, ensuring a solid and modular architecture.

- Clean Architecture: Organize the application following the principles of Clean Architecture, separating the layers clearly: Business Entities, Use Cases, Controllers, etc.
- SOLID: Apply the SOLID principles (Single Responsibility Principle, Open/Closed Principle, Liskov Substitution Principle, Interface Segregation Principle, Dependency Inversion Principle) to promote robust and flexible code design.
- CQS (Command Query Separation): Separate read operations (queries) from write operations (commands) to improve code clarity and maintainability.

## TypeScript application development (Core) by modules

- Categories;

- Cast Member;
- Genre;
- Video.
  <br />

## Integration with RabbitMQ, Keycloak, Logs and Video Encoder

### Technologies used:

- RabbitMQ: Implement integration with RabbitMQ for asynchronous communication.

- Keycloak: Integrate Keycloak for identity management and authentication.
- Logs: Implement logs for monitoring and tracking important events.
- Video Encoder: Integrate a video encoder for video processing and optimization.

## CI (Continuous Integration)

### Technologies used:

- GitHub Actions: Setting up workflows for continuous integration.

- Dockerfile for Production: Create a Dockerfile optimized for production. -->
