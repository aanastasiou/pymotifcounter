============
Installation
============

Prior to the adoption of ``pyproject.toml`` by Python (>=10.0), the installation of 
this package was not different to any other package obtained from PyPi.

This is because pymotifcounter was relying on parameter ``data_files`` of ``setup.py``.
This parameter packaged the compiled binaries along with the rest of the Python code 
and (more importantly) installed them in the virtual environment's
``bin/`` folder. From there, these binaries were becoming available to the command prompt 
whenever the virtual environment was active.

At the time of writing these lines (July 2023), the transition to the modern way of Python 
packaging, has not preserved the *exact* functionality of ``data_files``.

For this reason, from Pymotifcounter's version 2.0 onwards, **you** are responsible for 
making the binaries available to the rest of the system.

There is nothing to worry about though, because all I am doing in this section is 
expose the same steps that I have been taking to compile the binaries, most of which 
are already automated.

In what follows, ``code`` formatted lines beginning with ``>`` are "commands" to be entered
in the command line directly as seen, **without** the leading ``>`` character.

Installing ``pymotifcounter`` itself
====================================

A standard installation method is followed to install the package itself:

1. Create a virtual environment
2. Activate it
3. Download ``pymotifcounter``
4. Install it to the activated virtual environment.

Obtaining & Compiling the binaries
==================================

All available binaries are included in the top level directory ``binaries/``, 
each in its own folder.

At the time of writing these lines, these are as follows:

* NetMODE
* fanmod-cmd
* mfinder
* pgd

Obtaining and compiling each binary is common for the majority of these binaries. 

*Any special steps, wherever required are outlined in separate readme.md files in each directory*

.. note::

   To compile all of these binaries, your (Linux) system must have the ``build-essentials`` package 
   installed. This includes ``gcc, make`` and a few other tools and libraries that are required to 
   compile C and C++ code.

To compile a given binary:

1. Navigate to its directory (e.g. ``> cd binaries/NetMODE``)
2. Fetch the code with ``> ./fetch_NetMODE.sh``
3. Enter the directory that was just created with ``> cd NetMODE``
4. Compile the code with ``> make``

Compilation might take a few seconds but at the end of it you will see a binary created in the same directory (e.g. ``NetMODE``)

Repeat this process for each binary you want to make available to the rest of your system.

That is it.

Accessing the binaries
======================

Now, if you have just compiled ``NetMODE`` (for example) and your current working directory is ``binaries/NetMODE/NetMODE``, 
you can invoke the ``NetMODE`` binary on the command line by ``> ./NetMODE``.

But, once you navigate away from that directory, this "luxury" is gone.

So the problem now is how to maintain this access.

There are a few ways of achieving this and on a given Linux system, your primary criterion of choice 
might be, which locations you have access to.

The first method is guranteed to work with all configurations, the second method *might* require 
special access depending on the way your system administrator has set the system up.


Add symbolic links to specific directories
------------------------------------------

This process is the same (and works in exactly the same way), regardless of which 
directory you choose.

You have three options:

* ``~/.local/bin``, this directory is for binaries accessible to a given user. You definitely 
  have full access rights to this directory.

* ``/usr/local/bin`` is the (Linux) conventional directory for making third party binaries
  available to users in a given computer. You probably have access rights to this directory.

* Your V.Env's ``bin/`` directory contains executables that are specific to your Python installation.
  If you are using a program like ``pyenv``, you definitely have full access rights to this directory.


1. Find the ``bin`` directory of your choice

   * Either navigate to ``/usr/local/bin`` with ``> cd /usr/local/bin``, 
     or ``> cd ~/.local/bin``; or

   * Find the ``bin/`` directory of your virtual environment:

     * This depends on the way you have set your virtual environment up.
       For example, if you are using `pyenv <https://github.com/pyenv/pyenv>`_,
       the ``bin/`` directory you are looking for would be located in:
       ``~/.pyenv/versions/<name of your virtual environment>/bin``

2. Navigate to that directory (with ``~/.pyenv/versions/<name of your virtual environment>/bin``)

3. Create a `symbolic link <https://en.wikipedia.org/wiki/Symbolic_link>`_ to your binary.

   * A symbolic link is a way that the operating system offers (Linux), to make a file 
     appear within a directory *without* physically copying that file to that directory.

   * Create a symbolic link with ``ln -s <path to where you downloaded pymotifcounter>/binaries/NetMODE/NetMODE/NetMODE ./NetMODE``

4. Navigate to your home directory with ``> cd~/`` and you should now be able to run ``NetMODE``.


Add each binary to your ``PATH``
--------------------------------

1. Open your ``~/.bashrc`` or ``~/.bash_profile`` file with your favourite editor
2. Find the declaration of the ``PATH`` environment variable

   * It is a line beginning with ``export PATH="$PATH....``
3. Add the binary path you want to make available to the rest of the system with something like:

   ```
   export PATH="$PATH:/path/to/the/binary/directory
   ```

   * An easy way to recover the ``/path/to/the/binary/directory``, is to run ``> pwd`` from within your
     binary directory (e.g. ``binaries/NetMODE/NetMODE``). ``pwd`` will return an **absolute path** to
     that specific location. Just copy it exacly as it is returned and include if to the ``export PATH`` 
     statement.

4. "Source" your ``.bashrc`` or ``.bash_profile`` file (depending on which one you edited in step 1) for 
   the changes to take effect.



