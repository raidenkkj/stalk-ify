# ![Stalk-ify](https://github.com/raidenkkj/stalk-ify/blob/main/images/header.png?raw=true)

<p align="center">
    <i>A tool that uses the instaloader library to increase your stalking level.</i>
</p>

<p align="center">
  <a href="https://github.com/raidenkkj/stalk-ify/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/raidenkkj/stalk-ify?style=flat-square">
  </a>
  <a href="https://github.com/raidenkkj/stalk-ify/network">
    <img alt="Forks" src="https://img.shields.io/github/forks/raidenkkj/stalk-ify?style=flat-square">
  </a>
  <a href="https://github.com/raidenkkj/stalk-ify/stargazers">
    <img alt="Stars" src="https://img.shields.io/github/stars/raidenkkj/stalk-ify?style=flat-square">
  </a>
  <a href="https://github.com/raidenkkj/stalk-ify/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/raidenkkj/stalk-ify?style=flat-square">
  </a>
</p>

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## About

**Stalk-ify** is a tool that uses the **Instaloader** library to facilitate the process of collecting information from Instagram accounts. The goal is to help developers and curious people automate and optimize their searches by offering an easy-to-use interface for manipulating Instagram profile data.

---

## Features

- Collection of public information from Instagram profiles.
- Integration with **Instaloader** for automation.
- Support for Python 3.8+.
- Easy to configure and use via command line.
- Customization of search parameters.

---

## Dependencies

- Python 3.8 ou higher
- Git
- Colorama
- Instaloader
- Configparser

## Installation

1. Clone the repository: 
   ```bash
   git clone https://github.com/raidenkkj/stalk-ify.git
   ```
2. Go to the repository:
   ```bash
   cd stalk-ify
   ```

3. Create a virtual environment (optional, but recommended):

Linux/macOS/Termux:
   ```bash
   python -m venv venv
   ```
Activate:
   ```bash
   source venv/bin/activate
   ```
Activate (windows):
   ```bash
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run via command line:

After installation, inside the cloned directory, you can use the command below to run **Stalk-ify:**

```bash
stalkify --login
```

Options:

> -h, --help: Displays help and exits.

> -a, --analysis TARGET_USERNAME: Analyzes the target user to collect information from Instagram.

> -g, --get_info TARGET_USERNAME: Collects information from the target user's Instagram profile. (in development)

> -c, --compare: Compares previously performed analyses.


### Examples

To analyze a user on Instagram:

```bash
stalkify --analysis raidenkkj
```

Or to collect detailed information:

```bash
stalkify --get_info raidenkkj
```

If you want to compare previous analyses:

```bash
stalkify --compare
```

---

## License

This project is licensed under the GPL-3.0 license. See the LICENSE file for more details.

---

## Contributing

Contributions are always welcome! If you have any suggestions for improvement, feel free to create an issue or open a pull request.

1. Fork the project


2. Create a new branch
   ```bash
   git checkout -b feature/YourFeature
   ```


3. Commit your changes
   ```bash
   git commit -m 'Add new functionality'
   ```

4. Push to the branch
   ```bash
   git push origin feature/YourFeature
   ```


5. Open a pull request

---

## Contact

Author: [Raiden Ishigami](https://t.me/raidenkkj)

Email: contact.raidenishi69@gmail.com

GitHub: [raidenkkj](https://github.com/raidenkkj)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/raidenkkj">Raiden Ishigami</a>
</p>
