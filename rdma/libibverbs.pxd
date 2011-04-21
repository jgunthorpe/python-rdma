# -*- Python -*-
# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.

include 'libibverbs_enums.pxd'

cdef extern from 'infiniband/verbs.h':

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

