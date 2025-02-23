<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://cdn.freebiesupply.com/logos/large/2x/slack-logo-icon.png" alt="Logo" width="80" height="80">
    <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/deepseek-logo-icon.png" alt="Logo" width="80" height="80">
    <img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/ollama.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Slack Chatbot Powered by Deepseek R1 with Ollama API</h3>

  <p align="center">
    Send and edit auto-generated responses in Slack channels.
    <br />
    <a href="https://github.com/Kevdawg1/slack-chatbot-deepseek"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Kevdawg1/slack-chatbot-deepseek">View Demo</a>
    &middot;
    <a href="https://github.com/Kevdawg1/slack-chatbot-deepseek/issues/new?template=bug_report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Kevdawg1/slack-chatbot-deepseek/issues/new?template=feature_request.md">Request Feature</a>
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to showcase how simple it is to implement and deploy a DeepSeek R1 model using Ollama. This model is applied to a auto-responder on behalf of the user in Slack channels. The chatbot is designed to read historical messages, identify the latest topic and provide a short response suggestion. 

There are two ways to use this chatbot: 
1. **Auto-responder**: Automatically respond to channel messages in a thread. Triggered by new messages with a cooldown of 10 minutes to allow for more context to be built by peers in the channel. 
2. **Modal Mode**: The chatbot can be triggered by using a custom message shortcut. This will open a modal with a generated response and an input field that will allow the user to enter further context or perspective on the matter which will be used to regenerate the response. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Python][Python]][Python]
* [![Conda][Conda]][Conda]
* Ngrok
* Ollama

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python
  ```sh
  python -m pip install --upgrade pip
  ```
* Ollama - Linux
  ```sh
  curl -fsSL https://ollama.com/install.sh | sh
  ```
* Ollama - macOS and Windows: https://ollama.com/download
* Slack: https://slack.com/intl/en-gb/downloads
* Slack API: https://api.slack.com/apps

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/Kevdawg1/slack-chatbot-deepseek.git
   ```
2. Create virtual environment
   ```sh
   conda create -p venv python==3.11
   ```
3. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables in a .env file
   ```
   SLACK_BOT_TOKEN="xoxp-********"
   SLACK_SIGNING_SECRET="********"
   DEEPSEEK_API_URL="http://localhost:11434/api/chat"
   BOT_USER_ID="U0*******"
   CHANNEL_ID="C0*******""
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

### Slack App Configuration

Before you get started with using this project, you will need to set up the following Slack components: 

1. Slack User Account: Set up at least one but you can use multiple for distinct interactions
2. Slack Workspace: Either setup a new workspace or use an existing one. 
3. Slack Channel: Create a **public** Slack channel in your Slack Workspace. Preferably start with a test channel with carefully selected members.
4. Slack API App: Create a Slack API App https://api.slack.com/apps

### Slack API App Configurations

#### OAuth Access Tokens

When you have created your Slack API App, you will need to give it some permissions to read and write messages to your Slack channel.

1. Navigate to the `OAuth & Permissions` section in the menu sidebar.
2. Add the following scopes to the User Token Scopes: 
    * `channels:history`
    * `channels:read`
    * `chats:write`
    * `commands`
    * `groups:history`
    * `im:history`
    * `im:write`
    * `users:read`
    * `users:read.email`

#### Slack Event Subscriptions

The next step involves configuring the settings used to send webhooks to your app's endpoint. These messages will be used to trigger your app's functions. 

1. Navigate to the `Event Subscriptions` section in the menu sidebar.
2. Enable Events ✅
3. Add and verify your ngrok endpoint as the `Request URL`.
    * Ensure that ngrok is running in a terminal (see <a href="#ngrok-server-hosting" >Ngrok Server Hosting</a>).
    * Your endpoint should look like: https://65fb-175-144-190-131.ngrok-free.app/slack/events
4. In `Subscribe to bot events` and `Subscribe to event on behalf of users`, add the `message:channels` event. 
5. Save Changes

#### (FOR MODAL MODE ONLY) Interactivity & Shortcuts

This is an optional step if you want to use the Modal Mode of the app. 

1. Navigate to the `Interactivity & Shortcuts` section in the menu sidebar.
2. Add and verify your ngrok endpoint as the `Request URL`.
    * Ensure that ngrok is running in a terminal.
    * Your endpoint should look like: https://65fb-175-144-190-131.ngrok-free.app/slack/events
3. Under `Shortcuts`, Click `Create New Shortcut`
    * Set the `location` to `Messages`
    * Name your shortcut. e.g. "Generate Response with Deepseek".
    * Set the `callback_id` to `add_context`.
4. Save Changes

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Python Application

```sh
  python app.py
```

### Ngrok Server Hosting

Set up your ngrok endpoint. This will expose a public endpoint (e.g. https://65fb-175-144-190-131.ngrok-free.app) and forward requests to your Python app running locally (http://localhost:3000).

```
  ngrok 3000
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

README.md template from https://github.com/othneildrew/Best-README-Template/blob/main/README.md 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/kevin-kam-eng
[Python]: https://img.shields.io/pypi/pyversions/slack_bolt?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/downloads/
[Conda]: https://img.shields.io/conda/d/conda-forge/python?style=for-the-badge&logo=anaconda
[Conda-url]: https://docs.anaconda.com/anaconda/install/
