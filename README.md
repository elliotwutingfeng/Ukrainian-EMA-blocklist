# Ukrainian Interbank Payment Systems Member Association "EMA" blocklist

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)
[![scraper](https://img.shields.io/github/actions/workflow/status/elliotwutingfeng/Ukrainian-EMA-blocklist/scraper.yml?branch=main&label=SCRAPER&style=for-the-badge)](https://github.com/elliotwutingfeng/Ukrainian-EMA-blocklist/actions/workflows/scraper.yml)
![Total Blocklist URLs](https://tokei-rs.onrender.com/b1/github/elliotwutingfeng/Ukrainian-EMA-blocklist?label=Total%20Blocklist%20URLS&style=for-the-badge)

Machine-readable `.txt` blocklist of fraudulent URLs and IP Addresses from the [Ukrainian Interbank Payment Systems Member Association "EMA"](https://www.ema.com.ua) website, updated once a day.

The URLs and IP Addresses in this blocklist are compiled by the **Ukrainian Interbank Payment Systems Member Association "EMA"**.

**Disclaimer:** _This project is not sponsored, endorsed, or otherwise affiliated with the Ukrainian Interbank Payment Systems Member Association "EMA"._

## Blocklist download

| File | Download |
|:-:|:-:|
| urls.txt | [:floppy_disk:](urls.txt?raw=true) |
| urls-ABP.txt | [:floppy_disk:](urls-ABP.txt?raw=true) |
| urls-UBO.txt | [:floppy_disk:](urls-UBO.txt?raw=true) |
| urls-pihole.txt | [:floppy_disk:](urls-pihole.txt?raw=true) |
| ips.txt | [:floppy_disk:](ips.txt?raw=true) |

## Requirements

- Python >= 3.11

## Setup instructions

`git clone` and `cd` into the project directory, then run the following

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 scraper.py
```

## Libraries/Frameworks used

- [tldextract](https://github.com/john-kurkowski/tldextract)

&nbsp;

<sup>These files are provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, arising from, out of or in connection with the files or the use of the files.</sup>

<sub>Any and all trademarks are the property of their respective owners.</sub>
