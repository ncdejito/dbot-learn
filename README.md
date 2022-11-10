# dbot-learn
Turning robots into couriers.
[Design doc](https://docs.google.com/document/d/15c91RNcq1T3N0ISpP4KQvbZ_NOrFok91Wy4N75wZA7Y/edit?usp=sharing)
## Usage
Input pickup and dropoff location with API call below, then watch it appear at client http://172.27.131.157:8501/
```bash
http://127.0.0.1:8000//order/pickup={pickup_lon},{pickup_lat};dropoff={dropoff_lon},{dropoff_lat};
```

![](assets/demo.gif)


### :dart: Features

- Order taking via API
- Dispatching with logs
- Frontend for monitoring movement



### :camera: Traits

 - Resilient
 - Scalable
 - Cost-aware

 
### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
    <li><a href="https://www.rabbitmq.com/">RabbitMQ (WIP)</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://redis.io/">Redis (WIP)</a></li>
  </ul>
</details>

<details>
<summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker (WIP)</a></li>
    <li><a href="https://www.docker.com/">Kubernetes (WIP)</a></li>
    <li><a href="https://www.docker.com/">Terraform (WIP)</a></li>
  </ul>
</details>


## 	:toolbox: Getting Started


### :bangbang: Prerequisites

This project uses poetry as package manager

```bash
 pip install poetry
```


### :gear: Installation

Install project with poetry

```bash
  cd dbot-learn
  poetry install
```
   

### :test_tube: Running Tests

To run tests, run the following command

```bash
  pytest
```

### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/ncdejito/dbot-learn.git
```

Go to the project directory

```bash
  cd dbot-learn
```

Install dependencies

```bash
  poetry shell
```

Start the server

```bash
  make run_api
```

Start the client

```bash
  make run_client
```




## :compass: Roadmap

* [x] Minimum working example
* [ ] Microservices setup