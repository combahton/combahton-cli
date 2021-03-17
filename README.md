[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Build Status][build-shield]][build-url]
[![Twitter][twitter-shield]][twitter-url]

<br />
<p align="center">
  <a href="https://github.com/combahton">
    <img src="https://avatars.githubusercontent.com/u/75513620?s=200&v=4" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">combahton CLI</h3>

  <p align="center">
    Simple CLI to interact with combahton.net Services and the API
    <br />
    <a href="https://wiki.combahton.net/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/combahton/combahton-cli/issues">Report Bug</a>
    ·
    <a href="https://github.com/combahton/combahton-cli/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
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
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

combahton-cli (formerly combahton-api-cli/cbcli) provides a simple way of interacting with combahton.net services from the command line.


### Built With

* [Python 3.9](https://www.python.org/)
* [PyInstaller](https://www.pyinstaller.org/)
* [Visual Studio Code](https://code.visualstudio.com/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
* pip
  ```sh
  python3.9 -m pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/combahton/combahton-cli.git
   ```
2. Install requirements
   ```sh
   python3.9 -m pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage

To authenticate with the API, either create an .env file with the following contents, or populate them to your OS environment.
```env
CB_AUTH_USER=<email>
CB_AUTH_SECRET=<secret>
```

Optionally, you can set the following variables:

**CB_DEFAULT_IP**: If an IP address is required as a parameter, it can be set persistently as an environment variable so that you do not need to enter it explicitly.

Please see `combahton_cli --help` for more help / details.

```
Usage: combahton [OPTIONS] COMMAND [ARGS]...

  Simple CLI Interface to interact with combahton Services

Options:
  --help  Show this message and exit.

Commands:
  antiddos  Provides access to AntiDDoS Options of combahton.net
  cloud     Provides access to cloud servers from combahton.net
  customer  Provides access to customer details from combahton.net
  ipaddr    Provides access to ip address details from combahton.net
  misc      Provides access to miscellaneous functions
```

_For more examples, please refer to the [Documentation](https://github.com/combahton/combahton-cli/wiki)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/combahton/combahton-cli/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License.



<!-- CONTACT -->
## Contact

Maurice Schmitz - [@combahton](https://twitter.com/combahton) - msc@combahton.net

Project Link: [https://github.com/combahton/combahton-cli](https://github.com/combahton/combahton-cli)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/combahton/combahton-cli.svg?style=for-the-badge
[contributors-url]: https://github.com/combahton/combahton-cli/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/combahton/combahton-cli.svg?style=for-the-badge
[forks-url]: https://github.com/combahton/combahton-cli/network/members
[stars-shield]: https://img.shields.io/github/stars/combahton/combahton-cli.svg?style=for-the-badge
[stars-url]: https://github.com/combahton/combahton-cli/stargazers
[issues-shield]: https://img.shields.io/github/issues/combahton/combahton-cli.svg?style=for-the-badge
[issues-url]: https://github.com/combahton/combahton-cli/issues
[build-shield]: https://img.shields.io/github/workflow/status/combahton/combahton-cli/PyInstaller%20Build?style=for-the-badge
[build-url]: https://github.com/combahton/combahton-cli/actions/workflows/build.yml
[twitter-shield]: https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=555
[twitter-url]: https://twitter.com/combahton