Introduction
============

.. image:: https://readthedocs.org/projects/community-circuitpython-tca9555/badge/?version=latest
    :target: https://community-circuitpython-tca9555.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/lesamouraipourpre/Community_CircuitPython_TCA9555/workflows/Build%20CI/badge.svg
    :target: https://github.com/lesamouraipourpre/Community_CircuitPython_TCA9555/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for Texas Instruments TCA9555 Low-Voltage 16-Bit I2C
and SMBus I/O Expander with Input / Output and Polarity Inversion.

`DataSheet <https://www.ti.com/lit/ds/symlink/tca9555.pdf>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/community-circuitpython-tca9555/>`_.
To install for current user:

.. code-block:: shell

    pip3 install community-circuitpython-tca9555

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install community-circuitpython-tca9555

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install community-circuitpython-tca9555



Usage Example
=============

Create an instance of TCA9555 expander. This defaults to all 16 pins set as
inputs with no polarity conversion.

.. code-block:: python

    from community_tca9555 import TCA9555
    # If the board has I2C defined
    expander = TCA9555(board.I2C())  # Use default address of 0x20
    # Else specify the specific pins
    expander = TCA9555(busio.I2C(scl=board.GP5, sda=board.GP4))  # for the RP Pico

Set the low 8 bits as inputs and the high 8 bits as outputs.

.. code-block:: python

    # set all 16 pins at once
    expander.configuration_ports = 0x00FF

    # or
    # set port 0 (8bits) and port 1 (8 bits)
    expander.configuration_port_0 = 0xFF  # Inputs
    expander.configuration_port_1 = 0x00  # Outputs

    # or
    # set each pin individually
    expander.configuration_port_0_pin_0 = True   # Input
    # ...
    expander.configuration_port_1_pin_7 = False  # Output

Set pins 6 and 7 of both port 0 and port 1 as polarity inverted.

.. code-block:: python

    # Set polarity inversion state for individual pins.
    expander.polarity_inversion_port_0_pin_6 = True  # Inverted
    expander.polarity_inversion_port_0_pin_7 = True
    expander.polarity_inversion_port_1_pin_6 = True
    expander.polarity_inversion_port_1_pin_7 = True

    # or
    # Set an 8bit port at once
    expander.polarity_inversion_port_0 = 0xC0  # Just bits 6 and 7

    # or
    # Set all 16bits at once
    expander.polarity_inversions = 0xC0C0

Read the input pins.

.. code-block:: python

    input_state = expander.input_port_0
    print("Inputs: {:08b}".format(input_state))

Set the state of the output pins.

.. code-block:: python

    expander.output_port_1 = 0x42


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/lesamouraipourpre/Community_CircuitPython_TCA9555/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
