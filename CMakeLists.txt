cmake_minimum_required(VERSION 2.6)
project(NautilusAdmin NONE)

install(FILES polkit/org.freedesktop.nautilus-admin.policy DESTINATION /usr/share/polkit-1/actions)
install(FILES extension/nautilus-admin.py DESTINATION /usr/share/nautilus-python/extensions)
install(PROGRAMS bin/nautilus-pkexec DESTINATION /usr/bin)

# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)
