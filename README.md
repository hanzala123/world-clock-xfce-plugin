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
        <li><a href="#configuration">Configuration</a></li>
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

GTK Theme: Orchis-dark, Icon Theme: Colloid

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
If you are on Ubuntu or an Ubuntu Based Distro then you can install the dependencies with this
  ```sh
  sudo apt-get libxfce4panel-2.0
  sudo apt-get install python-gi-dev
  sudo apt-get install libgtk-3-dev
  sudo apt-get install meson ninja
  ```
Then install the required the Python Packages.
  ```sh
  pip3 install -r requirements.txt
  ```

Then You can test it by running this command from the project directory.
  ```sh
  python3 run.py
  ```

### Installation

If you see it working when you run ```python3 run.py``` then you can install it by doing
   ```sh
   bash install.sh
   ```

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


### Configuration

Running it first time will automatically create the config files at 
  ```~/.config/world_clock_plugin@hanzala123/```

You can open the configuration window for this the same way as other plugins.

#### Main Time Format
This is the format in which the time will be shown in the panel. The convention is the one used for formating string in Python's DateTime Module. More about that [here](https://www.programiz.com/python-programming/datetime/strftime).

#### Date Format For World Clocks
This the the format in which the date will be displayed on the world clocks. The same convention is used here as well.

#### Calendar Window Allocation
This is the place where the calendar/world clock window will appear. By default it set to ```auto```. Which shows the Calendar next to the plugin when clicked. It can also be set to show at a specific location on the screen. The value should be comma separated X and Y coordinates of the place the calendar will appear. Something like this ```0, 0``` will show the calendar in the top left corner of the screen (or as close as possible to that).

#### Existing Timezone(s) / Delete a Timezone
Here all the currently configured timezones will appear. To delete a timezone click on the timezone and once it is selected click on the 'Delete' button.

#### Add New Timezone
You can use this section to add new timezones. To do so first select the area from the left most dropdown selector. Then select the region from the second left most dropdown selector. Finally click on the 'Add' button to add the selected timezone.


PS: YOU MUST CLICK ON THE 'Apply' BUTTON FOR THE CHANGES TO BE APPLIED AND SAVED.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After Following the previous steps it's pretty simple to use it like any other panel plugin.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Make GUI for Configuration.

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

Project Link: [https://github.com/hanzala123/world-clock-xfce-plugin](https://github.com/hanzala123/world-clock-xfce-plugin)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [sample-python-plugin](https://gitlab.xfce.org/itsManjeet/sample-python-plugin/)
* [PyTZ](https://pypi.org/project/pytz/)

<p align="right">(<a href="#top">back to top</a>)</p>


[product-screenshot]: screenshots/main_gif.gif
