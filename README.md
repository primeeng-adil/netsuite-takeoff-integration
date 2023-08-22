# NetSuite Takeoff Integrator
Welcome to the NetSuite Takeoff Integrator repository! The software is intended to be used by Prime Engineering Business Team to 
automatically generate proposals on NetSuite. The following section details on the installation process:

## Installation
To install the integrator:
1. Get the latest installer release from 

## Usage
Using the integrator is quite simple. The only requirement is to fill in all the mandatory fields, that is all the fields
without the _'Not Required'_ label. To avoid running with incomplete inputs, the program has been designed to throw errors
if one of the mandatory field is left blank.

### Guide to First Time Running the Program
When launching the program for the first time, the following points are noteworthy:
1. Ensure you have the appropriate chromedriver installed and correctly configured in your environment variables.
2. Prior to clicking the 'Run' button, evaluate the browser's functionality by accessing Edit > Open Browser through the application's menu bar.
3. Test logging into NetSuite using the opened chromedriver browser. During login, address any security questions and select the 'Remember Me' checkbox. This enables NetSuite to remember the chromedriver browser for future sessions.
4. While the aforementioned steps usually obviate the need for Security Questions, there might be cases where NetSuite struggles to remember a user. In such scenarios, it's recommended to enter security questions and answers in their designated input fields.
5. Once you have added all the inputs, it is always a good idea to save the login and details by clicking 'Save Login' and 'Save Details' in the File menu in the menu bar at the top.

### Saving Inputs
You can easily store your login information and other details by using the 'Save Login/Details As...' or 'Save Login/Details' options. These two options differ mainly in terms of where your information will be stored.
- **Save Login/Details:** This option automatically saves your data to the default location: `C:\Users\<username>\Documents\Netsuite Inputs`. You can modify this default storage location by accessing the 'Settings' through `File > Settings` in the menu bar.
- **Save Login/Details As...:** With this option, you get to choose the specific folder where you want to save your information. A dialog will prompt you to select the desired location for saving.

**Remember:**
- Use the 'Save Login/Details' option alongside 'Load Login/Details.'
- Use the 'Save Login/Details As...' option in conjunction with the 'Load Login/Details As...' choice from the File menu.

> _Note: Do NOT save your login information in a public drive. Always choose to save it locally on your machine. The default location is always your local Documents folder._

### Consts File
Included within the program is a file named `consts.csv`, found at `<install_path>/data/consts.csv`, which houses vital runtime information utilized by the application. The `consts.csv` file showcases a table of adjustable parameters, each of which holds significance during program execution. Among these parameters, you will encounter the **NETSUITE URL** entry, important for transitioning between sandbox and production environments.
Noteworthy is the fact that upon modifying the consts file, certain OS settings may not allow you to save the changes directly within the original file. In such instances, consider the following steps:
1. Create a duplicate of the file and save it in another location. Ensure that this copy bears the exact name as the original, i.e., `consts.csv`.
2. Subsequently, substitute the original `consts.csv` with the modified duplicate, effectively replacing the original file with the modified version.

This process guarantees that the revised `consts.csv` is successfully integrated into the program's operation.

### Switching between Sandbox and Production Environments

To transition between the sandbox and production environments, follow these steps to modify the 'NETSUITE URL' parameter in consts.csv. By default, the URL is set for the sandbox environment. To make the switch to the production environment, simply eliminate the `-sb1` suffix from the URL. This transformation results in a URL resembling:

`https://6516658.app.netsuite.com/app/common/custom/custrecordentry.nl?rectype=207`

And to switch back to sandbox environment, reinstating the `-sb1` suffix in the NETSUITE URL accomplishes the switch effectively. For example:

`https://6516658-sb1.app.netsuite.com/app/common/custom/custrecordentry.nl?rectype=207`

### Chromedriver
Chromedriver is essentially the workhorse of the NetSuite Takeoff Integrator. It is basically a modified version of the original Chrome browser
created for automation and testing by developers. 

> _Note: During the runtime of the application, it is important to NOT interact with the Chromedriver browser. However, you may continue doing other
> stuff on your machine and that includes your home browser._

### Chrome Settings


### Name and Customer Fields
The 'Name' and 'Customer' are the two dropdown 

## Debugging

First and foremost, it is always a good idea to restart the program if it crashes before running it again. Make sure you close
all the associated program windows to ensure a complete termination. 