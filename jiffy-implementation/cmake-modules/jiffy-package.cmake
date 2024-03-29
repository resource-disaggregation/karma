# whether package contains all development files or only runtime files
set (DEVEL )

# ------------------------------------------------------------------------------
# Debian package
if (CPACK_GENERATOR MATCHES "DEB")

  set (CPACK_PACKAGE_FILE_NAME   "lib${CPACK_PACKAGE_NAME}")
  if (DEVEL)
    set (CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-dev")
  else ()
    set (CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}0")
  endif ()
  set (CPACK_PACKAGE_FILE_NAME   "${CPACK_PACKAGE_FILE_NAME}_${CPACK_PACKAGE_VERSION}-1_${CPACK_PACKAGE_ARCHITECTURE}")

  set (CPACK_DEBIAN_PACKAGE_DEPENDS)
  set (CPACK_DEBIAN_PACKAGE_SECTION      "devel")
  set (CPACK_DEBIAN_PACKAGE_PRIORITY     "optional")
  set (CPACK_DEBIAN_PACKAGE_HOMEPAGE     "${CPACK_RPM_PACKAGE_URL}")
  set (CPACK_DEBIAN_PACKAGE_MAINTAINER   "${CPACK_PACKAGE_VENDOR}")
  set (CPACK_DEBIAN_PACKAGE_ARCHITECTURE "${CPACK_PACKAGE_ARCHITECTURE}")

# ------------------------------------------------------------------------------
# RPM package
elseif (CPACK_GENERATOR MATCHES "RPM")

  set (CPACK_PACKAGE_FILE_NAME   "${CPACK_PACKAGE_NAME}")
  if (DEVEL)
    set (CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-devel")
  endif ()
  set (CPACK_PACKAGE_FILE_NAME   "${CPACK_PACKAGE_FILE_NAME}-${CPACK_PACKAGE_VERSION}-1.${CPACK_PACKAGE_ARCHITECTURE}")

endif ()
