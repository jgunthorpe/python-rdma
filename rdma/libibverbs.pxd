
cdef extern from 'infiniband/verbs.h':

    enum ibv_access_flags:
        IBV_ACCESS_LOCAL_WRITE
        IBV_ACCESS_REMOTE_WRITE
        IBV_ACCESS_REMOTE_READ
        IBV_ACCESS_REMOTE_ATOMIC
        IBV_ACCESS_MW_BIND

    enum ibv_atomic_cap:
        IBV_ATOMIC_NONE
        IBV_ATOMIC_HCA
        IBV_ATOMIC_GLOB

    enum ibv_device_cap_flags:
        IBV_DEVICE_RESIZE_MAX_WR
        IBV_DEVICE_BAD_PKEY_CNTR
        IBV_DEVICE_BAD_QKEY_CNTR
        IBV_DEVICE_RAW_MULTI
        IBV_DEVICE_AUTO_PATH_MIG
        IBV_DEVICE_CHANGE_PHY_PORT
        IBV_DEVICE_UD_AV_PORT_ENFORCE
        IBV_DEVICE_CURR_QP_STATE_MOD
        IBV_DEVICE_SHUTDOWN_PORT
        IBV_DEVICE_INIT_TYPE
        IBV_DEVICE_PORT_ACTIVE_EVENT
        IBV_DEVICE_SYS_IMAGE_GUID
        IBV_DEVICE_RC_RNR_NAK_GEN
        IBV_DEVICE_SRQ_RESIZE
        IBV_DEVICE_N_NOTIFY_CQ

    enum ibv_event_type:
        IBV_EVENT_CQ_ERR
        IBV_EVENT_QP_FATAL
        IBV_EVENT_QP_REQ_ERR
        IBV_EVENT_QP_ACCESS_ERR
        IBV_EVENT_COMM_EST
        IBV_EVENT_SQ_DRAINED
        IBV_EVENT_PATH_MIG
        IBV_EVENT_PATH_MIG_ERR
        IBV_EVENT_DEVICE_FATAL
        IBV_EVENT_PORT_ACTIVE
        IBV_EVENT_PORT_ERR
        IBV_EVENT_LID_CHANGE
        IBV_EVENT_PKEY_CHANGE
        IBV_EVENT_SM_CHANGE
        IBV_EVENT_SRQ_ERR
        IBV_EVENT_SRQ_LIMIT_REACHED
        IBV_EVENT_QP_LAST_WQE_REACHED
        IBV_EVENT_CLIENT_REREGISTER

    enum ibv_mig_state:
        IBV_MIG_MIGRATED
        IBV_MIG_REARM
        IBV_MIG_ARMED

    enum ibv_mtu:
        IBV_MTU_256
        IBV_MTU_512
        IBV_MTU_1024
        IBV_MTU_2048
        IBV_MTU_4096

    enum ibv_mw_type:
        IBV_MW_TYPE_1
        IBV_MW_TYPE_2

    enum ibv_node_type:
        IBV_NODE_UNKNOWN
        IBV_NODE_CA
        IBV_NODE_SWITCH
        IBV_NODE_ROUTER
        IBV_NODE_RNIC

    enum ibv_port_state:
        IBV_PORT_NOP
        IBV_PORT_DOWN
        IBV_PORT_INIT
        IBV_PORT_ARMED
        IBV_PORT_ACTIVE
        IBV_PORT_ACTIVE_DEFER

    enum ibv_qp_attr_mask:
        IBV_QP_STATE
        IBV_QP_CUR_STATE
        IBV_QP_EN_SQD_ASYNC_NOTIFY
        IBV_QP_ACCESS_FLAGS
        IBV_QP_PKEY_INDEX
        IBV_QP_PORT
        IBV_QP_QKEY
        IBV_QP_AV
        IBV_QP_PATH_MTU
        IBV_QP_TIMEOUT
        IBV_QP_RETRY_CNT
        IBV_QP_RNR_RETRY
        IBV_QP_RQ_PSN
        IBV_QP_MAX_QP_RD_ATOMIC
        IBV_QP_ALT_PATH
        IBV_QP_MIN_RNR_TIMER
        IBV_QP_SQ_PSN
        IBV_QP_MAX_DEST_RD_ATOMIC
        IBV_QP_PATH_MIG_STATE
        IBV_QP_CAP
        IBV_QP_DEST_QPN

    enum ibv_qp_state:
        IBV_QPS_RESET
        IBV_QPS_INIT
        IBV_QPS_RTR
        IBV_QPS_RTS
        IBV_QPS_SQD
        IBV_QPS_SQE
        IBV_QPS_ERR

    enum ibv_qp_type:
        IBV_QPT_RC
        IBV_QPT_UC
        IBV_QPT_UD

    enum ibv_rate:
        IBV_RATE_MAX
        IBV_RATE_2_5_GBPS
        IBV_RATE_5_GBPS
        IBV_RATE_10_GBPS
        IBV_RATE_20_GBPS
        IBV_RATE_30_GBPS
        IBV_RATE_40_GBPS
        IBV_RATE_60_GBPS
        IBV_RATE_80_GBPS
        IBV_RATE_120_GBPS

    enum ibv_rereg_mr_flags:
        IBV_REREG_MR_CHANGE_TRANSLATION
        IBV_REREG_MR_CHANGE_PD
        IBV_REREG_MR_CHANGE_ACCESS
        IBV_REREG_MR_KEEP_VALID

    enum ibv_send_flags:
        IBV_SEND_FENCE
        IBV_SEND_SIGNALED
        IBV_SEND_SOLICITED
        IBV_SEND_INLINE

    enum ibv_srq_attr_mask:
        IBV_SRQ_MAX_WR
        IBV_SRQ_LIMIT

    enum ibv_transport_type:
        IBV_TRANSPORT_UNKNOWN
        IBV_TRANSPORT_IB
        IBV_TRANSPORT_IWARP

    enum ibv_wc_flags:
        IBV_WC_GRH
        IBV_WC_WITH_IMM

    enum ibv_wc_opcode:
        IBV_WC_SEND
        IBV_WC_RDMA_WRITE
        IBV_WC_RDMA_READ
        IBV_WC_COMP_SWAP
        IBV_WC_FETCH_ADD
        IBV_WC_BIND_MW
        IBV_WC_RECV
        IBV_WC_RECV_RDMA_WITH_IMM

    enum ibv_wc_status:
        IBV_WC_SUCCESS
        IBV_WC_LOC_LEN_ERR
        IBV_WC_LOC_QP_OP_ERR
        IBV_WC_LOC_EEC_OP_ERR
        IBV_WC_LOC_PROT_ERR
        IBV_WC_WR_FLUSH_ERR
        IBV_WC_MW_BIND_ERR
        IBV_WC_BAD_RESP_ERR
        IBV_WC_LOC_ACCESS_ERR
        IBV_WC_REM_INV_REQ_ERR
        IBV_WC_REM_ACCESS_ERR
        IBV_WC_REM_OP_ERR
        IBV_WC_RETRY_EXC_ERR
        IBV_WC_RNR_RETRY_EXC_ERR
        IBV_WC_LOC_RDD_VIOL_ERR
        IBV_WC_REM_INV_RD_REQ_ERR
        IBV_WC_REM_ABORT_ERR
        IBV_WC_INV_EECN_ERR
        IBV_WC_INV_EEC_STATE_ERR
        IBV_WC_FATAL_ERR
        IBV_WC_RESP_TIMEOUT_ERR
        IBV_WC_GENERAL_ERR

    enum ibv_wr_opcode:
        IBV_WR_RDMA_WRITE
        IBV_WR_RDMA_WRITE_WITH_IMM
        IBV_WR_SEND
        IBV_WR_SEND_WITH_IMM
        IBV_WR_RDMA_READ
        IBV_WR_ATOMIC_CMP_AND_SWP
        IBV_WR_ATOMIC_FETCH_AND_ADD

    union ibv_gid:
        char raw[16]

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

    ctypedef int size_t

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

    ibv_mr *ibv_reg_mr(ibv_pd *pd, void *addr, size_t length, int access)
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

    ibv_qp *ibv_create_qp(ibv_pd *pd, ibv_qp_init_attr *init_attr)
    int ibv_destroy_qp(ibv_qp *qp)
    int ibv_modify_qp(ibv_qp *qp, ibv_qp_attr *attr, int attr_mask)
    int ibv_query_qp(ibv_qp *qp, ibv_qp_attr *attr, int attr_mask, ibv_qp_init_attr *init)
    int ibv_post_send(ibv_qp *qp, ibv_send_wr *wr, ibv_send_wr **bad_wr)
    int ibv_post_recv(ibv_qp *qp, ibv_recv_wr *wr, ibv_recv_wr **bad_wr)
    char *ibv_wc_status_str(int status)

