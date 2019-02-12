cmake_minimum_required(VERSION 2.6)
project(NautilusAdmin NONE)
find_package(Gettext REQUIRED)

# Configurable paths
set(NAUTILUS_PATH "/usr/bin/nautilus" CACHE FILEPATH "nautilus program path.")
set(GEDIT_PATH "/usr/bin/gedit" CACHE FILEPATH "gedit program path.")

# Configure files
configure_file(extension/nautilus-admin.py
               extension/nautilus-admin.py)

# Update and compile the translations
file(GLOB TRANSLATION_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "po/*")
foreach(trans_file ${TRANSLATION_FILES})
    configure_file(${trans_file} ${trans_file} COPYONLY)
endforeach()
file(GLOB PO_FILES "${CMAKE_CURRENT_BINARY_DIR}/po/*.po")
gettext_create_translations("${CMAKE_CURRENT_BINARY_DIR}/po/nautilus-admin.pot"
                            ALL ${PO_FILES})

# Install target
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/extension/nautilus-admin.py"
        DESTINATION /usr/share/nautilus-python/extensions)

# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND}
                  -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)
