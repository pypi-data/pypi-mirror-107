import pathlib
import time
import numpy as np
from scipy.sparse import csr_matrix, load_npz, triu
from ..cool import write_coo, get_chrom_offsets
import cooler
import pandas as pd
import h5py
from concurrent.futures import ProcessPoolExecutor, as_completed

"""
Matrix names
E: Matrix normalized by global diagonal backgrounds, calculated from loop_bkg
T: Matrix normalized by global diagonal and local backgrounds, then minus E (T is the delta matrix), 
   calculated from loop_bkg
T2: T^2 of T, used to calculate t test p values 
O: Matrix indicting proportion of cells' E value passing bool_threshold (1.96 by default)
"""


def merge_cells_for_single_chromosome(output_dir,
                                      output_prefix,
                                      merge_type='EO',
                                      bool_threshold=1.96):
    start_time = time.time()
    if merge_type.upper() == 'EO':
        print('Merging E (global diag norm) and O (proportion of cells passing threshold) matrix.')
        # get cell paths
        cell_paths = [str(p) for p in pathlib.Path(output_dir).glob('*.E.npz')]
        n_cells = len(cell_paths)
        # get n_dims
        matrix = load_npz(cell_paths[0])
        n_dims = matrix.shape[0]
        # initialize
        e_sum = csr_matrix((n_dims, n_dims), dtype=np.float32)
        o_sum = csr_matrix((n_dims, n_dims), dtype=np.float32)
        for i, chrom_path in enumerate(cell_paths):
            matrix = load_npz(chrom_path)
            e_sum += matrix
            o_sum += (matrix > bool_threshold)
        write_coo(f'{output_prefix}.E.hdf', e_sum, chunk_size=None)
        write_coo(f'{output_prefix}.O.hdf', o_sum, chunk_size=None)
    else:
        print('Merging T (global and local norm) and T2 (T^2, for t-test) matrix.')
        # get cell paths
        cell_paths = [str(p) for p in pathlib.Path(output_dir).glob('*.T.npz')]
        n_cells = len(cell_paths)
        # get n_dims
        matrix = load_npz(cell_paths[0])
        n_dims = matrix.shape[0]
        # initialize
        t_sum = csr_matrix((n_dims, n_dims), dtype=np.float32)
        t2_sum = csr_matrix((n_dims, n_dims), dtype=np.float32)
        for i, chrom_path in enumerate(cell_paths):
            matrix = load_npz(chrom_path)
            t_sum += matrix
            t2_sum += matrix.multiply(matrix)
        write_coo(f'{output_prefix}.T.hdf', t_sum, chunk_size=None)
        write_coo(f'{output_prefix}.T2.hdf', t2_sum, chunk_size=None)
    print(f'Merge {n_cells} cells took {time.time() - start_time:.0f} seconds')
    return


def read_single_cool_chrom(cool_path, chrom):
    cool = cooler.Cooler(str(cool_path))
    matrix = triu(cool.matrix(balance=False, sparse=True).fetch(chrom))
    return matrix


def chrom_sum_iterator(chunk_dirs,
                       chrom_sizes,
                       chrom_offset,
                       matrix_type,
                       total_cells):
    print(f'Reading matrix {matrix_type}')
    for chrom in chrom_sizes.keys():
        # sum together multiple chunks
        # first
        cool_path = chunk_dirs[0] / f'{matrix_type}.cool'
        matrix = read_single_cool_chrom(cool_path, chrom)
        # others
        for chunk_dir in chunk_dirs[1:]:
            cool_path = chunk_dir / f'{matrix_type}.cool'
            matrix += read_single_cool_chrom(cool_path, chrom)

        matrix = matrix.tocoo()
        pixel_df = pd.DataFrame({
            'bin1_id': matrix.row,
            'bin2_id': matrix.col,
            'count': matrix.data
        })
        pixel_df.iloc[:, :2] += chrom_offset[chrom]
        pixel_df.iloc[:, -1] /= total_cells
        yield pixel_df


def save_single_matrix_type(cooler_path,
                            bins_df,
                            chunk_dirs,
                            chrom_sizes,
                            chrom_offset,
                            matrix_type,
                            total_cells):
    chrom_iter = chrom_sum_iterator(chunk_dirs,
                                    chrom_sizes,
                                    chrom_offset,
                                    matrix_type,
                                    total_cells)
    cooler.create_cooler(cool_uri=cooler_path,
                         bins=bins_df,
                         pixels=chrom_iter,
                         ordered=True,
                         dtypes={'count': np.float32})
    with h5py.File(cooler_path, 'a') as f:
        f.attrs['group_n_cells'] = total_cells
    return


def merge_group_chunks_to_group_cools(chrom_size_path,
                                      resolution,
                                      group,
                                      output_dir):
    # determine chunk dirs for the group:
    output_dir = pathlib.Path(output_dir).absolute()
    group_dir = output_dir / group
    group_dir.mkdir(exist_ok=True)

    chunk_dirs = list(output_dir.glob(f'{group}_chunk*'))

    # count total cells
    total_cells = 0
    for chunk_dir in chunk_dirs:
        total_cells += pd.read_csv(chunk_dir / 'cell_table.csv', index_col=0).shape[0]

    chrom_sizes = cooler.util.read_chromsizes(chrom_size_path)
    bins_df = cooler.binnify(chrom_sizes, resolution)
    chrom_offset = get_chrom_offsets(bins_df)

    matrix_types = ['E', 'O', 'T', 'T2', 'Q']
    with ProcessPoolExecutor(5) as exe:
        futures = {}
        for matrix_type in matrix_types:
            cooler_path = str(group_dir / f'{group}.{matrix_type}.cool')
            future = exe.submit(save_single_matrix_type,
                                cooler_path=cooler_path,
                                bins_df=bins_df,
                                chunk_dirs=chunk_dirs,
                                chrom_sizes=chrom_sizes,
                                chrom_offset=chrom_offset,
                                matrix_type=matrix_type,
                                total_cells=total_cells)
            futures[future] = matrix_type
        for future in as_completed(futures):
            matrix_type = futures[future]
            print(f'Matrix {matrix_type} generated')
            future.result()
    return
