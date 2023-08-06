
# particle board REPL (PBR)  program.


    pip install Particle_Board_REPL
    
To run interactively in with the REPL.

    PBR -r

This Module adds Particle board cli functionality along with
various other higher level functions for interacting with Particle.io boards.
The idea is to make it possible to create a repeatable process which can interact
test, and program a particle.io board.

This uses the particle.io cli, **particle-cli** in the Arch-linux AUR,
to interface with a board, verify it's life, update it, claim/register
it, flash it, test it, etc.

All of the commands here could be almost doable in a chain of _'do this', 'do that'_. But
the boards take time in between events. The USB device comes up and down constantly,
it's not reliable just because you know that's where the board was. I have read about
other gnu/linuxs which change the device on occasion or always. Arch does not. Once
I have it, I have it. However, it comes and goes... 

If a command fails at any point in a process, the entire process stops and the
board is considered a failure.

So we have to wait, watch and listen.

But, as a whole, it's just a module of things we'd like to do.  So we 
wrap those up to make life easier. and life is easier. At some point, 
making life is easier is just listing all the previous things that made life easier. 
And so it goes.

# Particle Board REPL runs 4 ways.

Once you have some processes defined you can then run what you like in
4 different ways,w

 * run the autoexec setting once: `PBR`
 * Start a REPL   `-r`
 * Run the autoexec setting in a loop with a continue dialog `-i` 
 * To run commands instead of the autoexec, Just add them to the command.

 `PBR -r get list
  PBR -i get list
  PBR get list
  PBR -r msgbox "hello"`


### Getting Help

Help with the command line can be obtained with `-h`,
Additionally, Help with the symbols which are available for programming in the yaml files or 
in the REPL are obtained with the `help` command, so `help` runs help.
 * `PBR -h` for cli help.
 * `PBR help` for internal help.
 * `PBR particle-help` for internal particle specific help.

The easiest way to understand this system by using the REPL. 
It will show you how it works. `PBR -r` 
 
Once in the REPL at the prompt; __PBR:>__,  There are two help 
commands.  __help__ and __particle-help__.  _Help_ shows all
the commands known with their documentation. _particle-help_,
__show-all__ will show you everything there is to know about the state
of things in yaml format. __showin__ lets you drill in if you like.


### Get

It's the first command you'll want to do when you plug in your particle board.

This is the command we use to populate our _usb device_, _board type_ and _device-id_.
Various particle commands need the id, and we need the usb device so we know
who to wait for. It uses `particle serial list` for it's data.

The first thing to do is a __list__ and a __get__ or just a __get__. From there
the device id board type and usb device should be known. They will be used
for other commands in the process.

If you know particle commands then those should make sense, this is a small subset of the
possibilities. 

The REPL will do whatever you ask, so _help_, _show_, _list_, _identify_, 
_update_, _set-setup-done_, etc. Some which require a bit more, such as entering _dfu_ 
or _listen_ mode, are wrapped up together for convenience, but also available as
commands themselves.


## Particle.io Lights.
Something very important for knowing the state of your Particle.io boron.

[The meaning of the lights on a Particle.io Boron.](https://docs.particle.io/tutorials/device-os/led/boron/)


## The modules, main.py, particle.py, and Config.

The more complex Particle functions are in main.py, These are functions which 
interact with the Application state as well as the device. 
This is also where the symbol tables are defined for the add on particle cli
functionality.

There is very little in the particle.py module. Particle cli commands are 
one line functions, and truly many of them are unecessary as they could be
done with the `pcmd`.

These are most of the basic particle-cli commands I've used so far. All of 
these functions are here to be as close to bare particle-cli commands as can be. 
I combined some things, like flash always does dfu first, identify always does a listen. 
Get is perhaps the most complex as it does wait and poll to give a chance 
for a reset or a plug. Internally there are a few versions of get to choose from.

The rest of the functions can actually live in the configuration file. 
It is only necessary to modify python code if there is a desire for more 
base functionality.

# Current state

__flash-test__, __flash-image__, __flash-tinker__, are working, but through 
os.popen().read() instead of subprocess like everything else.  I don't have an
explanation, subrocess needs more configuration for these commands. I've 
tried _shell=True_ with no change. So it's going be down in the details somewhere.

I had thought that perhaps using the particle.get_w_wait function to wait for 
the device could work nicely, but it does not. 

__login__ and __log_out__ needed to be called with os.system in order for them to
behave nicely with their prompts. Subprocess could work I think, but it's configuration
is complex and it's not worth investigating.


# The Internals.

This is at it's heart a simple Read Eval Print Loop. It has 4 ways
of running, and it automatically manages Application state, yaml 
configuration files, the command line, dialogs, prompts, logging and help.  
Everything needed for a particular application can be done with a module of functions..

The cli is done with argparse is extendible from the application layer as needed.

Python dialog, with several standard messages and boxes are included, as is 
a yaml configuration, and an Application state which contains everything
known to the app.

Everything is extensible. Usually a few python functions
and a configuration file is all you will need to create a nicely versatile 
application.

While there is a Repl available, and commands can be added, combined
and remixed, they can also be run automatically through the
autoexec setting in the config.  The default autoexec is to provide help.

## Configuration

The Simple Process REPL uses YAML for it's configuration files. 

Everything is specified there,
there is very little in common with the cli. If no config file is given, the default
_SPR-config.yaml_ will be loaded if found. The primary purpose of the cli is to 
designate the fashion you would like for the REPL to run. 

All necessary defaults are set within the package with SPR-defaults.yaml.
When building an application, that application's defaults will be merged 
into the Simple_Process_REPL's default configuration before loading a locally defined
SPR-config.yaml. An application can over-ride the configuration file name with a setting
in the defaults section of the Application State.


## 4 modes of running

  * Run in a loop for doing a process over and over 
  * Run the default process once 
  * Run a list of command/symbols from the command line 
  * As an interactive REPL 
  
__In any case, if any step fails, the process will fail.__ 
if in interactive loop mode, _-i_, the continue dialog will catch the fail for the next
loop.

## The default process
In the __exec__ section of the configuration there is an __autoexec__ attribute. 
This should be a symbol name or list of symbol names to run as the default process. 
This is the process that will run when running cli in interactive loop mode,
or when run once.
  
If commands are given on the cli after the option then that list is executed once 
automatically instead of the commands in autoexec.

The easiest way to understand this is system is by using the REPL. 
It will show you how it works. `PBR -r` 
 
Then type _help_, particle-help, and _showin_.  __Read It!__

Once in the REPL at the prompt; __PBR:>,
_help_ shows all the commands known with their documentation. 

## Symbols/Commands/functions

There are three kinds.

 * Symbols which point at directly at parameter-less functions
 * Symbols which are lists of symbols, _compound commands_.
 * Symbols which are _special_ because they take parameters.

### symbol/functions.
These commands are just python functions, whatever it is they do.
Usually, manipulate the application state, and/or interact with something.

### Compound commands

Compound commands are commands defined outside of python code. They are strings which
can be parsed and evaluated by the REPL/interpreter.

Compound commands can be built from other compound commands and _special_ commands.
Compound commands can be defined in the configuration yaml, in python code, 
or interactively in the REPL.


## The REPL

The REPL is very convenient as it saves state, and can be used to
interactively create/execute a process step by step. 
`help` at the REPL prompt. 

 * Builtins __help__ 
 * __showin__, are quite handy.
 * REPL prompt: persistent history and tab completion. 
 * The __loglvl__ command can change the logging level interactively.
 * Defining a symbol of a special works. - Super cool.
    * `msgbox "Hello World"` 
    * `def mymsg "my special msg" msgbox "Hello World"`
 * __log-info__ and __log-debug__ allow sending of arbitrary messages to the log.
 * __sh__ for running shell commands.
 * __pcmd__ for running particle-cli commands.

### Application State. 

```python
AS = {
    "config": {},
    "args": {},
    "defaults": {
        "config_file": "PBR-config.yaml",
        "loglevel": "info",
        "logfile": "PBR.log",
    },
    "device": {"id": "", "name": "", "path": ""},
    "wifi-connected": False,
    "platform": platform(),
}
```
 * configuration is the merged yaml configurations
 * args is the resolved command line
 * defaults is used by argparse to supply default options to the command line.
 * device is an imaginary device. Which we can wait for and handshake with.

The command: **showin** in the REPL will give it to you in yaml.
**help** will give you the documentation for every command you can do, even the ones you just created. 
The easiest way to access it is `showin device` or `showin config serial`
with `showin key1 key2,...` is the command to find sub-section or attributes in the REPL.
`showin config` , `showin defaults`, or just __showin__ which is the same as __show-all__.

For an Application layer, it is only necessary to provide a structure as desired, which
will be merged directly onto this structure.


## It's a Simple list processor.

This program is actually a very simple interpreter with an interactive REPL. 
Everything you want to do must be a python function which is registered in the
interpreter's symbol table. From there, everything is composable from symbol/words
from the interpreter's symbol table, ie, your symbols. Those composed symbols can 
also be added to the interpreter's symbol table to create increasingly
complex sets of processes, which are executed in order. These user
functions can also be defined in the YAML config file.

It has a really, really stupid parser. All it can do execute a list of symbols, or call
a special symbol with everything that follows. It does know the difference between
symbols, strings and numbers.

Basic symbol/functions should be functions done entirely for their side-effects.
They take no parameters and give no return. Special Symbols can take arguments.

At the lowest level the symbols/commands are directly connected to
python functions. But symbols/commands can also be lists of known symbols instead
of a function.  This allows for the creation of sub-groups which can be referenced by
other symbols.  There are no parentheses, only the ability to associate lists of
symbols with a new symbol.

    import repl as r
    symbols = [
        ['wifi',       connect_wifi,    'Connect to wifi using nmtui if not connected.']
        ['list',       P.list_usb,      'List the boards connected to USB.']
        ['start',      'wifi list',     'Connect wifi and list the boards.']
        ['identify',   P.identify,      'Try to identify a device.']
        ['domore',     'start identify', 'Start then identify']
        ['doevenmore', 'domore setup',   'Start identify and setup.']
    ]
    r.init_symbol_table(symbols)

The symbols _start_, _domore_ and _doevenmore_ can be defined in the YAML 
configuration file, it is not necessary to modify python code unless new 
functionality needs to be introduced.

## Special Symbols

The interpreter is not very bright and has no way of grouping things together which
makes it difficult to execute commands which take arguments. Specials are symbols 
at the beginning of a command which will eat the rest of the line, in attempt to
do what they are supposed to do.

To compensate the interpreter has the concept of special symbols, 
These are symbols which take arguments and can consume the entire REPL command. 

These are also pointers to python functions, but which take some arguments.
These go on a line by themselves since we have no way of knowing them unless the
line starts with them, and then the special gobbles up the rest of the line.

The REPL itself has a special symbol, __def__ which allows for the creation 
of a new symbol with the following syntax. 

    def <symbol> 'helpstr' symbol1 symbol2 symbol3...

Other commands are _save-config_, _load-config_, _msgbox_, _msgcli_,
_loglvl_, _log-info_, _showin_, etc.
    
Special symbols have an argument count which can be set. If positive the command will
be checked for compliance. Here is an example which
creates symbols for saving and loading configurations from a given filename.

    specials = [
        "Commands we want in the repl which can take arguments."
        ['save-config', save-config, 1,
        "Save the configuration; save-config 'filename'"]

        ['load-config', load-config, 1,
        "Load a configuration; save-config 'filename'"]
    ]
    

## Core: generic functionality

There are a few builtins which do 
special things. There is __wait__ which just waits for a device to come online 
with a timeout. There is pause which just sleeps for a few seconds as set in the 
configuration. The wifi function checks the wifi with linux's network manager, and
uses _nmcli_ to create a connection if one does not exist. Functionality is easy 
to add with a new function and an entry in the symbol table.

   * dialogs - There are some python dialog, and cli interface functionalities. 
   * wifi, - Uses network manager (nmcli) for linux. Non-functional on other platforms.
   * Waiting and handshaking.
        * __wait__ looks for the actual device path i/o event with a _timeout_.
        * __pause__ sleeps for _pause_time_. 
            Note: __wait__ for device is literally a poll to see if the device file exists.
            Once it appears there is some time before the udev rules make the file accessible
            by non-root users. A pause helps everything go smoothly. The next command will 
            actually have access to the device. So now I have a habit of following a __wait__ with
            a __pause__. 
        * __handshake__ does a blocking serial.read/readline for both the initial
        string, and the test results after. 


### Handshake function

This is a generic function that is a bit more complicated.  
It manages an interaction with a device. Everything _handshake_ 
does is defined in the configuration file. As with everything else, 
if anything fails, or doesn't match, an exception is raised.

Here are the steps that _handshake()_ does.

  * Wait for the _start_string_, match it.
  * Respond with the _response_string_.
  * Look in the output for: 
    * fail_regex, 
    * done_regex, 
    * do_qqc_regex.
  * If fail, raise an exception.
  * if done, exit quietly with true.
  * if do_qqc, then call the do_qqc_function 
  and send the return value to the serial device.

  qqc = quelque chose = something. 
  
  In the config the do_qqc_function is set to _input-serial_,
  as an example. Input-serial prompts for a serial number, 
  validates it, and returns it.  This function must be listed in
  the symbol table as that is where _handshake()_ will
  look for it. Makes it easy to test. _serial-input_ at the
  _SPR:>_ prompt.
      
    



