"""
Python Kit Information
~~~~~~~~~~~~~~~~~~~~~~

pykitinfo provides information about connected Microchip development kits.

pykitinfo will scan the USB subsystem for connected Microchip development kits, and provide information such as kit name, mounted device, serial port identifier, and extension information.

pykitinfo currently supports EDBG-based tools.

pykitinfo is available:
    * install using pip from pypi: https://pypi.org/project/pykitinfo
    * browse source code on github: https://github.com/microchip-pic-avr-tools/pykitinfo
    * read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitinfo

CLI usage example
~~~~~~~~~~~~~~~~~
See examples on pypi: https://pypi.org/project/pykitinfo

Library usage example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)
    from pykitinfo import pykitinfo
    kits = pykitinfo.detect_all_kits()
    for kit in kits:
        print("Found kit: '{}'".format(kit['debugger']['kitname']))

"""
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
