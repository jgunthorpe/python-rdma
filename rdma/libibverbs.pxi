
IBV_ACCESS_LOCAL_WRITE = c.IBV_ACCESS_LOCAL_WRITE
IBV_ACCESS_REMOTE_WRITE = c.IBV_ACCESS_REMOTE_WRITE
IBV_ACCESS_REMOTE_READ = c.IBV_ACCESS_REMOTE_READ
IBV_ACCESS_REMOTE_ATOMIC = c.IBV_ACCESS_REMOTE_ATOMIC
IBV_ACCESS_MW_BIND = c.IBV_ACCESS_MW_BIND

IBV_ATOMIC_NONE = c.IBV_ATOMIC_NONE
IBV_ATOMIC_HCA = c.IBV_ATOMIC_HCA
IBV_ATOMIC_GLOB = c.IBV_ATOMIC_GLOB

IBV_DEVICE_RESIZE_MAX_WR = c.IBV_DEVICE_RESIZE_MAX_WR
IBV_DEVICE_BAD_PKEY_CNTR = c.IBV_DEVICE_BAD_PKEY_CNTR
IBV_DEVICE_BAD_QKEY_CNTR = c.IBV_DEVICE_BAD_QKEY_CNTR
IBV_DEVICE_RAW_MULTI = c.IBV_DEVICE_RAW_MULTI
IBV_DEVICE_AUTO_PATH_MIG = c.IBV_DEVICE_AUTO_PATH_MIG
IBV_DEVICE_CHANGE_PHY_PORT = c.IBV_DEVICE_CHANGE_PHY_PORT
IBV_DEVICE_UD_AV_PORT_ENFORCE = c.IBV_DEVICE_UD_AV_PORT_ENFORCE
IBV_DEVICE_CURR_QP_STATE_MOD = c.IBV_DEVICE_CURR_QP_STATE_MOD
IBV_DEVICE_SHUTDOWN_PORT = c.IBV_DEVICE_SHUTDOWN_PORT
IBV_DEVICE_INIT_TYPE = c.IBV_DEVICE_INIT_TYPE
IBV_DEVICE_PORT_ACTIVE_EVENT = c.IBV_DEVICE_PORT_ACTIVE_EVENT
IBV_DEVICE_SYS_IMAGE_GUID = c.IBV_DEVICE_SYS_IMAGE_GUID
IBV_DEVICE_RC_RNR_NAK_GEN = c.IBV_DEVICE_RC_RNR_NAK_GEN
IBV_DEVICE_SRQ_RESIZE = c.IBV_DEVICE_SRQ_RESIZE
IBV_DEVICE_N_NOTIFY_CQ = c.IBV_DEVICE_N_NOTIFY_CQ

IBV_EVENT_CQ_ERR = c.IBV_EVENT_CQ_ERR
IBV_EVENT_QP_FATAL = c.IBV_EVENT_QP_FATAL
IBV_EVENT_QP_REQ_ERR = c.IBV_EVENT_QP_REQ_ERR
IBV_EVENT_QP_ACCESS_ERR = c.IBV_EVENT_QP_ACCESS_ERR
IBV_EVENT_COMM_EST = c.IBV_EVENT_COMM_EST
IBV_EVENT_SQ_DRAINED = c.IBV_EVENT_SQ_DRAINED
IBV_EVENT_PATH_MIG = c.IBV_EVENT_PATH_MIG
IBV_EVENT_PATH_MIG_ERR = c.IBV_EVENT_PATH_MIG_ERR
IBV_EVENT_DEVICE_FATAL = c.IBV_EVENT_DEVICE_FATAL
IBV_EVENT_PORT_ACTIVE = c.IBV_EVENT_PORT_ACTIVE
IBV_EVENT_PORT_ERR = c.IBV_EVENT_PORT_ERR
IBV_EVENT_LID_CHANGE = c.IBV_EVENT_LID_CHANGE
IBV_EVENT_PKEY_CHANGE = c.IBV_EVENT_PKEY_CHANGE
IBV_EVENT_SM_CHANGE = c.IBV_EVENT_SM_CHANGE
IBV_EVENT_SRQ_ERR = c.IBV_EVENT_SRQ_ERR
IBV_EVENT_SRQ_LIMIT_REACHED = c.IBV_EVENT_SRQ_LIMIT_REACHED
IBV_EVENT_QP_LAST_WQE_REACHED = c.IBV_EVENT_QP_LAST_WQE_REACHED
IBV_EVENT_CLIENT_REREGISTER = c.IBV_EVENT_CLIENT_REREGISTER

IBV_MIG_MIGRATED = c.IBV_MIG_MIGRATED
IBV_MIG_REARM = c.IBV_MIG_REARM
IBV_MIG_ARMED = c.IBV_MIG_ARMED

IBV_MTU_256 = c.IBV_MTU_256
IBV_MTU_512 = c.IBV_MTU_512
IBV_MTU_1024 = c.IBV_MTU_1024
IBV_MTU_2048 = c.IBV_MTU_2048
IBV_MTU_4096 = c.IBV_MTU_4096

IBV_MW_TYPE_1 = c.IBV_MW_TYPE_1
IBV_MW_TYPE_2 = c.IBV_MW_TYPE_2

IBV_NODE_UNKNOWN = c.IBV_NODE_UNKNOWN
IBV_NODE_CA = c.IBV_NODE_CA
IBV_NODE_SWITCH = c.IBV_NODE_SWITCH
IBV_NODE_ROUTER = c.IBV_NODE_ROUTER
IBV_NODE_RNIC = c.IBV_NODE_RNIC

IBV_PORT_NOP = c.IBV_PORT_NOP
IBV_PORT_DOWN = c.IBV_PORT_DOWN
IBV_PORT_INIT = c.IBV_PORT_INIT
IBV_PORT_ARMED = c.IBV_PORT_ARMED
IBV_PORT_ACTIVE = c.IBV_PORT_ACTIVE
IBV_PORT_ACTIVE_DEFER = c.IBV_PORT_ACTIVE_DEFER

IBV_QP_STATE = c.IBV_QP_STATE
IBV_QP_CUR_STATE = c.IBV_QP_CUR_STATE
IBV_QP_EN_SQD_ASYNC_NOTIFY = c.IBV_QP_EN_SQD_ASYNC_NOTIFY
IBV_QP_ACCESS_FLAGS = c.IBV_QP_ACCESS_FLAGS
IBV_QP_PKEY_INDEX = c.IBV_QP_PKEY_INDEX
IBV_QP_PORT = c.IBV_QP_PORT
IBV_QP_QKEY = c.IBV_QP_QKEY
IBV_QP_AV = c.IBV_QP_AV
IBV_QP_PATH_MTU = c.IBV_QP_PATH_MTU
IBV_QP_TIMEOUT = c.IBV_QP_TIMEOUT
IBV_QP_RETRY_CNT = c.IBV_QP_RETRY_CNT
IBV_QP_RNR_RETRY = c.IBV_QP_RNR_RETRY
IBV_QP_RQ_PSN = c.IBV_QP_RQ_PSN
IBV_QP_MAX_QP_RD_ATOMIC = c.IBV_QP_MAX_QP_RD_ATOMIC
IBV_QP_ALT_PATH = c.IBV_QP_ALT_PATH
IBV_QP_MIN_RNR_TIMER = c.IBV_QP_MIN_RNR_TIMER
IBV_QP_SQ_PSN = c.IBV_QP_SQ_PSN
IBV_QP_MAX_DEST_RD_ATOMIC = c.IBV_QP_MAX_DEST_RD_ATOMIC
IBV_QP_PATH_MIG_STATE = c.IBV_QP_PATH_MIG_STATE
IBV_QP_CAP = c.IBV_QP_CAP
IBV_QP_DEST_QPN = c.IBV_QP_DEST_QPN

IBV_QPS_RESET = c.IBV_QPS_RESET
IBV_QPS_INIT = c.IBV_QPS_INIT
IBV_QPS_RTR = c.IBV_QPS_RTR
IBV_QPS_RTS = c.IBV_QPS_RTS
IBV_QPS_SQD = c.IBV_QPS_SQD
IBV_QPS_SQE = c.IBV_QPS_SQE
IBV_QPS_ERR = c.IBV_QPS_ERR

IBV_QPT_RC = c.IBV_QPT_RC
IBV_QPT_UC = c.IBV_QPT_UC
IBV_QPT_UD = c.IBV_QPT_UD

IBV_RATE_MAX = c.IBV_RATE_MAX
IBV_RATE_2_5_GBPS = c.IBV_RATE_2_5_GBPS
IBV_RATE_5_GBPS = c.IBV_RATE_5_GBPS
IBV_RATE_10_GBPS = c.IBV_RATE_10_GBPS
IBV_RATE_20_GBPS = c.IBV_RATE_20_GBPS
IBV_RATE_30_GBPS = c.IBV_RATE_30_GBPS
IBV_RATE_40_GBPS = c.IBV_RATE_40_GBPS
IBV_RATE_60_GBPS = c.IBV_RATE_60_GBPS
IBV_RATE_80_GBPS = c.IBV_RATE_80_GBPS
IBV_RATE_120_GBPS = c.IBV_RATE_120_GBPS

IBV_REREG_MR_CHANGE_TRANSLATION = c.IBV_REREG_MR_CHANGE_TRANSLATION
IBV_REREG_MR_CHANGE_PD = c.IBV_REREG_MR_CHANGE_PD
IBV_REREG_MR_CHANGE_ACCESS = c.IBV_REREG_MR_CHANGE_ACCESS
IBV_REREG_MR_KEEP_VALID = c.IBV_REREG_MR_KEEP_VALID

IBV_SEND_FENCE = c.IBV_SEND_FENCE
IBV_SEND_SIGNALED = c.IBV_SEND_SIGNALED
IBV_SEND_SOLICITED = c.IBV_SEND_SOLICITED
IBV_SEND_INLINE = c.IBV_SEND_INLINE

IBV_SRQ_MAX_WR = c.IBV_SRQ_MAX_WR
IBV_SRQ_LIMIT = c.IBV_SRQ_LIMIT

IBV_TRANSPORT_UNKNOWN = c.IBV_TRANSPORT_UNKNOWN
IBV_TRANSPORT_IB = c.IBV_TRANSPORT_IB
IBV_TRANSPORT_IWARP = c.IBV_TRANSPORT_IWARP

IBV_WC_GRH = c.IBV_WC_GRH
IBV_WC_WITH_IMM = c.IBV_WC_WITH_IMM

IBV_WC_SEND = c.IBV_WC_SEND
IBV_WC_RDMA_WRITE = c.IBV_WC_RDMA_WRITE
IBV_WC_RDMA_READ = c.IBV_WC_RDMA_READ
IBV_WC_COMP_SWAP = c.IBV_WC_COMP_SWAP
IBV_WC_FETCH_ADD = c.IBV_WC_FETCH_ADD
IBV_WC_BIND_MW = c.IBV_WC_BIND_MW
IBV_WC_RECV = c.IBV_WC_RECV
IBV_WC_RECV_RDMA_WITH_IMM = c.IBV_WC_RECV_RDMA_WITH_IMM

IBV_WC_SUCCESS = c.IBV_WC_SUCCESS
IBV_WC_LOC_LEN_ERR = c.IBV_WC_LOC_LEN_ERR
IBV_WC_LOC_QP_OP_ERR = c.IBV_WC_LOC_QP_OP_ERR
IBV_WC_LOC_EEC_OP_ERR = c.IBV_WC_LOC_EEC_OP_ERR
IBV_WC_LOC_PROT_ERR = c.IBV_WC_LOC_PROT_ERR
IBV_WC_WR_FLUSH_ERR = c.IBV_WC_WR_FLUSH_ERR
IBV_WC_MW_BIND_ERR = c.IBV_WC_MW_BIND_ERR
IBV_WC_BAD_RESP_ERR = c.IBV_WC_BAD_RESP_ERR
IBV_WC_LOC_ACCESS_ERR = c.IBV_WC_LOC_ACCESS_ERR
IBV_WC_REM_INV_REQ_ERR = c.IBV_WC_REM_INV_REQ_ERR
IBV_WC_REM_ACCESS_ERR = c.IBV_WC_REM_ACCESS_ERR
IBV_WC_REM_OP_ERR = c.IBV_WC_REM_OP_ERR
IBV_WC_RETRY_EXC_ERR = c.IBV_WC_RETRY_EXC_ERR
IBV_WC_RNR_RETRY_EXC_ERR = c.IBV_WC_RNR_RETRY_EXC_ERR
IBV_WC_LOC_RDD_VIOL_ERR = c.IBV_WC_LOC_RDD_VIOL_ERR
IBV_WC_REM_INV_RD_REQ_ERR = c.IBV_WC_REM_INV_RD_REQ_ERR
IBV_WC_REM_ABORT_ERR = c.IBV_WC_REM_ABORT_ERR
IBV_WC_INV_EECN_ERR = c.IBV_WC_INV_EECN_ERR
IBV_WC_INV_EEC_STATE_ERR = c.IBV_WC_INV_EEC_STATE_ERR
IBV_WC_FATAL_ERR = c.IBV_WC_FATAL_ERR
IBV_WC_RESP_TIMEOUT_ERR = c.IBV_WC_RESP_TIMEOUT_ERR
IBV_WC_GENERAL_ERR = c.IBV_WC_GENERAL_ERR

IBV_WR_RDMA_WRITE = c.IBV_WR_RDMA_WRITE
IBV_WR_RDMA_WRITE_WITH_IMM = c.IBV_WR_RDMA_WRITE_WITH_IMM
IBV_WR_SEND = c.IBV_WR_SEND
IBV_WR_SEND_WITH_IMM = c.IBV_WR_SEND_WITH_IMM
IBV_WR_RDMA_READ = c.IBV_WR_RDMA_READ
IBV_WR_ATOMIC_CMP_AND_SWP = c.IBV_WR_ATOMIC_CMP_AND_SWP
IBV_WR_ATOMIC_FETCH_AND_ADD = c.IBV_WR_ATOMIC_FETCH_AND_ADD

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

