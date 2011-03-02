OFA_ROOT := /opt/ofa64-1.5.1
OFA_INCLUDE := $(OFA_ROOT)/include
OFA_LIB := $(OFA_ROOT)/lib
VERBS_H := $(OFA_INCLUDE)/infiniband/verbs.h

rdma/ibverbs.so: rdma/libibverbs.pxd rdma/libibverbs.pxi rdma/ibverbs.pyx Makefile
	python setup.py build_ext \
		--include-dirs $(OFA_INCLUDE) \
		--library-dirs $(OFA_LIB) \
		--rpath $(OFA_LIB)

rdma/libibverbs.pxd rdma/libibverbs.pxi: codegen/ibtypes.py $(VERBS_H)
	python $< --fmt $(patsubst rdma/libibverbs.%,%,$@) $(VERBS_H) > $@
