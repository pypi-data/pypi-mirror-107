import cooler
import numpy as np
from scipy import stats
from scipy.ndimage import convolve
import pandas as pd
import time
from statsmodels.stats.multitest import multipletests
from heapq import heappop, heapify


def fetch_chrom(cool, chrom) -> np.array:
    return cool.matrix(balance=False, sparse=True).fetch(chrom).toarray()


def select_loop_candidates(cool_e, cool_o, min_dist, max_dist, resolution,
                           chrom):
    """Select loop candidate pixel to perform t test"""
    E = fetch_chrom(cool_e, chrom)
    O = fetch_chrom(cool_o, chrom)

    oe_filter = (E > 0) * (O > 0.1)
    loop = np.where(oe_filter)
    dist_filter = np.logical_and((loop[1] - loop[0]) > (min_dist / resolution),
                                 (loop[1] - loop[0]) < (max_dist / resolution))
    loop = (loop[0][dist_filter], loop[1][dist_filter])
    print(dist_filter.sum(), 'loop candidate pixels')
    return E, loop


def paired_t_test(cool_t, cool_t2, chrom, loop, n_cells):
    """Paired t test per pixel"""
    T = fetch_chrom(cool_t, chrom)
    T2 = fetch_chrom(cool_t2, chrom)

    loop_t = T[loop]
    loop_t2 = T2[loop]

    t_score = loop_t / np.sqrt((loop_t2 - loop_t * loop_t) / (n_cells - 1))
    p_value = stats.t.sf(t_score, n_cells - 1)
    return p_value


def scan_kernel(E, kernel, loop):
    """Scan loop surrounding background kernel"""
    E_kernel = convolve(E, kernel, mode='mirror') * (E > 0)
    return E_kernel[loop]


def loop_background(E, pad, gap, loop):
    """Calculate loop surrounding background level"""
    w = pad * 2 + 1
    kernel_bl = np.zeros((w, w), np.float32)
    kernel_bl[-pad:, :(pad - gap)] = 1
    kernel_bl[-(pad - gap):, :pad] = 1
    kernel_bl = kernel_bl / np.sum(kernel_bl)
    loop_bl = scan_kernel(E, kernel_bl, loop)

    kernel_donut = np.ones((w, w), np.float32)
    kernel_donut[pad, :] = 0
    kernel_donut[:, pad] = 0
    kernel_donut[(pad - gap):(pad + gap + 1), (pad - gap):(pad + gap + 1)] = 0
    kernel_donut = kernel_donut / np.sum(kernel_donut)
    loop_donut = scan_kernel(E, kernel_donut, loop)

    kernel_h = np.ones((3, w), np.float32)
    kernel_h[:, (pad - gap):(pad + gap + 1)] = 0
    kernel_h = kernel_h / np.sum(kernel_h)
    loop_h = scan_kernel(E, kernel_h, loop)

    kernel_v = np.ones((w, 3), np.float32)
    kernel_v[(pad - gap):(pad + gap + 1), :] = 0
    kernel_v = kernel_v / np.sum(kernel_v)
    loop_v = scan_kernel(E, kernel_v, loop)

    loop_e = E[loop]
    return loop_bl, loop_donut, loop_h, loop_v, loop_e


def call_loop_single_chrom(group_prefix,
                           chrom,
                           resolution=10000,
                           min_dist=50000,
                           max_dist=10000000,
                           pad=5,
                           gap=2):
    """calculate t test and loop background for one chromosome"""
    # matrix cool obj
    cool_e = cooler.Cooler(f'{group_prefix}.E.cool')
    cool_o = cooler.Cooler(f'{group_prefix}.O.cool')
    cool_t = cooler.Cooler(f'{group_prefix}.T.cool')
    cool_t2 = cooler.Cooler(f'{group_prefix}.T2.cool')
    n_cells = cool_e.info['group_n_cells']

    # call loop
    E, loop = select_loop_candidates(cool_e=cool_e,
                                     cool_o=cool_o,
                                     min_dist=min_dist,
                                     max_dist=max_dist,
                                     resolution=resolution,
                                     chrom=chrom)
    p_value = paired_t_test(cool_t=cool_t,
                            cool_t2=cool_t2,
                            chrom=chrom,
                            loop=loop,
                            n_cells=n_cells)
    loop_bl, loop_donut, loop_h, loop_v, loop_e = loop_background(E=E,
                                                                  pad=pad,
                                                                  gap=gap,
                                                                  loop=loop)
    # put together loop table
    data = pd.DataFrame({
        'x': loop[0],
        'y': loop[1],
        'pval': p_value,
        'E': loop_e,
        'E_bl': loop_bl,
        'E_donut': loop_donut,
        'E_h': loop_h,
        'E_v': loop_v
    })
    data['chrom'] = chrom
    return data


def filter_by_background(data, thres_bl, thres_donut, thres_h, thres_v,
                         resolution):
    data['bkfilter'] = (((data['E'] / data['E_bl'] > thres_bl) |
                         (data['E_bl'] < 0)) &
                        ((data['E'] / data['E_donut'] > thres_donut) |
                         (data['E_donut'] < 0)) &
                        ((data['E'] / data['E_h'] > thres_h) |
                         (data['E_h'] < 0)) &
                        ((data['E'] / data['E_v'] > thres_v) |
                         (data['E_v'] < 0)))
    data['x1'] = data['x'].astype(int) * resolution
    data['y1'] = data['y'].astype(int) * resolution
    data['x2'] = data['x1'] + resolution
    data['y2'] = data['y1'] + resolution
    del data['x']
    del data['y']
    return data


def find_summit(loop, res, dist_thres):
    loop = loop.copy()
    start_time = time.time()
    cord = loop[['x1', 'y1']].values // res
    idx = np.argsort(cord[:, 0])
    neighbor = {i: [] for i in range(len(idx))}
    for i in range(len(idx) - 1):
        tmp = cord[idx[i]]
        for j in range(i + 1, len(idx)):
            if cord[idx[j], 0] - tmp[0] > dist_thres:
                break
            if np.abs(tmp[1] - cord[idx[j], 1]) <= dist_thres:
                neighbor[idx[i]].append(idx[j])
                neighbor[idx[j]].append(idx[i])
    print('Build graph takes', time.time() - start_time, 'seconds')

    start_time = time.time()
    nodescore = loop['E'].values
    flag = np.zeros(len(nodescore))
    tot = len(nodescore)
    summit = []
    nodeheap = (loop['E'] *
                -1).reset_index().reset_index()[['E',
                                                 'level_0']].values.tolist()
    heapify(nodeheap)

    while tot > 0:
        t = int(heappop(nodeheap)[1])
        while flag[t]:
            t = int(heappop(nodeheap)[1])
        q = [t]
        flag[t] = 1
        tot -= 1
        head = 0
        flagtmp = np.zeros(len(nodescore))
        while (head < len(q)):
            for t in neighbor[q[head]]:
                if not flagtmp[t] and nodescore[t] < nodescore[q[head]]:
                    if not flag[t]:
                        flag[t] = 1
                        tot -= 1
                    flagtmp[t] = 1
                    q.append(t)
            head += 1
        summit.append([q[0], len(q)])
    summit = np.array(summit)
    loop = loop.iloc[summit[:, 0]]
    loop['size'] = summit[:, 1]
    print('BFS takes', time.time() - start_time, 'seconds')
    return loop


def call_loops(group_prefix,
               resolution,
               output_prefix,
               thres_bl=1.33,
               thres_donut=1.33,
               thres_h=1.2,
               thres_v=1.2,
               fdr_thres=0.1,
               dist_thres=20000,
               size_thres=1):
    group_q = f'{group_prefix}.Q.cool'
    chroms = cooler.Cooler(group_q).chromnames
    total_loops = []
    for chrom in chroms:
        print(chrom)
        data = call_loop_single_chrom(group_prefix,
                                      chrom,
                                      resolution=10000,
                                      min_dist=50000,
                                      max_dist=10000000,
                                      pad=5,
                                      gap=2)
        total_loops.append(data)
    total_loops = pd.concat(total_loops)

    # add background judge info
    total_loops = filter_by_background(data=total_loops,
                                       thres_bl=thres_bl,
                                       thres_donut=thres_donut,
                                       thres_h=thres_h,
                                       thres_v=thres_v,
                                       resolution=resolution)
    total_loops['pval_adj'] = multipletests(total_loops['pval'], 0.1,
                                            'fdr_bh')[1]
    loop = total_loops.loc[total_loops['bkfilter']
                           & (total_loops['pval_adj'] < fdr_thres)].copy()
    loop.to_hdf(f'{output_prefix}.loop_info.hdf', key='data')

    # filter and save bedpd
    bedpe_cols = ['chrom', 'x1', 'x2', 'chrom', 'y1', 'y2', 'E']
    loop.sort_values(by=['chrom', 'x1', 'y1'])[bedpe_cols].to_csv(
        f'{output_prefix}.loop.bedpe', sep='\t', index=False, header=None)
    scloop = total_loops.loc[total_loops['pval_adj'] < fdr_thres]
    scloop.sort_values(by=['chrom', 'x1', 'y1'])[bedpe_cols].to_csv(
        f'{output_prefix}.scloop.bedpe', sep='\t', index=False, header=None)
    bkloop = total_loops.loc[total_loops['bkfilter']]
    bkloop.sort_values(by=['chrom', 'x1', 'y1'])[bedpe_cols].to_csv(
        f'{output_prefix}.bkloop.bedpe', sep='\t', index=False, header=None)

    # find summit
    if loop.shape[0] > 0:
        summit = pd.concat([
            find_summit(loop=sub_df,
                        res=resolution,
                        dist_thres=dist_thres // resolution)
            for chrom, sub_df in loop.groupby('chrom')
        ],
            axis=0)
        summit = summit[summit['size'] >= size_thres]
        summit.sort_values(
            by=['chrom', 'x1', 'y1'])[bedpe_cols + ['size']].to_csv(
            f'{output_prefix}.loop_summit.bedpe',
            sep='\t',
            index=False,
            header=None)
    else:
        pd.DataFrame([]).to_csv(f'{output_prefix}.loop_summit.bedpe')
    return
