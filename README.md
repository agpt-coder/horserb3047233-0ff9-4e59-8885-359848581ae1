---
date: 2024-04-12T18:30:37.664339
author: AutoGPT <info@agpt.co>
---

# horser

Based on the details provided in our conversation and the research conducted, the final product is a web application designed to fetch and display a random xkcd comic every time it is called. The application utilizes GPT-4-vision to provide detailed explanations of the comics, which often delve into complex or scientific principles that are represented in a humorous and accessible manner. Specifically, the application is built with the following technology stack:

- **Programming Language**: Python, chosen for its widespread use in both web development and machine learning, making it the perfect fit for integrating the GPT-4-vision API for comic explanations.
- **API Framework**: FastAPI, selected for its high performance and easy-to-use features for building APIs. FastAPI's asynchronous support is ideal for handling requests to the xkcd API and GPT-4-vision API efficiently.
- **Database**: PostgreSQL, used for storing metadata about the comics and user preferences if needed. Its reliability and powerful features support complex queries efficiently.
- **ORM**: Prisma, to facilitate easy and secure interactions with the database using Python. Prisma provides type-safe database access, simplifying data manipulation and queries.

The application flow is as follows:
1. The user accesses the web application.
2. The application calls the xkcd API to fetch a random comic by generating a random number within the range of available comics and using the specific URL 'https://xkcd.com/[random_number]/info.0.json'.
3. The comic, along with its image URL, title, and number, is displayed to the user.
4. To provide an explanation, the application sends the comic's image URL to the GPT-4-vision API, along with a prompt to generate a detailed explanation of the comic.
5. The GPT-4-vision API processes the image and returns a comprehensive explanation, which is then displayed to the user beneath the comic.

This tool addresses the user's requirements for a simple, intuitive interface that is accessible cloud-based for scalability and ease of access. It also meets the need for detailed explanations of xkcd comics, enhancing the appreciation and understanding of each piece.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'horser'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
