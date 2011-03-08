#! /usr/bin/python

# FIXME: look at using ctypes here.

import optparse
import re
import sys

parser = optparse.OptionParser(usage="%prog [options] file.h")
parser.add_option('--fmt', type="choice", choices=('pxi','pxd'), default='pxi')

(opt, args) = parser.parse_args()
if len(args) != 1:
    parser.error("expected include file argument")

pxi = """
%(enums)s

wc = tools.struct(
    'wc',
    (('wr_id',long),
     ('status',int), #enum
     ('opcode',int), #enum
     ('vendor_err',int),
     ('byte_len',int),
     ('imm_data',int),
     ('qp_num',int),
     ('src_qp',int),
     ('wc_flags',int),
     ('pkey_index',int),
     ('slid',int),
     ('sl',int),
     ('dlid_path_bits',int)
    )
)

global_route = tools.struct(
    'global_route',
    (
     ('dgid',IBA.GID),
     ('flow_label',int),
     ('sgid_index',int),
     ('hop_limit',int),
     ('traffic_class',int)
    )
)

ah_attr = tools.struct(
    'ah_attr',
    (
     ('grh',global_route),
     ('dlid',int),
     ('sl',int),
     ('src_path_bits',int),
     ('static_rate',int),
     ('is_global',int),
     ('port_num',int)
    )
)

qp_init_attr = tools.struct(
    'qp_init_attr',
    (
     ('send_cq',None), # needs forward decl
     ('recv_cq',None),
     ('srq',None),
     ('cap',int),
     ('qp_type',int),
     ('sq_sig_all',int)
    )
)

qp_cap = tools.struct(
    'qp_cap',
    (
     ('max_send_wr',int),
     ('max_recv_wr',int),
     ('max_send_sge',int),
     ('max_recv_sge',int),
     ('max_inline_data',int)
    )
)

qp_attr = tools.struct(
    'qp_attr',
    (
     ('qp_state',int,IBV_QP_STATE),
     ('cur_qp_state',int,IBV_QP_CUR_STATE),
     ('path_mtu',int,IBV_QP_PATH_MTU),
     ('path_mig_state',int,IBV_QP_PATH_MIG_STATE),
     ('qkey',int,IBV_QP_QKEY),
     ('rq_psn',int,IBV_QP_RQ_PSN),
     ('sq_psn',int,IBV_QP_SQ_PSN),
     ('dest_qp_num',int,IBV_QP_DEST_QPN),
     ('qp_access_flags',int,IBV_QP_ACCESS_FLAGS),
     ('cap',qp_cap,IBV_QP_CAP),
     ('ah_attr',ah_attr,IBV_QP_AV),
     ('alt_ah_attr',ah_attr,IBV_QP_ALT_PATH),
     ('pkey_index',int,IBV_QP_PKEY_INDEX),
     ('alt_pkey_index',int,IBV_QP_ALT_PATH),
     ('en_sqd_async_notify',int,IBV_QP_EN_SQD_ASYNC_NOTIFY),
     ('sq_draining',int),
     ('max_rd_atomic',int,IBV_QP_MAX_QP_RD_ATOMIC),
     ('max_dest_rd_atomic',int,IBV_QP_MAX_DEST_RD_ATOMIC),
     ('min_rnr_timer',int,IBV_QP_MIN_RNR_TIMER),
     ('port_num',int,IBV_QP_PORT),
     ('timeout',int,IBV_QP_TIMEOUT),
     ('retry_cnt',int,IBV_QP_RETRY_CNT),
     ('rnr_retry',int,IBV_QP_RNR_RETRY),
     ('alt_port_num',int,IBV_QP_ALT_PATH),
     ('alt_timeout',int,IBV_QP_ALT_PATH)
    )
)

srq_attr = collections.namedtuple(
    'srq_attr',
    'max_wr max_sge srq_limit')

port_attr = collections.namedtuple(
    'port_attr',
    '''state
     max_mtu
     active_mtu
     gid_tbl_len
     port_cap_flags
     max_msg_sz
     bad_pkey_cntr
     qkey_viol_cntr
     pkey_tbl_len
     lid
     sm_lid
     lmc
     max_vl_num
     sm_sl
     subnet_timeout
     init_type_reply
     active_width
     active_speed
     phys_state''');

device_attr = collections.namedtuple(
    'device_attr',
    '''fw_ver
    node_guid
    sys_image_guid
    max_mr_size
    page_size_cap
    vendor_id
    vendor_part_id
    hw_ver
    max_qp
    max_qp_wr
    device_cap_flags
    max_sge
    max_sge_rd
    max_cq
    max_cqe
    max_mr
    max_pd
    max_qp_rd_atom
    max_ee_rd_atom
    max_res_rd_atom
    max_qp_init_rd_atom
    max_ee_init_rd_atom
    atomic_cap
    max_ee
    max_rdd
    max_mw
    max_raw_ipv6_qp
    max_raw_ethy_qp
    max_mcast_grp
    max_mcast_qp_attach
    max_total_mcast_qp_attach
    max_ah
    max_fmr
    max_map_per_fmr
    max_srq
    max_srq_wr
    max_srq_sge
    max_pkeys
    local_ca_ack_delay
    phys_port_cnt''');

sge = tools.struct(
    'sge',
    (
     ('addr',int),
     ('length',int),
     ('lkey',int)
    )
)

# Refer to verbs documentation to see which fields are valid for which
# operation
send_wr = tools.struct(
    'send_wr',
    (
     ('wr_id', long),
     ('sg_list', None), # sge or list/tuple of sge
     ('opcode', int),
     ('send_flags', int),
     ('imm_data', int),

     # WR_RDMA*
     ('remote_addr', long),
     ('rkey', int),

     # WR_ATOMIC_*
     # + remote_addr
     ('compare_add',long),
     ('swap',long),
     ('rkey',int),

     # UD WR_SEND
     ('ah', None),
     ('remote_qpn', int),
     ('remote_qkey', int)
    )
)

recv_wr = tools.struct(
    'recv_wr',
    (
     ('wr_id', long),
     ('sg_list', None), # sge or list/tuple of sge
    )
)
"""

pxd = """
cdef extern from 'infiniband/verbs.h':

%(enums)s

    union ibv_gid:
        char *raw

    struct ibv_global_route:
        ibv_gid dgid
        int flow_label
        int sgid_index
        int hop_limit
        int traffic_class

    struct ibv_grh:
        unsigned int version_tclass_flow
        unsigned int paylen
        unsigned int next_hdr
        unsigned int hop_limit
        ibv_gid sgid
        ibv_gid dgid

    struct ibv_ah_attr:
        ibv_global_route grh
        int dlid
        int sl
        int src_path_bits
        int static_rate
        int is_global
        int port_num

    struct ibv_device:
        char *name

    struct ibv_context:
        ibv_device *device

    struct ibv_pd:
        pass

    struct ibv_mr:
        void *addr
        size_t length
        int lkey
        int rkey

    struct ibv_cq:
        pass

    struct ibv_comp_channel:
        int fd

    struct ibv_ah:
        ibv_context *context
        ibv_pd *pd
        int handle

    struct ibv_wc:
        long wr_id
        int status
        int opcode
        int vendor_err
        int byte_len
        int imm_data
        int qp_num
        int src_qp
        int wc_flags
        int pkey_index
        int slid
        int sl
        int dlid_path_bits

    struct ibv_srq_attr:
        unsigned int max_wr
        unsigned int max_sge
        unsigned int srq_limit

    struct ibv_srq_init_attr:
        void *srq_context
        ibv_srq_attr attr

    struct ibv_srq:
        pass

    struct ibv_qp:
        int qp_num
        int qp_type
        int state

    struct ibv_qp_cap:
        int max_send_wr
        int max_recv_wr
        int max_send_sge
        int max_recv_sge
        int max_inline_data

    struct ibv_qp_init_attr:
        void *qp_context
        ibv_cq *send_cq
        ibv_cq *recv_cq
        ibv_srq *srq
        ibv_qp_cap cap
        ibv_qp_type qp_type
        int sq_sig_all

    struct ibv_qp_attr:
        ibv_qp_state qp_state
        ibv_qp_state cur_qp_state
        ibv_mtu path_mtu
        ibv_mig_state path_mig_state
        int qkey
        int rq_psn
        int sq_psn
        int dest_qp_num
        int qp_access_flags
        ibv_qp_cap cap
        ibv_ah_attr ah_attr
        ibv_ah_attr alt_ah_attr
        int pkey_index
        int alt_pkey_index
        int en_sqd_async_notify
        int sq_draining
        int max_rd_atomic
        int max_dest_rd_atomic
        int min_rnr_timer
        int port_num
        int timeout
        int retry_cnt
        int rnr_retry
        int alt_port_num
        int alt_timeout

    struct ibv_sge:
        long addr
        int length
        int lkey

    struct ibv_send_wr_wr_rdma:
        long remote_addr
        int rkey

    struct ibv_send_wr_wr_atomic:
        long remote_addr
        long compare_add
        long swap
        int rkey

    struct ibv_send_wr_wr_ud:
        ibv_ah *ah
        int remote_qpn
        int remote_qkey

    union ibv_send_wr_wr:
        ibv_send_wr_wr_rdma rdma
        ibv_send_wr_wr_atomic atomic
        ibv_send_wr_wr_ud ud

    struct ibv_send_wr:
        long wr_id
        ibv_send_wr *next
        ibv_sge *sg_list
        int num_sge
        int opcode
        int send_flags
        int imm_data
        ibv_send_wr_wr wr

    struct ibv_recv_wr:
        long wr_id
        ibv_recv_wr *next
        ibv_sge *sg_list
        int num_sge

    struct ibv_port_attr:
        ibv_port_state state
        ibv_mtu max_mtu
        ibv_mtu active_mtu
        int gid_tbl_len
        int port_cap_flags
        int max_msg_sz
        int bad_pkey_cntr
        int qkey_viol_cntr
        int pkey_tbl_len
        int lid
        int sm_lid
        int lmc
        int max_vl_num
        int sm_sl
        int subnet_timeout
        int init_type_reply
        int active_width
        int active_speed
        int phys_state

    struct ibv_device_attr:
        char fw_ver[64]
        unsigned long node_guid
        unsigned long sys_image_guid
        unsigned long max_mr_size
        unsigned long page_size_cap
        unsigned int vendor_id
        unsigned int vendor_part_id
        unsigned int hw_ver
        int max_qp
        int max_qp_wr
        int device_cap_flags
        int max_sge
        int max_sge_rd
        int max_cq
        int max_cqe
        int max_mr
        int max_pd
        int max_qp_rd_atom
        int max_ee_rd_atom
        int max_res_rd_atom
        int max_qp_init_rd_atom
        int max_ee_init_rd_atom
        ibv_atomic_cap atomic_cap
        int max_ee
        int max_rdd
        int max_mw
        int max_raw_ipv6_qp
        int max_raw_ethy_qp
        int max_mcast_grp
        int max_mcast_qp_attach
        int max_total_mcast_qp_attach
        int max_ah
        int max_fmr
        int max_map_per_fmr
        int max_srq
        int max_srq_wr
        int max_srq_sge
        unsigned int max_pkeys
        unsigned int local_ca_ack_delay
        unsigned int phys_port_cnt

    ibv_device **ibv_get_device_list(int *n)
    void ibv_free_device_list(ibv_device **list)
    ibv_context *ibv_open_device(ibv_device *dev)
    int ibv_close_device(ibv_context *ctx)
    int ibv_query_port(ibv_context *ctx, int port_num, ibv_port_attr *attr)
    int ibv_query_device(ibv_context *ctx, ibv_device_attr *attr)

    ibv_pd *ibv_alloc_pd(ibv_context *ctx)
    int ibv_dealloc_pd(ibv_pd *pd)

    ibv_ah *ibv_create_ah(ibv_pd *pd, ibv_ah_attr *attr)
    int ibv_destroy_ah(ibv_ah *ah)

    ibv_mr *ibv_reg_mr(ibv_pd *pd, void *addr, int length, int access)
    int ibv_dereg_mr(ibv_mr *mr)

    ibv_comp_channel *ibv_create_comp_channel(ibv_context *ctx)
    int ibv_destroy_comp_channel(ibv_comp_channel *chan)

    ibv_cq *ibv_create_cq(ibv_context *ctx, int cqe,
                          void *user_cq_ctx,
                          ibv_comp_channel *chan,
                          int comp_vector)
    int ibv_destroy_cq(ibv_cq *cq)
    int ibv_poll_cq(ibv_cq *cq, int n, ibv_wc *wc)
    int ibv_req_notify_cq(ibv_cq *cq, int solicited_only)
    int ibv_get_cq_event(ibv_comp_channel *chan,ibv_cq **,void **cq_context)
    void ibv_ack_cq_events(ibv_cq *cq,unsigned int nevents)
    int ibv_resize_cq(ibv_cq *cq, int cqe)

    ibv_qp *ibv_create_qp(ibv_pd *pd, ibv_qp_init_attr *init_attr)
    int ibv_destroy_qp(ibv_qp *qp)
    int ibv_modify_qp(ibv_qp *qp, ibv_qp_attr *attr, int attr_mask)
    int ibv_query_qp(ibv_qp *qp, ibv_qp_attr *attr, int attr_mask, ibv_qp_init_attr *init)
    int ibv_post_send(ibv_qp *qp, ibv_send_wr *wr, ibv_send_wr **bad_wr)
    int ibv_post_recv(ibv_qp *qp, ibv_recv_wr *wr, ibv_recv_wr **bad_wr)
    int ibv_attach_mcast(ibv_qp *qp, ibv_gid *gid, unsigned int lid)
    int ibv_detach_mcast(ibv_qp *qp, ibv_gid *gid, unsigned int lid)

    ibv_srq *ibv_create_srq(ibv_pd *pd,ibv_srq_init_attr *srq_init_attr)
    int ibv_destroy_srq(ibv_srq *srq)
    int ibv_modify_srq(ibv_srq *srq,ibv_srq_attr *srq_attr,int srq_attr_mask)
    int ibv_query_srq(ibv_srq *srq,ibv_srq_attr *srq_attr)
    int ibv_post_srq_recv(ibv_srq *qp, ibv_recv_wr *wr, ibv_recv_wr **bad_wr)

    char *ibv_wc_status_str(int status)
"""

f = open(args[0])
s = f.read()
comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
s = comment_pattern.sub('', s)

enum = {}
for m in re.finditer(r'enum\s+(\w+)\s*{(.*?)}', s, re.DOTALL):
    name = m.group(1)
    constants = [c.partition('=')[0].strip() for c in m.group(2).split(',')]
    enum[name] = tuple(constants)

ekeys = sorted(enum.keys())
if opt.fmt == 'pxi':
    print pxi % { 'enums':
                  '\n\n'.join('\n'.join('%s = c.%s' % (c, c) for c in enum[e])
                              for e in ekeys) }
else:
    sep = '\n' + ' '*8
    print pxd % { 'enums': '\n\n'.join('    enum %s:%s' % (e,sep) + sep.join(enum[e])
                                       for e in ekeys) }

