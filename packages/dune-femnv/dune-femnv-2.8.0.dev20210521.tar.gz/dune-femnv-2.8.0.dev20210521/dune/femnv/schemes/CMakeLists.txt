set(HEADERS
      capabilities.hh  diffusionmodel.hh  nvdgelliptic.hh
)
install(FILES ${HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/femnv/schemes)
