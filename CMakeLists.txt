cmake_minimum_required(VERSION 2.6)
project(NautilusAdmin NONE)
find_package(Gettext REQUIRED)

# Configurable paths
set(PKEXEC_PATH "/usr/bin/pkexec" CACHE FILEPATH "pkexec program path.")
set(NAUTILUS_PATH "/usr/bin/nautilus" CACHE FILEPATH "nautilus program path.")
set(GEDIT_PATH "/usr/bin/gedit" CACHE FILEPATH "gedit program path.")

# Configure files
configure_file(extension/nautilus-admin.py
               extension/nautilus-admin.py)
configure_file(polkit/org.freedesktop.nautilus-admin.policy
               polkit/org.freedesktop.nautilus-admin.policy)

# Update and compile the translations
gettext_create_translations(po/nautilus-admin.pot ALL po/ar.po po/fr.po po/pt.po
                                                      po/ru.po)

# Install target
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/polkit/org.freedesktop.nautilus-admin.policy"
        DESTINATION /usr/share/polkit-1/actions)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/extension/nautilus-admin.py"
        DESTINATION /usr/share/nautilus-python/extensions)

# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND}
                  -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)
