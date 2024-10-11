# Autoruns: Disable startup services on Kodi
[![Kodi versions](https://img.shields.io/badge/kodi%20versions-19--20--21-blue)](https://kodi.tv/ "Kodi add-on for Kodi 19, 20 and 21")
[![GitHub release](https://img.shields.io/github/release/bittor7x0/kodi.script.autoruns.svg)](https://github.com/bittor7x0/kodi.script.autoruns/releases/latest "Download latest release")
[![Kodi Addon checks](https://img.shields.io/github/actions/workflow/status/bittor7x0/kodi.script.autoruns/addon-check.yml?branch=main&label=CI)](https://github.com/bittor7x0/kodi.script.autoruns/actions/workflows/addon-check.yml "Kodi Addon checks")
[![Python Code Scans](https://img.shields.io/github/actions/workflow/status/bittor7x0/kodi.script.autoruns/code-scan.yml?branch=main&label=code%20scan)](https://github.com/bittor7x0/kodi.script.autoruns/actions/workflows/code-scan.yml "Python Code Scans")
[![Coverity Scan Status](https://img.shields.io/coverity/scan/29705.svg)](https://scan.coverity.com/projects/bittor7x0-kodi-script-autoruns "View Coverity Scan Status")
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt "Read License GPL v3")

![](https://github.com/bittor7x0/kodi.script.autoruns/blob/main/resources/icon.png)

## Overview
Some [Kodi](https://github.com/xbmc/xbmc) add-ons are [service add-ons](https://kodi.wiki/view/Service_add-ons), which will be automatically started when Kodi starts.

Kodi does not allow you to disable these services to use the add-ons with their services disabled and if you have a lot of service add-ons installed, Kodi startup will be very slow because they will be using system resources (CPU, memory, network, hard disk, etc.) and some service add-ons will be using them while Kodi is running.

This Kodi add-on lists the services add-ons and allows you to disable them (and enable them if you had disabled them before), improving Kodi internal speed because the add-ons with their services disabled will only run when you access them.

To achieve this, Autoruns add-on modifies the **addon.xml** file of service add-ons commenting the **xbmc.service** extension point, so you must restart Kodi after disabling them and when they are updated you will have to disable them again because the **addon.xml** file will have been restored to its original state.

Most add-ons work properly with their services disabled, but you should be aware that some add-ons use their services for some functionalities, for example, [plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube) uses it to play MPEG-DASH VODS.

## Installation
* [Download the latest release](https://github.com/bittor7x0/kodi.script.autoruns/releases/latest) (`script.autoruns-<VERSION>.zip`)
* Copy the zip file to your Kodi system
* Open Kodi, go to `System -> Add-ons -> Install from zip file`
* Select the file `script.autoruns-<VERSION>.zip`

## History
In 2013, **fightnight** created this add-on replacing the **xbmc.service** extension point with the fake variable **xbmc.pass** in the **addon.xml** file of the service add-ons you want to disable. **fightnight** updated the add-on to 2015.

This dirty hack no longer works with Kodi v19 Matrix, because it parses the **addon.xml** file and if this file isn't a valid XML (with **xbmc.pass** isn't valid) the add-on is disabled and it cannot be enabled until the **addon.xml** file is valid (modifying it manually or reinstalling the add-on).

So in 2021 and because the **fightnight** add-on was abandoned, **Jon Bovi** updated the add-on to disable the services commenting the line **<extension ... xbmc.service ...>** in the **addon.xml** file.

This new approach does not work if the add-on has the **xbmc.service** extension point in multiple lines (for example [KCleaner](https://forum.kodi.tv/showthread.php?tid=307919)) because it generates an invalid XML file.

Because I did not find this add-on on GitHub and cannot contact these authors to fix it, in 2022, I released this add-on based on **fightnight**'s latest version, but now the **xbmc.service** extension point is commented parsing the **addon.xml** file, this way, it works with all the add-ons because the XML is always valid.

This version is compatible with Kodi v19 Matrix and Kodi v20 Nexus and I will update the add-on to work with future Kodi versions and accept pull requests with improvements.

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt "Read License GPL v3")\
Autoruns add-on is **[GPL v3 licensed](LICENSE.txt "Read License GPL v3")**.\
You may use, distribute and copy it under the license terms.
