
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
        char *raw

    struct ibv_global_route:
        ibv_gid dgid
        unsigned int flow_label
        unsigned int sgid_index
        unsigned int hop_limit
        unsigned int traffic_class

    struct ibv_grh:
        unsigned int version_tclass_flow
        unsigned int paylen
        unsigned int next_hdr
        unsigned int hop_limit
        ibv_gid sgid
        ibv_gid dgid

    struct ibv_ah_attr:
        ibv_global_route grh
        unsigned int dlid
        unsigned int sl
        unsigned int src_path_bits
        unsigned int static_rate
        unsigned int is_global
        unsigned int port_num

    struct ibv_device:
        char *name

    struct ibv_context:
        ibv_device *device
        unsigned int async_fd
        unsigned int cmd_fd

    struct ibv_pd:
        unsigned int handle

    struct ibv_mr:
        void *addr
        size_t length
        unsigned int lkey
        unsigned int rkey
        unsigned int handle

    struct ibv_cq:
        void *cq_context
        unsigned int handle

    struct ibv_comp_channel:
        int fd

    struct ibv_ah:
        ibv_context *context
        ibv_pd *pd
        unsigned int handle

    struct ibv_wc:
        unsigned long wr_id
        unsigned int status
        unsigned int opcode
        unsigned int vendor_err
        unsigned int byte_len
        unsigned int imm_data
        unsigned int qp_num
        unsigned int src_qp
        unsigned int wc_flags
        unsigned int pkey_index
        unsigned int slid
        unsigned int sl
        unsigned int dlid_path_bits

    struct ibv_srq_attr:
        unsigned int max_wr
        unsigned int max_sge
        unsigned int srq_limit
        unsigned int handle

    struct ibv_srq_init_attr:
        void *srq_context
        ibv_srq_attr attr

    struct ibv_srq:
        void *srq_context
        unsigned int handle

    struct ibv_qp:
        void *qp_context
        unsigned int qp_num
        unsigned int qp_type
        unsigned int state
        unsigned int handle

    struct ibv_qp_cap:
        unsigned int max_send_wr
        unsigned int max_recv_wr
        unsigned int max_send_sge
        unsigned int max_recv_sge
        unsigned int max_inline_data

    struct ibv_qp_init_attr:
        void *qp_context
        ibv_cq *send_cq
        ibv_cq *recv_cq
        ibv_srq *srq
        ibv_qp_cap cap
        ibv_qp_type qp_type
        unsigned int sq_sig_all

    struct ibv_qp_attr:
        ibv_qp_state qp_state
        ibv_qp_state cur_qp_state
        ibv_mtu path_mtu
        ibv_mig_state path_mig_state
        unsigned int qkey
        unsigned int rq_psn
        unsigned int sq_psn
        unsigned int dest_qp_num
        unsigned int qp_access_flags
        ibv_qp_cap cap
        ibv_ah_attr ah_attr
        ibv_ah_attr alt_ah_attr
        unsigned int pkey_index
        unsigned int alt_pkey_index
        unsigned int en_sqd_async_notify
        unsigned int sq_draining
        unsigned int max_rd_atomic
        unsigned int max_dest_rd_atomic
        unsigned int min_rnr_timer
        unsigned int port_num
        unsigned int timeout
        unsigned int retry_cnt
        unsigned int rnr_retry
        unsigned int alt_port_num
        unsigned int alt_timeout

    struct ibv_sge:
        unsigned long addr
        unsigned int length
        unsigned int lkey

    struct ibv_send_wr_wr_rdma:
        unsigned long remote_addr
        unsigned int rkey

    struct ibv_send_wr_wr_atomic:
        unsigned long remote_addr
        unsigned long compare_add
        unsigned long swap
        unsigned int rkey

    struct ibv_send_wr_wr_ud:
        ibv_ah *ah
        unsigned int remote_qpn
        unsigned int remote_qkey

    union ibv_send_wr_wr:
        ibv_send_wr_wr_rdma rdma
        ibv_send_wr_wr_atomic atomic
        ibv_send_wr_wr_ud ud

    struct ibv_send_wr:
        unsigned long wr_id
        ibv_send_wr *next
        ibv_sge *sg_list
        unsigned int num_sge
        unsigned int opcode
        unsigned int send_flags
        unsigned int imm_data
        ibv_send_wr_wr wr

    struct ibv_recv_wr:
        unsigned long wr_id
        ibv_recv_wr *next
        ibv_sge *sg_list
        unsigned int num_sge

    struct ibv_port_attr:
        ibv_port_state state
        ibv_mtu max_mtu
        ibv_mtu active_mtu
        unsigned int gid_tbl_len
        unsigned int port_cap_flags
        unsigned int max_msg_sz
        unsigned int bad_pkey_cntr
        unsigned int qkey_viol_cntr
        unsigned int pkey_tbl_len
        unsigned int lid
        unsigned int sm_lid
        unsigned int lmc
        unsigned int max_vl_num
        unsigned int sm_sl
        unsigned int subnet_timeout
        unsigned int init_type_reply
        unsigned int active_width
        unsigned int active_speed
        unsigned int phys_state

    struct ibv_device_attr:
        char fw_ver[64]
        unsigned long node_guid
        unsigned long sys_image_guid
        unsigned long max_mr_size
        unsigned long page_size_cap
        unsigned int vendor_id
        unsigned int vendor_part_id
        unsigned int hw_ver
        unsigned int max_qp
        unsigned int max_qp_wr
        unsigned int device_cap_flags
        unsigned int max_sge
        unsigned int max_sge_rd
        unsigned int max_cq
        unsigned int max_cqe
        unsigned int max_mr
        unsigned int max_pd
        unsigned int max_qp_rd_atom
        unsigned int max_ee_rd_atom
        unsigned int max_res_rd_atom
        unsigned int max_qp_init_rd_atom
        unsigned int max_ee_init_rd_atom
        ibv_atomic_cap atomic_cap
        unsigned int max_ee
        unsigned int max_rdd
        unsigned int max_mw
        unsigned int max_raw_ipv6_qp
        unsigned int max_raw_ethy_qp
        unsigned int max_mcast_grp
        unsigned int max_mcast_qp_attach
        unsigned int max_total_mcast_qp_attach
        unsigned int max_ah
        unsigned int max_fmr
        unsigned int max_map_per_fmr
        unsigned int max_srq
        unsigned int max_srq_wr
        unsigned int max_srq_sge
        unsigned int max_pkeys
        unsigned int local_ca_ack_delay
        unsigned int phys_port_cnt

    union ibv_async_event_element:
        ibv_cq *cq
        ibv_qp *qp
        ibv_srq *srq
        unsigned int port_num

    struct ibv_async_event:
        ibv_async_event_element element
        unsigned int event_type

    ibv_device **ibv_get_device_list(int *n)
    void ibv_free_device_list(ibv_device **list)
    ibv_context *ibv_open_device(ibv_device *dev)
    int ibv_close_device(ibv_context *ctx)
    int ibv_query_port(ibv_context *ctx, unsigned int port_num, ibv_port_attr *attr)
    int ibv_query_device(ibv_context *ctx, ibv_device_attr *attr)

    ibv_pd *ibv_alloc_pd(ibv_context *ctx)
    int ibv_dealloc_pd(ibv_pd *pd)

    ibv_ah *ibv_create_ah(ibv_pd *pd, ibv_ah_attr *attr)
    int ibv_destroy_ah(ibv_ah *ah)

    ibv_mr *ibv_reg_mr(ibv_pd *pd, void *addr, unsigned int length,
                       unsigned int access)
    int ibv_dereg_mr(ibv_mr *mr)

    ibv_comp_channel *ibv_create_comp_channel(ibv_context *ctx)
    int ibv_destroy_comp_channel(ibv_comp_channel *chan)

    ibv_cq *ibv_create_cq(ibv_context *ctx, unsigned int cqe,
                          void *user_cq_ctx,
                          ibv_comp_channel *chan,
                          unsigned int comp_vector)
    int ibv_destroy_cq(ibv_cq *cq)
    int ibv_poll_cq(ibv_cq *cq, unsigned int n, ibv_wc *wc)
    int ibv_req_notify_cq(ibv_cq *cq, unsigned int solicited_only)
    int ibv_get_cq_event(ibv_comp_channel *chan,ibv_cq **,void **cq_context)
    void ibv_ack_cq_events(ibv_cq *cq,unsigned int nevents)
    int ibv_resize_cq(ibv_cq *cq, unsigned int cqe)

    ibv_qp *ibv_create_qp(ibv_pd *pd, ibv_qp_init_attr *init_attr)
    int ibv_destroy_qp(ibv_qp *qp)
    int ibv_modify_qp(ibv_qp *qp, ibv_qp_attr *attr, unsigned int attr_mask)
    int ibv_query_qp(ibv_qp *qp, ibv_qp_attr *attr, unsigned int attr_mask, ibv_qp_init_attr *init)
    int ibv_post_send(ibv_qp *qp, ibv_send_wr *wr, ibv_send_wr **bad_wr)
    int ibv_post_recv(ibv_qp *qp, ibv_recv_wr *wr, ibv_recv_wr **bad_wr)
    int ibv_attach_mcast(ibv_qp *qp, ibv_gid *gid, unsigned int lid)
    int ibv_detach_mcast(ibv_qp *qp, ibv_gid *gid, unsigned int lid)

    ibv_srq *ibv_create_srq(ibv_pd *pd,ibv_srq_init_attr *srq_init_attr)
    int ibv_destroy_srq(ibv_srq *srq)
    int ibv_modify_srq(ibv_srq *srq,ibv_srq_attr *srq_attr,int srq_attr_mask)
    int ibv_query_srq(ibv_srq *srq,ibv_srq_attr *srq_attr)
    int ibv_post_srq_recv(ibv_srq *qp, ibv_recv_wr *wr, ibv_recv_wr **bad_wr)

    int ibv_get_async_event(ibv_context *context,ibv_async_event *event)
    void ibv_ack_async_event(ibv_async_event *event)

    char *ibv_wc_status_str(unsigned int status)

