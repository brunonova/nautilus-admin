Installing Nautilus Admin from source
=====================================

1.  Install the dependencies.
    In Ubuntu and Debian, these are the known dependencies:

    *   cmake
    *   gedit *(optional)*
    *   gettext
    *   gir1.2-gconf-2.0
    *   policykit-1
    *   python-nautilus

2.  Open a terminal in the project directory and run:

        mkdir build
        cd build
        cmake ..
        make
        sudo make install

3.  If Nautilus is running, restart it:

        nautilus -q

    Then start it again.
