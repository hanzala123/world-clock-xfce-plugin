<div id="top"></div>
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

<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">World Clock Plugin For XFCE</h3>

  <p align="center">
    A World Clock Plugin for XFCE Written in Python
    <br />
    <a href="https://github.com/hanzala123/world-clock-xfce-plugin"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hanzala123/world-clock-xfce-plugin/issues">Report Bug</a>
    ·
    <a href="https://github.com/hanzala123/world-clock-xfce-plugin/issues">Request Feature</a>
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
        <li><a href="#updating">Updating</a></li>
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

![World-Clock-Plugin][product-screenshot]

GTK Theme: Orchis-dark, Icon Theme: Papirus

After switching to XFCE I was amazed at the speed of everything. But one thing that I really miss from KDE or GNOME is the World Clock. I have never worked with GTK or any such Toolkit ever. So with my very very minimal knowledge of GTK I made a fix for it using the [AppIndicator](https://github.com/hanzala123/world-clock-appindicator). But That was taking up precious space in my vertical panel. So I decided to make a plugin from it. But making an XFCE Planel Plugin using Python (My Speciality) is very poorly if not at all documented. But finally I found a project on gitlab and used that as a Base. Much thanks to the creator of that project.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [sample-python-plugin](https://gitlab.xfce.org/itsManjeet/sample-python-plugin/)
* [PyTZ](https://pypi.org/project/pytz/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

I am on EndeavourOS and most of the required libraries were preinstalled. I had to install pip, meson and ninja
  ```sh
  sudo pacman -Sy python-pip meson ninja
  ```
Then install the required the Python Packages.
  ```sh
  pip3 install -r requirements.txt
  ```

Then You can test it by running this command from the project directory.
  ```sh
  python3 run.py
  ```
Running it first time will automatically create the config files at 
  ```~/.config/world_clock_plugin@hanzala123/```

The configuration file is called config.json and as the name suggests the file is in JSON format. It has three keys ```format```, ```allocation``` and ```timezones```.

The ```format``` is the format in which the time will be displayed. The convention is the one used for formating string in Python's DateTime Module. More About that [here](https://www.programiz.com/python-programming/datetime/strftime).

The ```allocation``` is the place where the calendar will appear. By default it set to ```auto```. Which shows the Calendar next to the plugin when clicked. It can also be set to show at a specific location on the screen. The value should be a list to show the X and Y coordinates of the place the calendar will appear. Something like this
  ```json
  "allocation": [0, 0]
  ```
The above will show the calendar in the top left corner of the screen (or as close as possible to that).

The ```timezones``` sets the timezones that will appear. By default it's set to Europe/Amsterdam. This is basically as list of lists. The First element of of each child list the generic name of the timezone and the other element is the name that the user wants to be displayed as the name of that timezone. When the program is run for the first time it will also create a file called ```available_timezones.txt``` in the config directory. This will help you find the generic name of the timezone you wish to add. If I want to Dhaka to the plugin alongside Amsterdam it will look like this.
  ```json
    "timezones": [
    ["Europe/Amsterdam", "Amsterdam"],
    ["Asia/Dhaka", "Dhaka"]
  ]
  ```

PS: It is recommended that you check if the configraution is working or not by running ```python3 run.py```. Also for efficiency the config is kept in memory. So any changes will not take effect until the the app is restarted. Or if it is already added to the panel then you need to restart the panel by doing
  ```sh
  xfce4-panel -r
  ```

### Installation

If you see it working when you run ```python3 run.py``` then you can install it by doing
   ```sh
   bash install.sh
   ```
Though in My case The Plugin kept removing it self and after following the [Panel Debug Docs](https://docs.xfce.org/xfce/xfce4-panel/debugging/) I figured the problem was the line 27 in ```src/plugin.c``` This did not match the python version that was installed on my system which I checked using this 
   ```sh
   python3 --version
   ```
So I replaced 
  ```
  dlopen("libpython3.9.so", RTLD_LAZY | RTLD_GLOBAL);
  ```
with
  ```
  dlopen("libpython3.10.so", RTLD_LAZY | RTLD_GLOBAL);
  ```
And then installed it again by running 
   ```sh
   bash install.sh
   ```
And it worked perfectly. Now due to my lack of knowledge in C I could not figure out a better fix for this. If anyone can then feel free to fork it and then create a Pull Request.
<p align="right">(<a href="#top">back to top</a>)</p>

### Updating

Updating is pretty simple. You just need to go to the project directory and do
   ```sh
   git pull
   ```
This will sync the changes from the github repo to your local machine. It is recommended that you run 
   ```sh
   python3 run.py
   ```
Just to make sure everything is working. Then you run the install script
   ```sh
   bash install.sh
   ```
This will update the plugin. Sometimes it might require restarting the panel (```xfce4-panel -r```) to see the changes take effect.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

After Following the previous steps it's pretty simple to use it like any other panel plugin.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Make GUI for Configuration.

See the [open issues](https://github.com/hanzala123/world-clock-xfce-plugin/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

My Email - hanzalarushnan@gmail.com

Project Link: [https://github.com/hanzala123/world-clock-xfce-plugin](https://github.com/hanzala123/world-clock-xfce-plugin)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [sample-python-plugin](https://gitlab.xfce.org/itsManjeet/sample-python-plugin/)
* [PyTZ](https://pypi.org/project/pytz/)

<p align="right">(<a href="#top">back to top</a>)</p>


[product-screenshot]: screenshots/main_gif.gif
