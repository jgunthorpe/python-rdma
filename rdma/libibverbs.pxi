# -*- Python -*-
# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
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

async_event = collections.namedtuple(
     'async_event_port',
     'event_type obj');

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

