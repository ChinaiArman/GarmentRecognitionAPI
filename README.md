<!-- DOCUMENT HEADER -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ChinaiArman/GarmentRecognitionAPI">
    <img src="resources/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Garment Recognition API</h3>

  <p align="center">
    An API that uses computer vision and semantic textual analysis to recognize clothing items through images.
    <br />
    <a href="https://github.com/ChinaiArman/GarmentRecognitionAPI/blob/main/ui/static/swagger.yaml"><strong>Explore the docs »</strong></a>
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
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Developer Team</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

The Garment Recognition API is a RESTful API that uses computer vision and semantic textual analysis to recognize clothing items through images. The project was developed by a team of 5 students as part of BCIT's COMP 3800 course. The API leverages Azure's Dense Captioning model to generate textual descriptions of images, which are then processed by a custom-built NLP model to extract relevant information about the clothing items. The server is built using Flask and the API is documented using Swagger. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Pandas][Pandas]][Pandas-url]
* [![Flask][Flask]][Flask-url]
* [![Azure][Azure]][Azure-url]
* [![HuggingFace][HuggingFace]][HuggingFace-url]
* [![Swagger][Swagger]][Swagger-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/ChinaiArman/GarmentRecognitionAPI.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DEPLOYMENT EXAMPLES -->
## Deployment

Write deployment guide here.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/ChinaiArman/GarmentRecognitionAPI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Developer Team

Arman Chinai:

[![LinkedIn][linkedin-shield]][arman-linkedin] [![GitHub][github-shield]][arman-github]

Lex Wong:

[![LinkedIn][linkedin-shield]][lex-linkedin] [![GitHub][github-shield]][lex-github]

Natalie Yu:

Ehsan Emadi:

Collin Chan:

Project Link: [https://github.com/ChinaiArman/GarmentRecognitionAPI](https://github.com/ChinaiArman/GarmentRecognitionAPI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: resources/demo.png
[contributors-shield]: https://img.shields.io/github/contributors/chinaiarman/GarmentRecognitionAPI.svg?style=for-the-badge
[contributors-url]: https://github.com/ChinaiArman/GarmentRecognitionAPI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ChinaiArman/GarmentRecognitionAPI.svg?style=for-the-badge
[github-shield]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[forks-url]: https://github.com/ChinaiArman/GarmentRecognitionAPI/network/members
[stars-shield]: https://img.shields.io/github/stars/ChinaiArman/GarmentRecognitionAPI.svg?style=for-the-badge
[stars-url]: https://github.com/ChinaiArman/GarmentRecognitionAPI/stargazers
[issues-shield]: https://img.shields.io/github/issues/ChinaiArman/GarmentRecognitionAPI.svg?style=for-the-badge
[issues-url]: https://github.com/ChinaiArman/GarmentRecognitionAPI/issues
[license-shield]: https://img.shields.io/github/license/ChinaiArman/GarmentRecognitionAPI.svg?style=for-the-badge
[license-url]: https://github.com/ChinaiArman/GarmentRecognitionAPI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.0.x/
[Azure]: https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white
[Azure-url]: https://azure.microsoft.com/en-us/
[Pandas]: https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Swagger]: https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black
[Swagger-url]: https://swagger.io/
[HuggingFace]: https://img.shields.io/badge/Hugging%20Face-FFD000?style=for-the-badge&logo=huggingface&logoColor=black
[HuggingFace-url]: https://huggingface.co/
[arman-linkedin]: https://www.linkedin.com/in/armanchinai/
[arman-github]: https://github.com/ChinaiArman/
[lex-linkedin]: https://www.linkedin.com/in/alexandra-wong-8188a122a/
[lex-github]: https://github.com/levxxvi/