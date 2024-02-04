<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![codecov](https://codecov.io/gh/rkanapka/darbas24/graph/badge.svg?token=XN37MKVTU5)](https://codecov.io/gh/rkanapka/darbas24)<br/>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]


<br />
<div align="center">
  <a href="https://github.com/devKanapka/darbas24">
    <img src="static/images/logo.png" alt="Logo">
  </a>

  <h3 align="center">Lithuanian Job Offers Scraper</h3>

  <p align="center">
Welcome to the Lithuanian Job Offers Scraper project!<br/>
This open-source tool is designed to simplify the job search process by aggregating job offers from various Lithuanian job offer sites.<br/>
Built using the Python programming language and the Django web framework, this project aims to provide a centralized platform for job seekers to easily explore and filter job opportunities from multiple sources.<br/>
    <br />
    <a href="https://github.com/devKanapka/darbas24"><strong>Happy job hunting!</strong></a> 🚀
    <br />
    <br />
    <a href="https://github.com/devKanapka/darbas24">View Demo</a>
    ·
    <a href="https://github.com/devKanapka/darbas24/issues">Report Bug</a>
    ·
    <a href="https://github.com/devKanapka/darbas24/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#additional-setup">Additional Setup</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Here's why you should use this scraper:
* <b>Multi-Site Scraping</b>:</b> The scraper efficiently extracts job listings from diverse Lithuanian job offer websites, ensuring a comprehensive and up-to-date collection of opportunities.
* <b>User-Friendly Interface:</b> The Django framework powers a clean and intuitive user interface, making it easy for users to search, filter, and explore job offers based on their preferences.
* <b>Automated Updates:</b> The scraper is designed to regularly update its database, ensuring that users have access to the latest job opportunities without manual intervention.
* <b>Customizable Filters:</b> Job seekers can personalize their search criteria with customizable filters, allowing them to narrow down results based on location, industry, job type, and more.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Django][Djangoproject.com]][Django-url]
* [![Celery][Docs.celeryq.dev.com]][Celery-url]
* [![Rabbitmq][Rabbitmq.com]][Rabbitmq-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![Docker][Docker.com]][Docker-url]
* [![Postgreql][Postgresql.org]][Postgresql-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get started with the Lithuanian Job Offers Scraper, follow these steps:

### Prerequisites

* docker & docker compose:<br/>
[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Installation

Project setup:

1. Clone the repo:
   ```bash
   git clone https://github.com/devKanapka/darbas24.git
   ```
2. In project root directory create `.env` file. Env sample:
   ```env
    POSTGRES_DB=darbas24
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=mypassword

    RMQ_USER=admin
    RMQ_PASS=mypass
   ```
3. Build docker image:
   ```bash
    docker compose up --build
   ```
4. Make new migrations and migrate schema to DB:
   ```bash
    docker exec -it darbas24-web-1 python manage.py makemigrations
    docker exec -it darbas24-web-1 python manage.py migrate
   ```
5. Load data to DB:
   ```bash
    docker exec -it darbas24-web-1 python manage.py loaddata cities
    docker exec -it darbas24-web-1 python manage.py loaddata categories
   ```
6. Change RabbitMQ's admin password according to .env file:
   ```bash
      docker exec -it darbas24-rabbit-1 rabbitmqctl change_password admin mypass
   ```
7. Access the Application:<br/>
Open your web browser and navigate to `http://localhost:8000` to explore the job offers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Additional setup

### Create Django site adminstrator
1. Run command and fill required information:
   ```bash
    docker exec -it darbas24-web-1 python manage.py createsuperuser
   ```
2. Login to django site panel:<br/>
[ http://localhost:8000/admin/login](http://localhost:8000/admin/login)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Testing
### Unit tests & coverage
1. Run unit tests and generate coverage report:
   ```bash
    docker exec -it darbas24-web-1 coverage run --source='.' manage.py test
    docker exec -it darbas24-web-1 coverage report
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Scheduled jobs

### Run scheduled jobs manually with Celery
1. Run command and wait for job to start:
   ```bash
    docker exec -it darbas24-web-1 celery -A darbas24 worker -B -l INFO
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create.<br/>
Any contributions you make are **greatly appreciated**.<br/>

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingNewFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingNewFeature'`)
4. Push to the Branch (`git push origin feature/AmazingNewFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

[![Facebook][facebook-shield]][facebook-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Instagram][instagram-shield]][instagram-url]

Rimvydas Kanapka - [kanapka.rimvydas@gmail.com](MAILTO:kanapka.rimvydas@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/devKanapka/darbas24.svg?style=for-the-badge
[contributors-url]: https://github.com/devKanapka/darbas24/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/devKanapka/darbas24.svg?style=for-the-badge
[forks-url]: https://github.com/devKanapka/darbas24/network/members
[stars-shield]: https://img.shields.io/github/stars/devKanapka/darbas24.svg?style=for-the-badge
[stars-url]: https://github.com/devKanapka/darbas24/stargazers
[issues-shield]: https://img.shields.io/github/issues/devKanapka/darbas24.svg?style=for-the-badge
[issues-url]: https://github.com/devKanapka/darbas24/issues
<!-- Social media -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-007AB5.svg?style=for-the-badge&logo=linkedin
[linkedin-url]: https://www.linkedin.com/in/rimvydas-kanapka
[facebook-shield]: https://img.shields.io/badge/-facebook-0866FF.svg?style=for-the-badge&logo=facebook
[facebook-url]: https://www.facebook.com/kanapka.rimvydas
[instagram-shield]: https://img.shields.io/badge/-instagram-C5346E.svg?style=for-the-badge&logo=instagram&logoColor=white
[instagram-url]: https://www.instagram.com/rimvydaskanapka
<!-- Tech stack -->
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Djangoproject.com]: https://img.shields.io/badge/Django-0F3E2E?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com
[Rabbitmq.com]: https://img.shields.io/badge/rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white
[Rabbitmq-url]: https://rabbitmq.com
[Docs.celeryq.dev.com]: https://img.shields.io/badge/celery-B6DE64?style=for-the-badge&logo=celery&logoColor=white
[Celery-url]: https://docs.celeryq.dev
[Docker.com]: https://img.shields.io/badge/docker-1D63ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com
[Postgresql.org]: https://img.shields.io/badge/postgresql-336791?style=for-the-badge&logo=postgresql&logoColor=white
[Postgresql-url]: https://www.postgresql.org
