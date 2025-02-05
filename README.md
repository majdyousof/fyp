(ASSUMING WINDOWS) To start, initialise your python environment, for this project/example I've called it `myenv`:

``` Bash
py -m venv myenv
```
after that, activate your environment using this command:

``` Bash
myenv/Scripts/activate
```
Then, install the `requirements.txt` file to install the dependencies into your environment:

``` Bash
 pip install -r requirements.txt
 ```
 Then use the environment as your jupyter notebook kernel.

> [!WARNING]
> As this program uses Pytorch, the Python version necessary to run this must be 3.11 or lower.
