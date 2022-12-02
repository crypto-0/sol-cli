<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">SOL-CLI</h3>

  <p align="center">
    An awesome Application to download movies or shows !
    <br />
    <a href="#demo">View Demo</a>
    ·
    <a href="https://github.com/crypto-0/sol-cli/issues">Report Bug</a>
    ·
    <a href="https://github.com/crypto-0/sol-cli/pulls">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is movies or tv show downloader Application that will scrape solarmovie.pe and download movies and tv shows

Here's why I took on this challenge:
* learn how to use the lowest level scrapping library on python which is lxml
* learn how to reverse enginner websites that have obscure javascript and trace network calls
* learn how to properly split my programs into multiple python packages and also follow a proper folder structure

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* python3
* pip

### Installation
```sh
$ git clone https://github.com/crypto-0/sol-cli.git
$ cd sol-cli
$ pip install -r requirements.txt
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
```sh
Usage: runner.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download  download a movie or show by query
  search    Search for a movie or show.
```
### download/search
These commands are the main set of commands in this application which all scrape solarmovie.pe
* The **download** option will download movie or tv shows episodes to your local machine
* The **search** option will send a search query for a movie or tv show and show up to 10 found matches
### h / --help argument
This argument is used to get help if lost or don't know what to do and will exist the application after

### -i / --index argument
This argument is used by download to automatically select the search result

### --s / --seaseon
This argument is used by download to automatically select the provided season if it is a tv show and is within range of number of seasons

### --q / --quality
This argument is used by download to automatically try to download the provided quality if it exist

### --d / --dir
This argument is used by download to download movies or tv shows episodes to that given location
### --e / --episode_ranges
This argument is used by download to automatically select the provided episodes range if it is a tv show and is within range of number of episodes
* 1 will be treated as a singular range from 1 to 1.
* 1-2 will be treated as a range from 1 to 2.
* 1-2,6-9 will be treated as two different checks. The first check will be from 1 to 2, the second from 6 to 9.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Demo
<img src="sol-cli.gif" />
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


