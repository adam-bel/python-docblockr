DocBlockr for Python
====================

Based off the [DocBlockr](https://github.com/spadgos/sublime-jsdocs) project, This extension provides the similar funtionality but for python docstrings.
The default formatter for this plugin is designed around [PEP-257](https://www.python.org/dev/peps/pep-0257/) compliance but with more verbosity: Added variable types, listing class extensions, and listing decorators.
The main goal of this project is to help developer provide better documentation by giving easy and consistent formatting.


Installation
------------
<!-- **Package Control**
Now you can install it with package control!

1. Open your command pallete and type `Package Control: Install Package`.
1. Find this project `DocBlockr Python` and press `Enter`. -->

**Manually**
Download the release and put it in your installed packages directory yourself

1. Go to the [Latest Release](https://github.com/thep0y/python-docblockr/releases/latest) and download the `python-docblockr.sublime-package` file.
1. Move this file to your `Installed Packages` directory. (`Preferences > Browse Packages...` and go up one directory to see `Installed Packages`)
1. If you are updating your existing install, a restart of Sublime Text will be in order.


Usage
-----
There isn't a command pallete command to start this plugin, it is triggerg by hitting **enter** or **tab** after opening a docstring (`"""`) at the `module`, `class`, or `function` level.
If you wanted to simply put a new line after opening a docstring and not trigger the formatter, just hold `ctrl` and press enter.


Default and User Settings
-------------------------
You can configure which docstring format to use by updating your user settings for this package (`Preferences > Package Settings > Python DocBlockr > Settings`).


Project Settings
----------------
You can also override your user settings on a per project basis by editing your project file. Any setting will be available for overriding here.

```json
{
	"PythonDocblockr": {
		"formatter": "sphinx"
	},
	"folders": [
	  // ...
	]
}
```


Supported Docstring Styles
--------------------------
- Docblockr (PEP0257 with types)
- [PEP0257](https://www.python.org/dev/peps/pep-0257/)
- [Google](https://google.github.io/styleguide/pyguide.html#Comments)
- [Numpy](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
- [Sphinx (reST)](https://pythonhosted.org/an_example_pypi_project/sphinx.html)



Known Issues
------------
- Only detects closed docstring if it is on a line of the same indentation, and has no text in front of it. Single Line docstrings are converted to block
