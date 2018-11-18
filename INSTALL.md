Installing Nautilus Admin from source
=====================================

1.  Install the dependencies.
    In Ubuntu and Debian, these are the known dependencies:

    *   cmake
    *   gedit *(optional)*
    *   gettext
    *   python-nautilus

    The python-nautilus package may have different names on other distributions.
    On Fedora, for example, it's called nautilus-python.

2.  Open a terminal in the project directory and run:

        mkdir build
        cd build
        cmake ..
        make
        sudo make install

3.  If Nautilus is running, restart it:

        nautilus -q

    Then start it again.
