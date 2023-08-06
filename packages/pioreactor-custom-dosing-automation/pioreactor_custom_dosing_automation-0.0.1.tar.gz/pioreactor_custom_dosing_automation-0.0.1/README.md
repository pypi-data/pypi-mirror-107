## An example of how to include a custom dosing / LED / temperature automation

This is an example repository for creating a custom automation for the [Pioreactor](https://pioreactor.com/). By turning your automation into a repository, it can be installed easier into your Pioreactor cluster, and can be shared with others:


If available on PyPI:
```
pio install-plugin <plugin-name>
```

(And also `pios` to install across your entire cluster.)

If avaiable on Github:

```
pio install-plugin <plugin-name> --url <git+ url>
```


### Components to make your own automation plugin

#### Python logic

This is the core logic that interacts with the pioreactor software. See the class `MyCustomDosingAutomation` for details. Note the following:

 - subclasses from `DosingAutomationContrib`, `LEDAutomationContrib`, or `TemperatureAutomationContrib`
 - requires a `key`
 - requires an `execute`

There are many other examples of automations in our core [repository](https://github.com/Pioreactor/pioreactor/tree/master/pioreactor/automations)


It's important that the class is in this the main `__init__.py`, as this is how `DosingController` discovers it.


#### `setup.py`

This can be copy-pasted into your project, with the fields updated. The most important field is
```python
  entry_points={'pioreactor.plugins': 'pioreactor_custom_dosing_automation = pioreactor_custom_dosing_automation'},
```

This is necessary, and your code should be updated with the correct name of your plugin.


### Adding specific settings to config.ini
Using the file `additional_config.ini` (must be located in the source code's folder), you can add user-editable settings for your automation. This will be merged into the `config.ini`.

### Adding your automation to the UI

You can specify the automation in the automation drop-down in the UI, and specify its fields and default values to be shown to the user.

Create a folder called `ui` in the source code folder. Inside it, create a folder called `contrib`. And inside that, create a folder depending on your automation type: `dosing`, `led`, or `temperature`. See below for example directory structure.


### `MANIFEST.in`

In order for Python to include `ui` and/or `additional_config.ini`, we need to specify them in a `MANIFEST.in` file. Copy-paste the `MANIFEST.in` from this project, and make the appropriate substitutions in its contents.



### Example directory structure for your plugin

```
 plugin_name/
    __init__.py
    other_python_files.py
    additional_config.ini
    ui/
      contrib/
        automations/
          dosing/
            plugin_name.yaml        OR
          led/
            plugin_name.yaml        OR
          temperature/
            plugin_name.yaml
setup.py
MANIFEST.in

```
