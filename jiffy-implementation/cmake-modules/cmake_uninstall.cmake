if (NOT EXISTS "/home/midhul/jiffy/cmake-modules/install_manifest.txt")
  message(FATAL_ERROR "Cannot find install manifest: /home/midhul/jiffy/cmake-modules/install_manifest.txt")
endif (NOT EXISTS "/home/midhul/jiffy/cmake-modules/install_manifest.txt")

file(READ "/home/midhul/jiffy/cmake-modules/install_manifest.txt" cppfiles)
file(READ "/home/midhul/jiffy/cmake-modules/pyinstall_manifest.txt" pyfiles)
set(files "${cppfiles}\n${pyfiles}")
string(REGEX REPLACE "\n" ";" files "${files}")
foreach (file ${files})
  message(STATUS "Uninstalling $ENV{DESTDIR}${file}")
  if (IS_SYMLINK "$ENV{DESTDIR}${file}" OR EXISTS "$ENV{DESTDIR}${file}")
    exec_program(
            "/usr/local/bin/cmake" ARGS "-E remove \"$ENV{DESTDIR}${file}\""
            OUTPUT_VARIABLE rm_out
            RETURN_VALUE rm_retval
    )
    if (NOT "${rm_retval}" STREQUAL 0)
      message(FATAL_ERROR "Problem when removing $ENV{DESTDIR}${file}")
    endif (NOT "${rm_retval}" STREQUAL 0)
  else (IS_SYMLINK "$ENV{DESTDIR}${file}" OR EXISTS "$ENV{DESTDIR}${file}")
    message(STATUS "File $ENV{DESTDIR}${file} does not exist.")
  endif (IS_SYMLINK "$ENV{DESTDIR}${file}" OR EXISTS "$ENV{DESTDIR}${file}")
endforeach (file)
